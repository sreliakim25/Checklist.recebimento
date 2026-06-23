import csv
import io
import os
import urllib.request
from datetime import datetime

from flask import Flask, jsonify, redirect, render_template, request, send_file, send_from_directory
from database.db_adapter import get_db, init_db_if_needed

app = Flask(__name__)

# Vercel sets VERCEL=1 automatically; DATABASE_URL is set manually for Postgres
_IS_VERCEL = bool(os.environ.get('VERCEL'))
_HAS_POSTGRES = bool(os.environ.get('DATABASE_URL', ''))
_IS_SERVERLESS = _IS_VERCEL or _HAS_POSTGRES

FOTOS_DIR = '/tmp/fotos' if _IS_VERCEL else 'fotos'
SVG_ORIGINAL = os.path.join('..', 'Rec. Oliveiras 1.svg')
SVG_PROCESSADO = os.path.join('static', 'svg', 'Rec_Oliveiras_1.svg')

# ── Supabase Storage ──────────────────────────────────────────────────────────
_SUPABASE_URL = os.environ.get('SUPABASE_URL', '').rstrip('/')
_SUPABASE_SERVICE_KEY = os.environ.get('SUPABASE_SERVICE_KEY', '')
_STORAGE_BUCKET = 'fotos'
_USE_SUPABASE_STORAGE = bool(_IS_VERCEL and _SUPABASE_URL and _SUPABASE_SERVICE_KEY)


def _storage_upload(path_in_bucket: str, file_bytes: bytes, content_type: str = 'image/jpeg'):
    url = f"{_SUPABASE_URL}/storage/v1/object/{_STORAGE_BUCKET}/{path_in_bucket}"
    req = urllib.request.Request(url, data=file_bytes, method='POST')
    req.add_header('Authorization', f'Bearer {_SUPABASE_SERVICE_KEY}')
    req.add_header('Content-Type', content_type)
    req.add_header('x-upsert', 'true')
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read()


def _storage_delete(path_in_bucket: str):
    url = f"{_SUPABASE_URL}/storage/v1/object/{_STORAGE_BUCKET}/{path_in_bucket}"
    req = urllib.request.Request(url, method='DELETE')
    req.add_header('Authorization', f'Bearer {_SUPABASE_SERVICE_KEY}')
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            resp.read()
    except Exception:
        pass


def _storage_public_url(path_in_bucket: str) -> str:
    return f"{_SUPABASE_URL}/storage/v1/object/public/{_STORAGE_BUCKET}/{path_in_bucket}"


def _storage_ensure_bucket():
    """Cria o bucket 'fotos' se ainda não existir (idempotente)."""
    import json
    url = f"{_SUPABASE_URL}/storage/v1/bucket"
    payload = json.dumps({'id': _STORAGE_BUCKET, 'name': _STORAGE_BUCKET, 'public': True}).encode()
    req = urllib.request.Request(url, data=payload, method='POST')
    req.add_header('Authorization', f'Bearer {_SUPABASE_SERVICE_KEY}')
    req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            resp.read()
    except urllib.error.HTTPError as e:
        if e.code != 409:  # 409 = bucket already exists
            raise


def get_config():
    with get_db() as conn:
        try:
            rows = conn.execute('SELECT chave, valor FROM config').fetchall()
            return {r['chave']: r['valor'] for r in rows}
        except Exception:
            return {}


@app.context_processor
def inject_config():
    cfg = get_config()
    return {'obra_config': cfg}


def init_db():
    if _IS_SERVERLESS:
        os.makedirs(FOTOS_DIR, exist_ok=True)
        if _USE_SUPABASE_STORAGE:
            _storage_ensure_bucket()
    else:
        os.makedirs('database', exist_ok=True)
        os.makedirs(FOTOS_DIR, exist_ok=True)
        os.makedirs(os.path.join('static', 'svg'), exist_ok=True)
    init_db_if_needed()
    if not _IS_SERVERLESS:
        _preprocessar_svg()


