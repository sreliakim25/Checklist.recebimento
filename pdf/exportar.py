import io
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle,
    Paragraph, Spacer, Image, KeepTogether, PageBreak
)

CORES = {
    'lote':         ('#5C1A2E', '#8B3A5A'),
    'pavimentacao': ('#5C1A2E', '#8B3A5A'),
    'passeio':      ('#5C1A2E', '#8B3A5A'),
    'saa':          ('#5C1A2E', '#8B3A5A'),
    'drenagem':     ('#5C1A2E', '#8B3A5A'),
    'ses':          ('#5C1A2E', '#8B3A5A'),
    'guarita':      ('#1B3C6B', '#2E5FA3'),
    'quiosque':     ('#1B3C6B', '#2E5FA3'),
    'salao':        ('#1B3C6B', '#2E5FA3'),
    'dep_lixo':     ('#4A2000', '#7A4010'),
    'deck':         ('#1B5E5A', '#2D8A84'),
}

TITULOS = {
    'lote':         'Checklist de Recebimento — Lote',
    'pavimentacao': 'Checklist de Recebimento — Pavimentação',
    'passeio':      'Checklist de Recebimento — Passeio / Boulevard',
    'saa':          'Checklist de Recebimento — Sistema de Abastecimento de Água',
    'drenagem':     'Checklist de Recebimento — Sistema de Drenagem',
    'ses':          'Checklist de Recebimento — Sistema de Esgotamento Sanitário',
    'guarita':      'Checklist de Recebimento — Guarita',
    'quiosque':     'Checklist de Recebimento — Quiosques',
    'dep_lixo':     'Checklist de Recebimento — Depósito de Lixo',
    'deck':         'Checklist de Recebimento — Deck de Piscinas',
    'salao':        'Checklist de Recebimento — Salão de Festas',
}

STATUS_LABEL = {'C': 'Conforme', 'NC': 'Não Conforme', 'NA': 'N/A'}

PAGE_W = A4[0]
PAGE_H = A4[1]
L_MARGIN = 1.5 * cm
R_MARGIN = 1.5 * cm
TABLE_W = PAGE_W - L_MARGIN - R_MARGIN

THUMB_W = 5.2 * cm
THUMB_H = 4.0 * cm
THUMB_COLS = 3        # miniaturas por linha no inline
ANNEX_IMG_W = 8.0 * cm
ANNEX_IMG_H = 6.2 * cm


def _estilos(cor_h):
    return {
        'titulo': ParagraphStyle('titulo', fontName='Helvetica-Bold', fontSize=13,
                                 textColor=colors.HexColor('#FFFFFF')),
        'sub':    ParagraphStyle('sub', fontName='Helvetica', fontSize=9,
                                 textColor=colors.HexColor('#FFFFFF')),
        'sec':    ParagraphStyle('sec', fontName='Helvetica-Bold', fontSize=8,
                                 textColor=colors.white),
        'item':   ParagraphStyle('item', fontName='Helvetica', fontSize=8,
                                 leading=10),
        'obs':    ParagraphStyle('obs', fontName='Helvetica', fontSize=7,
                                 textColor=colors.HexColor('#444444'), leading=9),
        'label':  ParagraphStyle('label', fontName='Helvetica-Bold', fontSize=8),
        'value':  ParagraphStyle('value', fontName='Helvetica', fontSize=8),
        'leg':    ParagraphStyle('leg', fontName='Helvetica', fontSize=7.5,
                                 textColor=colors.HexColor('#444444')),
        'caption': ParagraphStyle('caption', fontName='Helvetica', fontSize=6.5,
                                  textColor=colors.HexColor('#555555'), leading=8,
                                  alignment=1),
        'annex_nr': ParagraphStyle('annex_nr', fontName='Helvetica-Bold', fontSize=9,
                                   textColor=colors.HexColor('#1F2937'), leading=11),
        'annex_desc': ParagraphStyle('annex_desc', fontName='Helvetica', fontSize=8,
                                     textColor=colors.HexColor('#374151'), leading=10),
        'annex_obs': ParagraphStyle('annex_obs', fontName='Helvetica-Oblique', fontSize=7.5,
                                    textColor=colors.HexColor('#555555'), leading=9),
    }


