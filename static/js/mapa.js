const EQUIPAMENTOS = [
  { tipo: 'guarita',  label: 'GUARITA',        equipamento: 'guarita',        cx: 680, cy: 80  },
  { tipo: 'quiosque', label: 'QUIOSQUES',       equipamento: 'quiosque',       cx: 400, cy: 550 },
  { tipo: 'salao',    label: 'SALÃO DE FESTAS', equipamento: 'salao-festas',   cx: 400, cy: 480 },
  { tipo: 'deck',     label: 'DECK PISCINAS',   equipamento: 'deck-piscina',   cx: 350, cy: 520 },
  { tipo: 'dep_lixo', label: 'DEP. LIXO',       equipamento: 'deposito-lixo',  cx: 650, cy: 200 },
];

let SVG_EL = null;

document.addEventListener('DOMContentLoaded', async function () {
  if (!SVG_DISPONIVEL) return;

  SVG_EL = await carregarSVG();
  if (!SVG_EL) return;

  processarCamadasSVG(SVG_EL);
  await carregarStatus();
  adicionarMarcadoresEquipamentos(SVG_EL);
  registrarEventosMapa();
  registrarFechaPanel();
});

// ── Carrega o SVG via fetch + DOMParser (preserva namespaces corretamente) ──
async function carregarSVG() {
  const container = document.getElementById('svg-container');
  try {
    const resp = await fetch('/static/svg/Rec_Oliveiras_1.svg');
    if (!resp.ok) throw new Error('SVG não encontrado');
    const texto = await resp.text();

    const parser = new DOMParser();
    const doc = parser.parseFromString(texto, 'image/svg+xml');
    const svgEl = doc.documentElement;

    // Verificar erros de parse
    if (svgEl.tagName === 'parsererror') throw new Error('SVG inválido');

    // Ajustar dimensões para responsividade
    const w = parseFloat(svgEl.getAttribute('width'));
    const h = parseFloat(svgEl.getAttribute('height'));
    if (w && h && !svgEl.getAttribute('viewBox')) {
      svgEl.setAttribute('viewBox', `0 0 ${w} ${h}`);
    }
    svgEl.removeAttribute('width');
    svgEl.removeAttribute('height');
    svgEl.style.width = '100%';
    svgEl.style.height = '100%';
    svgEl.setAttribute('preserveAspectRatio', 'xMidYMid meet');
    svgEl.id = 'svg-principal';

    container.innerHTML = '';
    container.appendChild(svgEl);
    return svgEl;
  } catch (e) {
    container.innerHTML = `<p class="sem-mapa">Erro ao carregar mapa: ${e.message}</p>`;
    return null;
  }
}

// ── Adiciona classes clicáveis às camadas por ID Inkscape ──
function processarCamadasSVG(svgEl) {
  const camadas = [
    { id: 'g3065', tipo: 'lote',    classes: ['clicavel', 'lote']    },
    { id: 'g7237', tipo: 'rua',     classes: ['clicavel', 'rua']     },
    { id: 'g4477', tipo: 'passeio', classes: ['clicavel', 'passeio'] },
  ];
  camadas.forEach(({ id, tipo, classes }) => {
    const layer = svgEl.getElementById ? svgEl.getElementById(id) : svgEl.querySelector(`#${id}`);
    if (!layer) return;
    Array.from(layer.children).forEach(el => {
      el.setAttribute('data-tipo', tipo);
      classes.forEach(c => el.classList.add(c));
    });
  });
}

// ── Colorir mapa conforme status do banco ──
async function carregarStatus() {
  try {
    const resp = await fetch('/api/mapa/status');
    const data = await resp.json();

    data.lotes.forEach(item => {
      document.querySelectorAll(
        `[data-tipo="lote"][data-quadra="${item.quadra}"][data-lote="${item.lote}"]`
      ).forEach(el => el.setAttribute('data-resultado', item.resultado));
    });

    data.ruas.forEach(item => {
      document.querySelectorAll(`[data-rua="${item.rua}"]`)
        .forEach(el => el.setAttribute('data-resultado', item.resultado));
    });

    data.equipamentos.forEach(item => {
      document.querySelectorAll(`[data-tipo="${item.tipo}"]`)
        .forEach(el => el.setAttribute('data-resultado', item.resultado));
    });
  } catch (e) {
    console.warn('Erro ao carregar status do mapa:', e);
  }
}

// ── Marcadores de equipamentos (círculos sobrepostos) ──
function adicionarMarcadoresEquipamentos(svgEl) {
  EQUIPAMENTOS.forEach(eq => {
    const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    g.setAttribute('class', 'clicavel equipamento');
    g.setAttribute('data-tipo', eq.tipo);
    g.setAttribute('data-equipamento', eq.equipamento);
    g.style.cursor = 'pointer';

    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle.setAttribute('cx', eq.cx);
    circle.setAttribute('cy', eq.cy);
    circle.setAttribute('r', 14);
    circle.setAttribute('fill', '#5C1A2E');
    circle.setAttribute('fill-opacity', '0.85');
    circle.setAttribute('stroke', '#fff');
    circle.setAttribute('stroke-width', '2');

    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    text.setAttribute('x', eq.cx);
    text.setAttribute('y', eq.cy - 20);
    text.setAttribute('text-anchor', 'middle');
    text.setAttribute('font-size', '8');
    text.setAttribute('font-family', 'Helvetica, Arial, sans-serif');
    text.setAttribute('fill', '#1e293b');
    text.setAttribute('font-weight', 'bold');
    text.textContent = eq.label;

    g.appendChild(circle);
    g.appendChild(text);
    svgEl.appendChild(g);
  });
}