def _preprocessar_svg():
    """Copia o SVG original sem processar — interatividade adicionada via JS no cliente."""
    import shutil
    caminho_src = SVG_ORIGINAL
    if not os.path.exists(caminho_src):
        print(f'SVG não encontrado em: {caminho_src}')
        return
    try:
        shutil.copy2(caminho_src, SVG_PROCESSADO)
        print(f'SVG copiado para static/svg/')
    except Exception as e:
        print(f'Aviso: cópia do SVG falhou: {e}')


# ──────────────────────────── PWA assets ────────────────────────────

@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json',
                               mimetype='application/manifest+json')


@app.route('/sw.js')
def service_worker():
    return send_from_directory('static', 'sw.js',
                               mimetype='application/javascript')


@app.route('/offline')
def offline():
    return send_from_directory('static', 'offline.html',
                               mimetype='text/html')


# ──────────────────────────── Páginas HTML ────────────────────────────

@app.route('/')
def dashboard():
    return render_template('index.html')


@app.route('/mapa')
def mapa():
    svg_existe = os.path.exists(SVG_PROCESSADO)
    return render_template('mapa.html', svg_existe=svg_existe)


@app.route('/checklist/novo')
def checklist_novo():
    tipo = request.args.get('tipo', '')
    quadra = request.args.get('quadra', '')
    lote = request.args.get('lote', '')
    rua = request.args.get('rua', '')
    equipamento = request.args.get('equipamento', '')
    return render_template('checklist_form.html',
                           tipo=tipo, quadra=quadra, lote=lote,
                           rua=rua, equipamento=equipamento,
                           checklist_id=None)


@app.route('/checklist/<int:cid>')
def checklist_view(cid):
    return render_template('checklist_view.html', checklist_id=cid)


@app.route('/checklist/<int:cid>/editar')
def checklist_editar(cid):
    return render_template('checklist_form.html', checklist_id=cid,
                           tipo='', quadra='', lote='', rua='', equipamento='')


@app.route('/relatorio')
def relatorio():
    return render_template('relatorio.html')


# ──────────────────────────── API ────────────────────────────

@app.route('/api/checklist', methods=['POST', 'GET'])
def api_checklist():
    if request.method == 'POST':
        return _api_criar_checklist()
    return _api_listar_checklists()


def _api_listar_checklists():
    tipo = request.args.get('tipo', '')
    resultado = request.args.get('resultado', '')
    where, params = [], []
    if tipo:
        where.append('tipo=?')
        params.append(tipo)
    if resultado:
        where.append('resultado=?')
        params.append(resultado)
    sql = 'SELECT * FROM checklists'
    if where:
        sql += ' WHERE ' + ' AND '.join(where)
    sql += ' ORDER BY criado_em DESC'
    with get_db() as conn:
        rows = conn.execute(sql, params).fetchall()
    return jsonify([dict(r) for r in rows])


def _api_criar_checklist():
    from schemas.checklists import PK_ITENS, SCHEMAS
    data = request.json
    if not data:
        return jsonify({'erro': 'Body ausente ou inválido'}), 400
    tipo = data.get('tipo')
    schema = SCHEMAS.get(tipo)
    if not schema:
        return jsonify({'erro': f'Tipo inválido: {tipo}'}), 400

    with get_db() as conn:
        cur = conn.execute('''
            INSERT INTO checklists (tipo, quadra, lote, rua, trecho_inicio, trecho_fim,
                lotes_atendidos, equipamento, subequipamento,
                responsavel_ude, empresa_executora, data_vistoria)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        ''', (tipo, data.get('quadra'), data.get('lote'), data.get('rua'),
              data.get('trecho_inicio'), data.get('trecho_fim'),
              data.get('lotes_atendidos'), data.get('equipamento'),
              data.get('subequipamento'), data.get('responsavel_ude'),
              data.get('empresa_executora'), data.get('data_vistoria')))
        checklist_id = cur.lastrowid

        for secao in schema['secoes']:
            for item in secao['itens']:
                conn.execute('''
                    INSERT INTO checklist_itens (checklist_id, secao, item_nr, descricao, requer_foto)
                    VALUES (?,?,?,?,?)
                ''', (checklist_id, secao['titulo'], item['nr'], item['desc'],
                      1 if item.get('foto_se_nc') else 0))

        for pk_key in schema.get('pk_itens', []):
            if pk_key in PK_ITENS:
                conn.execute('''
                    INSERT INTO checklist_itens (checklist_id, secao, item_nr, descricao)
                    VALUES (?,?,?,?)
                ''', (checklist_id, 'Verificações UDE — Problemas Recorrentes',
                      pk_key, PK_ITENS[pk_key]))

    return jsonify({'id': checklist_id, 'status': 'created'})