def _bloco_cabecalho(c, estilos, cor_h, cor_s, config):
    tipo = c.get('tipo', '')
    titulo = TITULOS.get(tipo, 'Checklist de Recebimento')
    nome_obra = config.get('nome_obra', 'Empreendimento')
    num_obra = config.get('numero_obra', '—')
    construtora = config.get('construtora', '')

    localizador = ''
    if c.get('quadra') and c.get('lote'):
        localizador = f"Quadra: {c['quadra']}  |  Lote: {c['lote']}"
    elif c.get('rua'):
        localizador = f"Rua/Trecho: {c['rua']}"
        if c.get('trecho_inicio') or c.get('trecho_fim'):
            localizador += f"  |  Trecho: {c.get('trecho_inicio', '')} – {c.get('trecho_fim', '')}"
    elif c.get('equipamento'):
        localizador = f"Equipamento: {c['equipamento']}"

    data_str = c.get('data_vistoria', '___/___/______') or '___/___/______'
    resp = c.get('responsavel_ude', '') or ''
    empresa = c.get('empresa_executora', '') or ''

    cabecalho_txt = f"Obra {num_obra} — {nome_obra} | UDE — {construtora}"
    hdr_data = [
        [Paragraph(cabecalho_txt, estilos['sub']),
         Paragraph(titulo, estilos['titulo'])],
    ]
    hdr_tbl = Table(hdr_data, colWidths=[TABLE_W * 0.35, TABLE_W * 0.65])
    hdr_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), cor_h),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (0, -1), 8),
        ('LEFTPADDING', (1, 0), (1, -1), 6),
    ]))

    id_rows = [
        ['Data de Vistoria:', data_str, 'Responsável UDE:', resp],
        ['Empresa Executora:', empresa, 'Localizador:', localizador],
    ]
    id_tbl = Table(id_rows, colWidths=[TABLE_W * 0.18, TABLE_W * 0.27, TABLE_W * 0.18, TABLE_W * 0.37])
    id_tbl.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F3F4F6')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ]))

    return [hdr_tbl, id_tbl]


def _legenda(estilos):
    dados = [['C = Conforme', 'NC = Não Conforme', 'N/A = Não se Aplica']]
    tbl = Table(dados, colWidths=[TABLE_W / 3] * 3)
    tbl.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7.5),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F9FAFB')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    return tbl


def _miniaturas_inline(fts):
    """Linha(s) de miniaturas (5cm) com caption, até THUMB_COLS por linha."""
    imgs_validas = []
    for f in fts:
        caminho_abs = os.path.join('fotos', f['caminho'])
        if os.path.exists(caminho_abs):
            imgs_validas.append((caminho_abs, f))

    if not imgs_validas:
        return []

    col_w = THUMB_W + 0.3 * cm
    linhas = []
    for inicio in range(0, len(imgs_validas), THUMB_COLS):
        grupo = imgs_validas[inicio:inicio + THUMB_COLS]
        img_row = []
        cap_row = []
        for caminho, f in grupo:
            img_row.append(Image(caminho, width=THUMB_W, height=THUMB_H))
            # caption com número sequencial baseado no nome do arquivo
            nome = os.path.basename(f['caminho'])
            cap_row.append(Paragraph(nome[:28], _estilos(None)['caption']))

        pad = THUMB_COLS - len(grupo)
        img_row += [''] * pad
        cap_row += [''] * pad

        tbl = Table(
            [img_row, cap_row],
            colWidths=[col_w] * THUMB_COLS,
        )
        tbl.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('LEFTPADDING', (0, 0), (-1, -1), 2),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F9FAFB')),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
        ]))
        linhas.append(tbl)

    return linhas


def _secao(nome, itens, fotos_por_item, estilos, cor_h, cor_s):
    elementos = []
    p = Paragraph(nome.upper(), estilos['sec'])
    tbl_hdr = Table([[p]], colWidths=[TABLE_W])
    tbl_hdr.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), cor_h),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ]))
    elementos.append(tbl_hdr)

    colunas = ['Nº', 'Descrição do Item', 'C', 'NC', 'N/A', 'Observação']
    widths = [1.0 * cm, 9.5 * cm, 1.0 * cm, 1.0 * cm, 1.0 * cm, 4.8 * cm]
    widths[1] = TABLE_W - sum(widths) + widths[1]

    hdr = Table([colunas], colWidths=widths)
    hdr.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), cor_s),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elementos.append(hdr)

    for i, item in enumerate(itens):
        s = item.get('status', 'NA')
        linha = [
            item['item_nr'],
            Paragraph(item['descricao'], estilos['item']),
            'X' if s == 'C' else '',
            'X' if s == 'NC' else '',
            'X' if s == 'NA' else '',
            Paragraph(item.get('observacao') or '', estilos['obs']),
        ]
        row_style = [
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (2, 0), (4, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
        ]
        if s == 'NC':
            row_style.append(('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FFF5F5')))
            row_style.append(('TEXTCOLOR', (3, 0), (3, -1), colors.HexColor('#EF4444')))
            row_style.append(('FONTNAME', (3, 0), (3, -1), 'Helvetica-Bold'))
        elif i % 2 == 0:
            row_style.append(('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F9FAFB')))

        t = Table([linha], colWidths=widths)
        t.setStyle(TableStyle(row_style))
        block = [t]

        if item['id'] in fotos_por_item:
            block.extend(_miniaturas_inline(fotos_por_item[item['id']]))

        elementos.append(KeepTogether(block))

    return elementos