// ── Eventos de clique no mapa ──
function registrarEventosMapa() {
  const area = document.getElementById('svg-mapa');
  area.addEventListener('click', async function (e) {
    const el = e.target.closest('.clicavel');
    if (!el) return;

    document.querySelectorAll('.clicavel.selecionado')
      .forEach(x => x.classList.remove('selecionado'));
    el.classList.add('selecionado');

    const params = new URLSearchParams();
    const tipo = el.getAttribute('data-tipo');

    if (tipo === 'lote') {
      params.set('tipo', 'lote');
      const q = el.getAttribute('data-quadra');
      const l = el.getAttribute('data-lote');
      if (q) params.set('quadra', q);
      if (l) params.set('lote', l);
    } else if (tipo === 'rua') {
      params.set('tipo', 'pavimentacao');
      const r = el.getAttribute('data-rua');
      if (r) params.set('rua', r);
    } else if (tipo === 'passeio') {
      params.set('tipo', 'passeio');
      const r = el.getAttribute('data-rua');
      if (r) params.set('rua', r);
    } else {
      // equipamento
      params.set('tipo', tipo);
      const eq = el.getAttribute('data-equipamento') || el.closest('[data-equipamento]')?.getAttribute('data-equipamento');
      if (eq) params.set('equipamento', eq);
    }

    const resp = await fetch('/api/mapa/status?' + params.toString());
    const data = await resp.json();

    if (data.checklists && data.checklists.length > 0) {
      mostrarPainelExistentes(data.checklists, params, el);
    } else {
      mostrarPainelVazio(params, el);
    }
  });
}

function registrarFechaPanel() {
  document.getElementById('painel-fechar').addEventListener('click', () => {
    document.getElementById('painel-lateral').classList.remove('aberto');
    document.querySelectorAll('.clicavel.selecionado')
      .forEach(x => x.classList.remove('selecionado'));
  });
}

function mostrarPainelExistentes(checklists, params, el) {
  const painel = document.getElementById('painel-conteudo');
  const titulo = obterTituloLocal(params, el);
  let html = `<h3>${titulo}</h3>`;
  html += `<a href="/checklist/novo?${params}" class="btn-novo-checklist">+ Novo Checklist</a>`;
  html += '<ul class="lista-checklists">';
  checklists.forEach(c => {
    html += `<li><div class="checklist-lista-item">
      <span class="data">${c.data_vistoria || 'sem data'}</span>
      ${badgeHtml(c.resultado)}
      <span class="resp">${c.responsavel_ude || ''}</span>
      ${!c.finalizado ? '<span class="rascunho-tag">(rascunho)</span>' : ''}
      <div class="acoes">
        <a href="/checklist/${c.id}">👁 Ver</a>
        <a href="/api/checklist/${c.id}/pdf" target="_blank">📥 PDF</a>
        <a href="/checklist/${c.id}/editar">✏ Editar</a>
      </div>
    </div></li>`;
  });
  html += '</ul>';
  painel.innerHTML = html;
  document.getElementById('painel-lateral').classList.add('aberto');
}

function mostrarPainelVazio(params, el) {
  const painel = document.getElementById('painel-conteudo');
  const titulo = obterTituloLocal(params, el);
  painel.innerHTML = `
    <h3>${titulo}</h3>
    <p class="sem-checklist">Nenhum checklist registrado para este local.</p>
    <a href="/checklist/novo?${params}" class="btn-novo-checklist">+ Criar Checklist</a>`;
  document.getElementById('painel-lateral').classList.add('aberto');
}

function badgeHtml(resultado) {
  const cores = {
    'APROVADO': '#22c55e', 'APROVADO COM RESSALVAS': '#f59e0b',
    'REPROVADO': '#ef4444', 'PENDENTE': '#94a3b8'
  };
  return `<span class="badge" style="background:${cores[resultado]||'#94a3b8'}">${resultado||'PENDENTE'}</span>`;
}

function obterTituloLocal(params, el) {
  const quadra = params.get('quadra') || '';
  const lote = params.get('lote') || '';
  const rua = params.get('rua') || '';
  const eq = params.get('equipamento') || '';
  if (quadra && lote) return `Lote ${lote} — Quadra ${quadra}`;
  if (rua) return rua;
  if (eq) return eq.replace(/-/g, ' ').toUpperCase();
  if (el) {
    const g = el.closest('[data-equipamento]');
    if (g) return g.getAttribute('data-equipamento').replace(/-/g, ' ').toUpperCase();
  }
  const tipo = params.get('tipo') || '';
  return tipo.charAt(0).toUpperCase() + tipo.slice(1);
}