@app.route('/api/checklist/<int:cid>', methods=['GET', 'PUT', 'DELETE'])
def api_checklist_id(cid):
    if request.method == 'GET':
        return _api_get_checklist(cid)
    if request.method == 'PUT':
        return _api_update_checklist(cid)
    return _api_delete_checklist(cid)


def _api_get_checklist(cid):
    with get_db() as conn:
        c = conn.execute('SELECT * FROM checklists WHERE id=?', (cid,)).fetchone()
        if not c:
            return jsonify({'erro': 'Não encontrado'}), 404
        itens = conn.execute(
            'SELECT * FROM checklist_itens WHERE checklist_id=? ORDER BY id', (cid,)).fetchall()
        fotos = conn.execute(
            'SELECT * FROM fotos WHERE checklist_id=?', (cid,)).fetchall()
    return jsonify({
        'checklist': dict(c),
        'itens': [dict(i) for i in itens],
        'fotos': [dict(f) for f in fotos]
    })


def _api_update_checklist(cid):
    data = request.json
    campos = ['quadra', 'lote', 'rua', 'trecho_inicio', 'trecho_fim',
              'lotes_atendidos', 'equipamento', 'responsavel_ude',
              'empresa_executora', 'data_vistoria']
    sets, vals = [], []
    for campo in campos:
        if campo in data:
            sets.append(f'{campo}=?')
            vals.append(data[campo])
    if not sets:
        return jsonify({'status': 'noop'})
    sets.append("atualizado_em=datetime('now')")
    vals.append(cid)
    with get_db() as conn:
        conn.execute(f'UPDATE checklists SET {", ".join(sets)} WHERE id=?', vals)
    return jsonify({'status': 'updated'})


def _api_delete_checklist(cid):
    with get_db() as conn:
        conn.execute('DELETE FROM checklists WHERE id=?', (cid,))
    return jsonify({'status': 'deleted'})


@app.route('/api/checklist/<int:cid>/item/<int:item_id>', methods=['PUT'])
def api_update_item(cid, item_id):
    data = request.json
    with get_db() as conn:
        conn.execute('''
            UPDATE checklist_itens SET status=?, observacao=?, local_ref=?
            WHERE id=? AND checklist_id=?
        ''', (data.get('status'), data.get('observacao'), data.get('local_ref'),
              item_id, cid))
        conn.execute("UPDATE checklists SET atualizado_em=datetime('now') WHERE id=?", (cid,))
    return jsonify({'status': 'updated'})


@app.route('/api/checklist/<int:cid>/finalizar', methods=['POST'])
def api_finalizar(cid):
    data = request.json
    with get_db() as conn:
        conn.execute('''
            UPDATE checklists SET resultado=?, observacoes_gerais=?,
            finalizado=1, atualizado_em=datetime('now') WHERE id=?
        ''', (data.get('resultado'), data.get('observacoes_gerais'), cid))
    return jsonify({'status': 'finalizado'})