def _registro_fotografico(itens_ordenados, fotos_por_item, fotos_gerais, estilos, cor_h):
    """Seção anexa: foto grande (8cm) + informações completas do item."""
    # Coleta todas as fotos com contexto, mantendo a ordem dos itens
    entradas = []
    for item in itens_ordenados:
        fts = fotos_por_item.get(item['id'], [])
        for f in fts:
            caminho_abs = os.path.join('fotos', f['caminho'])
            if os.path.exists(caminho_abs):
                entradas.append((caminho_abs, item, f))

    # Fotos gerais (sem item vinculado)
    for f in fotos_gerais:
        caminho_abs = os.path.join('fotos', f['caminho'])
        if os.path.exists(caminho_abs):
            entradas.append((caminho_abs, None, f))

    if not entradas:
        return []

    elementos = [PageBreak()]

    # Cabeçalho da seção
    p_hdr = Paragraph('REGISTRO FOTOGRÁFICO', estilos['sec'])
    tbl_hdr = Table([[p_hdr]], colWidths=[TABLE_W])
    tbl_hdr.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), cor_h),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ]))
    elementos.append(tbl_hdr)
    elementos.append(Spacer(1, 0.4 * cm))

    info_w = TABLE_W - ANNEX_IMG_W - 0.5 * cm

    for idx, (caminho_abs, item, foto) in enumerate(entradas, 1):
        img = Image(caminho_abs, width=ANNEX_IMG_W, height=ANNEX_IMG_H)

        if item:
            s = item.get('status', 'NA')
            status_cor = {'C': '#16a34a', 'NC': '#dc2626', 'NA': '#6B7280'}.get(s, '#6B7280')
            status_txt = STATUS_LABEL.get(s, '—')

            linhas_info = [
                Paragraph(f"<b>Item {item['item_nr']}</b>  "
                          f"<font color='{status_cor}'>[{status_txt}]</font>",
                          estilos['annex_nr']),
                Spacer(1, 0.15 * cm),
                Paragraph(item['descricao'], estilos['annex_desc']),
            ]
            if item.get('observacao'):
                linhas_info.append(Spacer(1, 0.1 * cm))
                linhas_info.append(Paragraph(f"Obs: {item['observacao']}", estilos['annex_obs']))
            if item.get('local_ref'):
                linhas_info.append(Paragraph(f"Local/Ref: {item['local_ref']}", estilos['annex_obs']))
        else:
            linhas_info = [Paragraph('<b>Foto geral</b>', estilos['annex_nr'])]

        linhas_info.append(Spacer(1, 0.1 * cm))
        nome_arq = os.path.basename(foto['caminho'])
        linhas_info.append(Paragraph(f"Arquivo: {nome_arq}", estilos['annex_obs']))

        info_cell = linhas_info

        row_bg = colors.HexColor('#FFF5F5') if (item and item.get('status') == 'NC') else colors.HexColor('#FAFAFA')

        foto_tbl = Table(
            [[img, info_cell]],
            colWidths=[ANNEX_IMG_W + 0.3 * cm, info_w],
        )
        foto_tbl.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('BACKGROUND', (0, 0), (-1, -1), row_bg),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
        ]))
        elementos.append(KeepTogether([foto_tbl, Spacer(1, 0.25 * cm)]))

    return elementos


def _obs_gerais(obs_texto, estilos, cor_h):
    p_hdr = Paragraph('OBSERVAÇÕES GERAIS', estilos['sec'])
    tbl_hdr = Table([[p_hdr]], colWidths=[TABLE_W])
    tbl_hdr.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), cor_h),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ]))
    texto = obs_texto or ''
    linhas_obs = max(texto.count('\n') + 1, 5)
    p_obs = Paragraph(texto.replace('\n', '<br/>'), estilos['obs'])
    tbl_obs = Table([[p_obs]], colWidths=[TABLE_W])
    tbl_obs.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), int(linhas_obs * 9)),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ]))
    return [tbl_hdr, tbl_obs]