@app.route('/api/foto/upload', methods=['POST'])
def api_upload_foto():
    checklist_id = request.form.get('checklist_id')
    item_id = request.form.get('item_id')
    file = request.files.get('file')
    if not file or not checklist_id:
        return jsonify({'erro': 'Arquivo ou checklist_id ausente'}), 400

    ts = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:19]
    nome = f"{item_id or 'geral'}_{ts}.jpg"
    caminho_rel = f"{checklist_id}/{nome}"

    if _USE_SUPABASE_STORAGE:
        _storage_upload(caminho_rel, file.read(), file.content_type or 'image/jpeg')
    else:
        pasta = os.path.join(FOTOS_DIR, str(checklist_id))
        os.makedirs(pasta, exist_ok=True)
        file.save(os.path.join(pasta, nome))

    legenda = request.form.get('legenda', '')

    with get_db() as conn:
        cur = conn.execute(
            'INSERT INTO fotos (checklist_id, item_id, caminho, legenda) VALUES (?,?,?,?)',
            (checklist_id, item_id or None, caminho_rel, legenda or None))
        foto_id = cur.lastrowid

    return jsonify({'foto_id': foto_id, 'caminho': caminho_rel})


@app.route('/api/foto/<int:foto_id>', methods=['PUT', 'DELETE'])
def api_foto_id(foto_id):
    if request.method == 'PUT':
        data = request.json or {}
        legenda = data.get('legenda', '')
        with get_db() as conn:
            conn.execute('UPDATE fotos SET legenda=? WHERE id=?', (legenda or None, foto_id))
        return jsonify({'status': 'updated'})
    return _api_delete_foto(foto_id)


def _api_delete_foto(foto_id):
    with get_db() as conn:
        row = conn.execute('SELECT caminho FROM fotos WHERE id=?', (foto_id,)).fetchone()
        if row:
            if _USE_SUPABASE_STORAGE:
                _storage_delete(row['caminho'])
            else:
                caminho_abs = os.path.join(FOTOS_DIR, row['caminho'])
                if os.path.exists(caminho_abs):
                    os.remove(caminho_abs)
        conn.execute('DELETE FROM fotos WHERE id=?', (foto_id,))
    return jsonify({'status': 'deleted'})


@app.route('/fotos/<path:filename>')
def servir_foto(filename):
    if _USE_SUPABASE_STORAGE:
        return redirect(_storage_public_url(filename))
    caminho = os.path.join(FOTOS_DIR, filename)
    if not os.path.exists(caminho):
        return jsonify({'erro': 'Foto não encontrada'}), 404
    return send_file(caminho)


@app.route('/api/mapa/anotacoes', methods=['GET', 'POST'])
def api_anotacoes():
    if request.method == 'POST':
        data = request.json or {}
        with get_db() as conn:
            cur = conn.execute(
                'INSERT INTO anotacoes_mapa (rua, svg_x, svg_y, texto) VALUES (?,?,?,?)',
                (data.get('rua'), data.get('svg_x', 0), data.get('svg_y', 0), data.get('texto'))
            )
        return jsonify({'id': cur.lastrowid})
    with get_db() as conn:
        rows = conn.execute('SELECT * FROM anotacoes_mapa ORDER BY criado_em DESC').fetchall()
    return jsonify([dict(r) for r in rows])


@app.route('/api/mapa/anotacoes/<int:aid>', methods=['PUT', 'DELETE'])
def api_anotacao_id(aid):
    if request.method == 'DELETE':
        with get_db() as conn:
            # Remove foto do storage se existir
            row = conn.execute('SELECT foto_caminho FROM anotacoes_mapa WHERE id=?', (aid,)).fetchone()
            if row and row['foto_caminho']:
                if _USE_SUPABASE_STORAGE:
                    _storage_delete(row['foto_caminho'])
                else:
                    caminho_abs = os.path.join(FOTOS_DIR, row['foto_caminho'])
                    if os.path.exists(caminho_abs):
                        os.remove(caminho_abs)
            conn.execute('DELETE FROM anotacoes_mapa WHERE id=?', (aid,))
        return jsonify({'status': 'deleted'})
    data = request.json or {}
    with get_db() as conn:
        conn.execute('UPDATE anotacoes_mapa SET texto=? WHERE id=?', (data.get('texto'), aid))
    return jsonify({'status': 'updated'})


@app.route('/api/mapa/anotacoes/<int:aid>/foto', methods=['POST'])
def api_anotacao_foto(aid):
    file = request.files.get('file')
    if not file:
        return jsonify({'erro': 'Arquivo ausente'}), 400
    ts = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:19]
    nome = f"anotacao_{aid}_{ts}.jpg"
    caminho_rel = f"anotacoes/{nome}"
    if _USE_SUPABASE_STORAGE:
        _storage_upload(caminho_rel, file.read(), file.content_type or 'image/jpeg')
    else:
        pasta = os.path.join(FOTOS_DIR, 'anotacoes')
        os.makedirs(pasta, exist_ok=True)
        file.save(os.path.join(pasta, nome))
    with get_db() as conn:
        conn.execute('UPDATE anotacoes_mapa SET foto_caminho=? WHERE id=?', (caminho_rel, aid))
    return jsonify({'caminho': caminho_rel})


@app.route('/api/mapa/anotacoes/pdf')
def api_anotacoes_pdf():
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.platypus import (Image, Paragraph, SimpleDocTemplate,
                                    Spacer, Table, TableStyle)

    with get_db() as conn:
        rows = conn.execute(
            'SELECT * FROM anotacoes_mapa ORDER BY criado_em ASC'
        ).fetchall()
    anotacoes = [dict(r) for r in rows]

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    TEMA = colors.HexColor('#5C1A2E')
    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle('Titulo', parent=styles['Title'],
                                  fontSize=16, textColor=TEMA,
                                  spaceAfter=6)
    sub_style = ParagraphStyle('Sub', parent=styles['Normal'],
                               fontSize=9, textColor=colors.gray,
                               spaceAfter=14)
    rua_style = ParagraphStyle('Rua', parent=styles['Normal'],
                               fontSize=11, textColor=TEMA,
                               fontName='Helvetica-Bold', spaceBefore=10, spaceAfter=4)
    obs_style = ParagraphStyle('Obs', parent=styles['Normal'],
                               fontSize=10, spaceAfter=6)

    story = [
        Paragraph('Relatório de Danos na Pavimentação', titulo_style),
        Paragraph(f'Obra 38 — Recanto das Oliveiras | UDE — Viana &amp; Moura Construções<br/>'
                  f'Gerado em: {datetime.now().strftime("%d/%m/%Y %H:%M")}', sub_style),
    ]

    if not anotacoes:
        story.append(Paragraph('Nenhuma anotação registrada.', obs_style))
    else:
        for i, a in enumerate(anotacoes, 1):
            rua = a.get('rua') or 'Rua não identificada'
            texto = a.get('texto') or '(sem descrição)'
            data = a.get('criado_em', '')
            if data and 'T' in str(data):
                data = str(data)[:16].replace('T', ' ')

            story.append(Paragraph(f'{i}. {rua}', rua_style))
            data_info = f'<font size="8" color="gray">Registrado em: {data}</font>'
            story.append(Paragraph(data_info, obs_style))
            story.append(Paragraph(texto, obs_style))

            foto_caminho = a.get('foto_caminho')
            if foto_caminho:
                foto_data = None
                if _USE_SUPABASE_STORAGE:
                    pub_url = _storage_public_url(foto_caminho)
                    try:
                        with urllib.request.urlopen(pub_url, timeout=10) as resp:
                            foto_data = io.BytesIO(resp.read())
                    except Exception:
                        pass
                else:
                    fpath = os.path.join(FOTOS_DIR, foto_caminho)
                    if os.path.exists(fpath):
                        foto_data = fpath
                if foto_data:
                    try:
                        img = Image(foto_data, width=8*cm, height=6*cm)
                        img.hAlign = 'LEFT'
                        story.append(img)
                    except Exception:
                        pass
            story.append(Spacer(1, 0.3*cm))

    doc.build(story)
    buf.seek(0)
    nome = f'Relatorio_Danos_{datetime.now().strftime("%Y%m%d")}.pdf'
    return send_file(buf, mimetype='application/pdf', as_attachment=True,
                     download_name=nome)