def _resultado_assinaturas(resultado, estilos, cor_h):
    p_hdr = Paragraph('RESULTADO FINAL E ASSINATURAS', estilos['sec'])
    tbl_hdr = Table([[p_hdr]], colWidths=[TABLE_W])
    tbl_hdr.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), cor_h),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ]))

    ops = ['APROVADO', 'APROVADO COM RESSALVAS', 'REPROVADO']
    partes = []
    for op in ops:
        if op == resultado:
            partes.append(f'<b>( X ) {op}</b>')
        else:
            partes.append(f'(   ) {op}')
    res_linha = '     '.join(partes)

    p_res = Paragraph(res_linha, estilos['label'])
    tbl_res = Table([[p_res]], colWidths=[TABLE_W])
    tbl_res.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F9FAFB')),
    ]))

    col_w = TABLE_W / 3
    assin_hdr = [['Responsável UDE', 'Responsável Obra / Empresa', 'Fiscal / Supervisor']]
    assin_hdr_tbl = Table(assin_hdr, colWidths=[col_w] * 3)
    assin_hdr_tbl.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F3F4F6')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    assin_body_tbl = Table([['', '', '']], colWidths=[col_w] * 3, rowHeights=[2.5 * cm])
    assin_body_tbl.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
    ]))

    return [tbl_hdr, tbl_res, Spacer(1, 0.3 * cm), assin_hdr_tbl, assin_body_tbl]


def gerar_pdf(checklist: dict, itens: list, fotos: list, config: dict = None) -> bytes:
    if config is None:
        config = {}
    buf = io.BytesIO()
    tipo = checklist.get('tipo', 'lote')
    cor_h_hex, cor_s_hex = CORES.get(tipo, ('#5C1A2E', '#8B3A5A'))
    cor_h = colors.HexColor(cor_h_hex)
    cor_s = colors.HexColor(cor_s_hex)

    nome_obra = config.get('nome_obra', 'Empreendimento')
    num_obra = config.get('numero_obra', '—')
    construtora = config.get('construtora', '')

    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=L_MARGIN, rightMargin=R_MARGIN,
        topMargin=2 * cm, bottomMargin=3 * cm,
        title=TITULOS.get(tipo, 'Checklist de Recebimento'),
        author=f'UDE — {construtora}'
    )

    story = []
    estilos = _estilos(cor_h)

    story.extend(_bloco_cabecalho(checklist, estilos, cor_h, cor_s, config))
    story.append(Spacer(1, 0.3 * cm))
    story.append(_legenda(estilos))
    story.append(Spacer(1, 0.4 * cm))

    secoes = {}
    for item in itens:
        secoes.setdefault(item['secao'], []).append(item)

    fotos_por_item = {}
    fotos_gerais = []
    for f in fotos:
        if f.get('item_id'):
            fotos_por_item.setdefault(f['item_id'], []).append(f)
        else:
            fotos_gerais.append(f)

    for secao_nome, secao_itens in secoes.items():
        story.extend(_secao(secao_nome, secao_itens, fotos_por_item, estilos, cor_h, cor_s))
        story.append(Spacer(1, 0.3 * cm))

    story.extend(_obs_gerais(checklist.get('observacoes_gerais', ''), estilos, cor_h))
    story.append(Spacer(1, 0.3 * cm))
    story.extend(_resultado_assinaturas(checklist.get('resultado', ''), estilos, cor_h))

    # Anexo fotográfico (nova página)
    story.extend(_registro_fotografico(itens, fotos_por_item, fotos_gerais, estilos, cor_h))

    rodape_txt = f'Obra {num_obra} — {nome_obra} | UDE — {construtora}'

    def _rodape(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 7)
        canvas.setFillColor(colors.HexColor('#666666'))
        txt = f'Página {doc.page} | {rodape_txt}'
        canvas.drawCentredString(PAGE_W / 2, 1.2 * cm, txt)
        canvas.setStrokeColor(colors.HexColor('#CCCCCC'))
        canvas.line(L_MARGIN, 1.5 * cm, PAGE_W - R_MARGIN, 1.5 * cm)
        canvas.restoreState()

    doc.build(story, onFirstPage=_rodape, onLaterPages=_rodape)
    return buf.getvalue()