@app.route('/api/mapa/status')
def api_mapa_status():
    tipo = request.args.get('tipo')
    quadra = request.args.get('quadra')
    lote = request.args.get('lote')
    rua = request.args.get('rua')
    equipamento = request.args.get('equipamento')

    with get_db() as conn:
        if tipo or quadra or lote or rua or equipamento:
            where, params = [], []
            if tipo:
                where.append('tipo=?')
                params.append(tipo)
            if quadra:
                where.append('quadra=?')
                params.append(quadra)
            if lote:
                where.append('lote=?')
                params.append(lote)
            if rua:
                where.append('rua=?')
                params.append(rua)
            if equipamento:
                where.append('equipamento=?')
                params.append(equipamento)
            sql = 'SELECT id,tipo,resultado,data_vistoria,responsavel_ude,finalizado FROM checklists'
            if where:
                sql += ' WHERE ' + ' AND '.join(where)
            sql += ' ORDER BY criado_em DESC'
            rows = conn.execute(sql, params).fetchall()
            return jsonify({'checklists': [dict(r) for r in rows]})

        lotes = conn.execute('''
            SELECT quadra, lote, resultado
            FROM checklists WHERE tipo='lote' AND finalizado=1
            GROUP BY quadra, lote
            HAVING MAX(CASE resultado WHEN 'REPROVADO' THEN 1
                                       WHEN 'APROVADO COM RESSALVAS' THEN 2
                                       WHEN 'APROVADO' THEN 3 ELSE 0 END)
        ''').fetchall()
        ruas_rows = conn.execute('''
            SELECT rua, resultado FROM checklists
            WHERE tipo IN ('pavimentacao','passeio','saa','drenagem','ses') AND finalizado=1
        ''').fetchall()
        equip = conn.execute('''
            SELECT tipo, equipamento, resultado FROM checklists
            WHERE tipo IN ('guarita','quiosque','dep_lixo','deck','salao','parque','campo','quadra_esportiva') AND finalizado=1
        ''').fetchall()

    return jsonify({
        'lotes': [dict(r) for r in lotes],
        'ruas': [dict(r) for r in ruas_rows],
        'equipamentos': [dict(r) for r in equip]
    })


@app.route('/api/dashboard')
def api_dashboard():
    with get_db() as conn:
        total = conn.execute(
            'SELECT COUNT(*) FROM checklists WHERE finalizado=1').fetchone()[0]
        por_resultado = conn.execute('''
            SELECT resultado, COUNT(*) as qtd FROM checklists
            WHERE finalizado=1 GROUP BY resultado
        ''').fetchall()
        por_tipo = conn.execute('''
            SELECT tipo, COUNT(*) as qtd FROM checklists
            WHERE finalizado=1 GROUP BY tipo ORDER BY qtd DESC
        ''').fetchall()
        recentes = conn.execute('''
            SELECT id, tipo, resultado, data_vistoria,
                   quadra, lote, rua, equipamento, responsavel_ude
            FROM checklists WHERE finalizado=1
            ORDER BY atualizado_em DESC LIMIT 10
        ''').fetchall()
        lotes_avaliados = conn.execute(
            "SELECT COUNT(DISTINCT quadra||'-'||lote) FROM checklists "
            "WHERE tipo='lote' AND finalizado=1").fetchone()[0]
        rascunhos = conn.execute(
            'SELECT COUNT(*) FROM checklists WHERE finalizado=0').fetchone()[0]
        total_geral = conn.execute('SELECT COUNT(*) FROM checklists').fetchone()[0]

    return jsonify({
        'total': total,
        'total_geral': total_geral,
        'por_resultado': {r['resultado']: r['qtd'] for r in por_resultado},
        'por_tipo': [{'tipo': r['tipo'], 'qtd': r['qtd']} for r in por_tipo],
        'recentes': [dict(r) for r in recentes],
        'lotes_avaliados': lotes_avaliados,
        'lotes_total': 505,
        'rascunhos': rascunhos
    })


@app.route('/api/schema/<tipo>')
def api_schema(tipo):
    from schemas.checklists import PK_ITENS, SCHEMAS
    schema = SCHEMAS.get(tipo)
    if not schema:
        return jsonify({'erro': 'Tipo inválido'}), 404
    pk = {k: PK_ITENS[k] for k in schema.get('pk_itens', []) if k in PK_ITENS}
    return jsonify({**schema, 'pk_itens_dados': pk})


@app.route('/api/checklist/<int:cid>/pdf')
def api_pdf(cid):
    from pdf.exportar import gerar_pdf
    with get_db() as conn:
        c = conn.execute('SELECT * FROM checklists WHERE id=?', (cid,)).fetchone()
        if not c:
            return jsonify({'erro': 'Não encontrado'}), 404
        itens = conn.execute(
            'SELECT * FROM checklist_itens WHERE checklist_id=? ORDER BY id', (cid,)).fetchall()
        fotos = conn.execute(
            'SELECT * FROM fotos WHERE checklist_id=?', (cid,)).fetchall()

    pdf_bytes = gerar_pdf(dict(c), [dict(i) for i in itens], [dict(f) for f in fotos], get_config(), FOTOS_DIR)
    tipo = c['tipo']
    quad = c['quadra'] or ''
    lot = c['lote'] or ''
    rua = (c['rua'] or '').replace(' ', '_').replace('.', '').replace('º', '')
    data = (c['data_vistoria'] or datetime.now().strftime('%Y-%m-%d'))

    if quad and lot:
        nome = f'Checklist_{tipo}_{quad}-{lot}_{data}.pdf'
    elif rua:
        nome = f'Checklist_{tipo}_{rua}_{data}.pdf'
    elif c['equipamento']:
        eq = (c['equipamento'] or '').replace(' ', '_')
        nome = f'Checklist_{tipo}_{eq}_{data}.pdf'
    else:
        nome = f'Checklist_{tipo}_{data}.pdf'

    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=nome
    )


@app.route('/api/relatorio/csv')
def api_relatorio_csv():
    with get_db() as conn:
        rows = conn.execute('''
            SELECT id, tipo, quadra, lote, rua, trecho_inicio, trecho_fim,
                   equipamento, responsavel_ude, empresa_executora,
                   data_vistoria, resultado, observacoes_gerais,
                   finalizado, criado_em, atualizado_em
            FROM checklists ORDER BY criado_em DESC
        ''').fetchall()

    output = io.StringIO()
    if rows:
        w = csv.DictWriter(output, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows([dict(r) for r in rows])
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8-sig')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='checklists_obra38.csv'
    )


@app.route('/api/config', methods=['GET', 'PUT'])
def api_config():
    if request.method == 'GET':
        return jsonify(get_config())
    data = request.json or {}
    campos_permitidos = {'nome_obra', 'numero_obra', 'construtora'}
    with get_db() as conn:
        for chave, valor in data.items():
            if chave in campos_permitidos:
                conn.execute(
                    'INSERT OR REPLACE INTO config (chave, valor) VALUES (?,?)',
                    (chave, valor))
    return jsonify({'status': 'updated'})


# Inicializa banco ao importar o módulo (necessário para Vercel que não executa __main__)
try:
    init_db()
except Exception as _init_err:
    print(f'[init_db] aviso: {_init_err}')


if __name__ == '__main__':
    pass  # init_db já foi chamado acima
    import socket
    porta = 5000
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(('localhost', 5000)) == 0:
            porta = 5001
            print('AVISO: Porta 5000 ocupada (AirPlay Receiver?). Usando porta 5001.')
            print('Dica: desabilite "AirPlay Receiver" em Ajustes > Geral > AirDrop para usar 5000.')
    print('=' * 55)
    print(' Sistema de Checklists — Obra 38 — Recanto das Oliveiras')
    print(f' Acesse: http://localhost:{porta}')
    print('=' * 55)
    app.run(host='0.0.0.0', port=porta, debug=False)
