// Mapeamento: texto no SVG → dados do equipamento
// relativeTo: posiciona o círculo com offset em relação ao marcador de outro tipo
const EQUIP_TEXTOS = {
  'GUARITA':           { tipo: 'guarita',           label: 'GUARITA',           equipamento: 'guarita'           },
  'DEP. LIXO':         { tipo: 'dep_lixo',          label: 'DEP. LIXO',         equipamento: 'deposito-lixo',    relativeTo: 'guarita', offsetX: 26, offsetY: 0 },
  'SALÃO DE FESTAS':   { tipo: 'salao',             label: 'SALÃO DE FESTAS',   equipamento: 'salao-festas'      },
  'DECK PISCINAS':     { tipo: 'deck',              label: 'DECK PISCINAS',     equipamento: 'deck-piscina'      },
  'QUIOSQUES':         { tipo: 'quiosque',          label: 'QUIOSQUES',         equipamento: 'quiosque'          },
  'PLAYGROUND':        { tipo: 'parque',            label: 'PARQUE',            equipamento: 'parque-playground' },
  'MINICAMPO':         { tipo: 'campo',             label: 'MINICAMPO',         equipamento: 'minicampo'         },
  'QUADRA ESPORTIVA':  { tipo: 'quadra_esportiva',  label: 'QUADRA ESPORTIVA',  equipamento: 'quadra-esportiva'  },
};

// Mapeamento quadra → label para interface
const QUADRAS_LABEL = {
  'A':'A','B':'B','C':'C','D':'D','E':'E','F':'F','G':'G','H':'H',
  'I':'I','J':'J','K':'K','L':'L','M':'M','N':'N','O':'O','P':'P',
  'Q':'Q','R':'R','S':'S','T':'T'
};

// Tipos de checklist disponíveis por rua (label exibido + tipo interno)
const TIPOS_RUA = [
  { tipo: 'pavimentacao', label: 'Pavimentação', icone: '🛤' },
  { tipo: 'passeio',      label: 'Passeio',      icone: '🚶' },
  { tipo: 'saa',          label: 'Água (SAA)',   icone: '💧' },
  { tipo: 'drenagem',     label: 'Drenagem',     icone: '🌊' },
  { tipo: 'ses',          label: 'Esgoto (SES)', icone: '⬇' },
];

let SVG_EL = null;
const loteMap = {};  // svgId → { nr, quadra }
let _zoomTouchMoved = false;  // flag para distinguir tap de pan no mapa

// ViewBox atual exposto para conversão de coordenadas (atualizado por inicializarZoom)
let _viewBox = { x: 0, y: 0, w: 1, h: 1 };

function screenToSvg(clientX, clientY) {
  const r = document.getElementById('svg-viewport').getBoundingClientRect();
  return {
    x: _viewBox.x + (clientX - r.left) / r.width  * _viewBox.w,
    y: _viewBox.y + (clientY - r.top)  / r.height * _viewBox.h,
  };
}

function svgToScreen(svgX, svgY) {
  const r = document.getElementById('svg-viewport').getBoundingClientRect();
  return {
    left: r.left + (svgX - _viewBox.x) / _viewBox.w * r.width,
    top:  r.top  + (svgY - _viewBox.y) / _viewBox.h * r.height,
  };
}

// ── Modo Anotação ─────────────────────────────────────────────────────────────
let _annotationMode = false;
let _balaoState = { mode: 'new', anotacaoId: null, svgX: 0, svgY: 0, rua: '', fotoFile: null };

function toggleAnnotationMode() {
  _annotationMode = !_annotationMode;
  const btn = document.getElementById('btn-anotar');
  const viewport = document.getElementById('svg-viewport');
  const svgMapa = document.getElementById('svg-mapa');
  if (_annotationMode) {
    btn.classList.add('ativo');
    btn.textContent = '📌 Clique no mapa para anotar';
    if (viewport) viewport.style.cursor = 'crosshair';
    if (svgMapa) svgMapa.style.outline = '3px solid #F59E0B';
  } else {
    btn.classList.remove('ativo');
    btn.innerHTML = '&#128204; Anotar Dano';
    if (viewport) viewport.style.cursor = '';
    if (svgMapa) svgMapa.style.outline = '';
    fecharBalao();
  }
}

document.addEventListener('DOMContentLoaded', async function () {
  document.getElementById('btn-anotar')?.addEventListener('click', e => {
    e.stopPropagation();
    toggleAnnotationMode();
  });

  if (!SVG_DISPONIVEL) return;
  SVG_EL = await carregarSVG();
  if (!SVG_EL) return;

  processarCamadasSVG(SVG_EL);
  construirMapaLotes(SVG_EL);
  await carregarStatus();
  adicionarMarcadoresEquipamentos(SVG_EL);
  construirMapaRuas(SVG_EL);
  registrarEventosMapa();
  registrarFechaPanel();
  inicializarZoom();
  await carregarAnotacoes();
});

// ── Carrega o SVG via fetch + DOMParser ──
async function carregarSVG() {
  const container = document.getElementById('svg-container');
  try {
    const resp = await fetch('/static/svg/Rec_Oliveiras_1.svg');
    if (!resp.ok) throw new Error('SVG não encontrado');
    const texto = await resp.text();
    const parser = new DOMParser();
    const doc = parser.parseFromString(texto, 'image/svg+xml');
    const svgEl = doc.documentElement;
    if (svgEl.tagName === 'parsererror') throw new Error('SVG inválido');

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

// ── Constrói mapeamento SVG-id → { nr, quadra } usando posição espacial ──
function construirMapaLotes(svgEl) {
  // Coleta labels de lotes (g2055): cada element tem id e texto com nr do lote
  const loteLayer  = svgEl.getElementById('g3065');
  const labelLayer = svgEl.getElementById('g2055');
  const quadraLayer = svgEl.getElementById('g13051');
  if (!loteLayer || !labelLayer) return;

  // Monta array de labels { nr, cx, cy }
  const labels = [];
  Array.from(labelLayer.children).forEach(el => {
    const txt = el.textContent.trim();
    const nr = parseInt(txt, 10);
    if (isNaN(nr)) return;
    try {
      const bb = el.getBBox();
      labels.push({ nr: String(nr), cx: bb.x + bb.width / 2, cy: bb.y + bb.height / 2 });
    } catch (_) {}
  });

  // Monta array de quadras { quadra, cx, cy }
  const quadras = [];
  if (quadraLayer) {
    Array.from(quadraLayer.children).forEach(el => {
      const txt = el.textContent.trim();
      if (!txt) return;
      try {
        const bb = el.getBBox();
        quadras.push({ quadra: txt, cx: bb.x + bb.width / 2, cy: bb.y + bb.height / 2 });
      } catch (_) {}
    });
  }

  function nearest(arr, cx, cy) {
    let best = null, bestDist = Infinity;
    arr.forEach(item => {
      const d = (item.cx - cx) ** 2 + (item.cy - cy) ** 2;
      if (d < bestDist) { bestDist = d; best = item; }
    });
    return best;
  }

  // Para cada path de lote, encontra o label e quadra mais próximos
  Array.from(loteLayer.children).forEach(el => {
    try {
      const bb = el.getBBox();
      const cx = bb.x + bb.width / 2;
      const cy = bb.y + bb.height / 2;
      const lbl = nearest(labels, cx, cy);
      const qdr = nearest(quadras, cx, cy);
      if (lbl) {
        el.setAttribute('data-lote', lbl.nr);
        loteMap[el.id] = { nr: lbl.nr, quadra: qdr ? qdr.quadra : '' };
      }
      if (qdr) el.setAttribute('data-quadra', qdr.quadra);
    } catch (_) {}
  });
}

// Posições visuais das ruas (pré-calculadas com a matemática de rotação dos transforms do SVG)
// Formato: [cx, cy] em coordenadas do SVG
const RUA_POSICOES = {
  'RUA N.º 01':              [374, 274],
  'RUA N.º 02':              [603, 234],
  'RUA N.º 03':              [290, 511],
  'RUA N.º 04':              [677, 108],
  'RUA N.º 05':              [483, 252],
  'RUA N.º 06':              [244, 421],
  'RUA N.º 07':              [ 26, 597],
  'BV N.º 01':               [572, 195],
  'BV N.º 02':               [715, 161],
  'BV N.º 03':               [358, 347],
  'BV N.º 04':               [383, 383],
  'BV N.º 05':               [539, 341],
  'BV N.º 06':               [131, 508],
  'BV N.º 07':               [151, 548],
  'BV N.º 08':               [576, 184],
  'BV N.º 09':               [373, 352],
  'BV N.º 10':               [149, 508],
  'AVENIDA JOSIVALDO BARRETO':[732,  19],
};

// ── Constrói mapeamento rua → paths E adiciona marcadores clicáveis ──
function construirMapaRuas(svgEl) {
  // 1. Atribui data-rua às paths de pavimento por proximidade às posições conhecidas
  const labels = Object.entries(RUA_POSICOES).map(([rua, [cx, cy]]) => ({ rua, cx, cy }));

  function nearest(cx, cy) {
    let best = null, bestD = Infinity;
    labels.forEach(l => {
      const d = (l.cx - cx) ** 2 + (l.cy - cy) ** 2;
      if (d < bestD) { bestD = d; best = l; }
    });
    return best;
  }

  ['g7237', 'g4477'].forEach(layerId => {
    const layer = svgEl.getElementById(layerId);
    if (!layer) return;
    Array.from(layer.children).forEach(el => {
      try {
        const bb = el.getBBox();
        if (!bb || (bb.width === 0 && bb.height === 0)) return;
        const cx = bb.x + bb.width / 2;
        const cy = bb.y + bb.height / 2;
        const lbl = nearest(cx, cy);
        if (lbl) el.setAttribute('data-rua', lbl.rua);
      } catch (_) {}
    });
  });

  // 2. Cria marcadores visíveis e clicáveis para cada rua
  adicionarMarcadoresRuas(svgEl, labels);
}

// ── Marcadores clicáveis de rua (pílulas com nome) ──
function adicionarMarcadoresRuas(svgEl, labels) {
  labels.forEach(({ rua, cx, cy }) => {
    const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    g.setAttribute('class', 'clicavel rua marcador-rua');
    g.setAttribute('data-tipo', 'rua');
    g.setAttribute('data-rua', rua);
    g.style.cursor = 'pointer';

    const isBv = rua.startsWith('BV');
    const fillColor = isBv ? '#1B5E5A' : '#1B3C6B';
    const labelCurto = rua.replace('N.º ', '').replace('AVENIDA JOSIVALDO BARRETO', 'AVENIDA');

    // Pílula de fundo
    const pill = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    const pw = labelCurto.length * 4.5 + 10;
    const ph = 12;
    pill.setAttribute('x', cx - pw / 2);
    pill.setAttribute('y', cy - ph / 2);
    pill.setAttribute('width', pw);
    pill.setAttribute('height', ph);
    pill.setAttribute('rx', 6);
    pill.setAttribute('fill', fillColor);
    pill.setAttribute('fill-opacity', '0.85');
    pill.setAttribute('stroke', '#fff');
    pill.setAttribute('stroke-width', '1');

    // Texto da pílula
    const txt = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    txt.setAttribute('x', cx);
    txt.setAttribute('y', cy + 4);
    txt.setAttribute('text-anchor', 'middle');
    txt.setAttribute('font-size', '6');
    txt.setAttribute('font-family', 'Helvetica, Arial, sans-serif');
    txt.setAttribute('font-weight', 'bold');
    txt.setAttribute('fill', '#fff');
    txt.setAttribute('pointer-events', 'none');
    txt.textContent = labelCurto;

    g.appendChild(pill);
    g.appendChild(txt);
    svgEl.appendChild(g);
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

// ── Marcadores de equipamentos posicionados pelos textos reais do SVG ──
function adicionarMarcadoresEquipamentos(svgEl) {
  const textEls = Array.from(svgEl.querySelectorAll('text, tspan'));

  // Primeiro passo: posiciona todos que não dependem de outro marcador
  // e guarda as posições para uso por relativeTo
  const posicoes = {}; // tipo → { tx, ty }

  // Ordem: primeiro independentes, depois dependentes
  const independentes = Object.values(EQUIP_TEXTOS).filter(eq => !eq.relativeTo);
  const dependentes   = Object.values(EQUIP_TEXTOS).filter(eq =>  eq.relativeTo);

  // Mapeia chave de texto → eq para busca rápida
  const textoParaEq = {};
  Object.entries(EQUIP_TEXTOS).forEach(([k, v]) => { textoParaEq[k] = v; });

  independentes.forEach(eq => {
    const chave = Object.keys(textoParaEq).find(k => textoParaEq[k] === eq);
    const textEl = textEls.find(el => el.textContent.trim() === chave);
    if (!textEl) return;
    let bbox;
    try { bbox = textEl.getBBox(); } catch (_) { return; }
    const tx = bbox.x + bbox.width / 2;
    const ty = bbox.y + bbox.height / 2;
    posicoes[eq.tipo] = { tx, ty };
    _criarMarcador(svgEl, eq, tx, ty);
  });

  dependentes.forEach(eq => {
    const ref = posicoes[eq.relativeTo];
    if (!ref) return;
    const tx = ref.tx + (eq.offsetX || 0);
    const ty = ref.ty + (eq.offsetY || 0);
    posicoes[eq.tipo] = { tx, ty };
    _criarMarcador(svgEl, eq, tx, ty);
  });
}

function _criarMarcador(svgEl, eq, tx, ty) {
  const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  g.setAttribute('class', 'clicavel equipamento');
  g.setAttribute('data-tipo', eq.tipo);
  g.setAttribute('data-equipamento', eq.equipamento);
  g.style.cursor = 'pointer';

  const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
  circle.setAttribute('cx', tx);
  circle.setAttribute('cy', ty);
  circle.setAttribute('r', 12);
  circle.setAttribute('fill', '#5C1A2E');
  circle.setAttribute('fill-opacity', '0.88');
  circle.setAttribute('stroke', '#fff');
  circle.setAttribute('stroke-width', '2');

  const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
  label.setAttribute('x', tx);
  label.setAttribute('y', ty - 15);
  label.setAttribute('text-anchor', 'middle');
  label.setAttribute('font-size', '7');
  label.setAttribute('font-family', 'Helvetica, Arial, sans-serif');
  label.setAttribute('fill', '#1e293b');
  label.setAttribute('font-weight', 'bold');
  label.setAttribute('pointer-events', 'none');
  label.textContent = eq.label;

  g.appendChild(circle);
  g.appendChild(label);
  svgEl.appendChild(g);
}

// ── Eventos de clique no mapa ──
function registrarEventosMapa() {
  const area = document.getElementById('svg-mapa');
  area.addEventListener('click', async function (e) {
    if (_zoomTouchMoved) { _zoomTouchMoved = false; return; }

    // Clique em pin de anotação existente
    const pinEl = e.target.closest('.pin-anotacao');
    if (pinEl) {
      const id    = parseInt(pinEl.getAttribute('data-aid'));
      const texto = pinEl.getAttribute('data-texto') || '';
      const foto  = pinEl.getAttribute('data-foto') || '';
      const rua   = pinEl.getAttribute('data-rua') || '';
      abrirBalaoVerPin(e.clientX, e.clientY, id, texto, foto, rua);
      return;
    }

    // Modo anotação: clique em QUALQUER lugar do SVG cria pin
    if (_annotationMode) {
      // Ignorar cliques nos botões de zoom/toolbar
      if (e.target.closest('#zoom-controls') || e.target.closest('.mapa-toolbar-bottom')) return;
      // Deve estar dentro do viewport do SVG
      const vp = document.getElementById('svg-viewport');
      if (!vp || !vp.contains(e.target)) return;
      const el = e.target.closest('.clicavel');
      const rua = el ? (el.getAttribute('data-rua') || '') : '';
      const pt  = screenToSvg(e.clientX, e.clientY);
      abrirBalaoNovo(e.clientX, e.clientY, pt.x, pt.y, rua);
      return;
    }

    const el = e.target.closest('.clicavel');
    if (!el) return;

    const tipo = el.getAttribute('data-tipo');

    document.querySelectorAll('.clicavel.selecionado')
      .forEach(x => x.classList.remove('selecionado'));
    el.classList.add('selecionado');

    if (tipo === 'lote') {
      await abrirPainelLote(el);
    } else if (tipo === 'rua' || tipo === 'passeio') {
      await abrirPainelRua(el);
    } else {
      await abrirPainelGenerico(el, tipo);
    }
  });
}

// ── Painel específico para lotes ──
async function abrirPainelLote(el) {
  const quadra = el.getAttribute('data-quadra') || '';
  const lote   = el.getAttribute('data-lote')   || '';
  const painel = document.getElementById('painel-conteudo');

  // Cabeçalho sempre visível com identificação
  const temId = quadra || lote;
  const titulo = temId
    ? `Lote ${lote}${quadra ? ' — Quadra ' + quadra : ''}`
    : 'Lote (identificação pendente)';

  painel.innerHTML = `
    <h3 class="painel-titulo-lote">${titulo}</h3>
    <div class="lote-acoes">
      <a href="/checklist/novo?tipo=lote${quadra ? '&quadra='+quadra : ''}${lote ? '&lote='+lote : ''}"
         class="btn-acao btn-acao-novo">
        <span class="acao-icone">＋</span>
        <span>Novo Checklist</span>
      </a>
      <button class="btn-acao btn-acao-ver" id="btn-ver-checklists">
        <span class="acao-icone">📋</span>
        <span>Ver Checklists</span>
      </button>
    </div>
    <div id="lote-status-area">
      <div class="lote-carregando">Carregando…</div>
    </div>`;

  document.getElementById('painel-lateral').classList.add('aberto');

  // Busca checklists do lote
  const params = new URLSearchParams({ tipo: 'lote' });
  if (quadra) params.set('quadra', quadra);
  if (lote)   params.set('lote', lote);

  let checklists = [];
  try {
    const resp = await fetch('/api/mapa/status?' + params);
    const data = await resp.json();
    checklists = data.checklists || [];
  } catch (_) {}

  // Renderiza status do lote
  const statusArea = document.getElementById('lote-status-area');
  if (checklists.length === 0) {
    statusArea.innerHTML = `<p class="sem-checklist">Nenhum checklist registrado para este lote.</p>`;
  } else {
    // Badge de status consolidado
    const ultimo = checklists[0];
    statusArea.innerHTML = `
      <div class="lote-status-badge">
        ${badgeHtml(ultimo.resultado)}
        <span class="status-data">${ultimo.data_vistoria || '—'}</span>
      </div>
      <div id="lista-checklists-lote" style="display:none">
        ${checklists.map(c => itemChecklistHtml(c)).join('')}
      </div>`;
  }

  // Toggle "Ver checklists"
  const btnVer = document.getElementById('btn-ver-checklists');
  if (btnVer) {
    const listaEl = document.getElementById('lista-checklists-lote');
    btnVer.addEventListener('click', () => {
      if (!listaEl) return;
      const aberto = listaEl.style.display !== 'none';
      listaEl.style.display = aberto ? 'none' : 'block';
      btnVer.querySelector('span:last-child').textContent = aberto ? 'Ver Checklists' : 'Ocultar';
    });
  }
}

// ── Painel de rua — múltiplos tipos de checklist ──
async function abrirPainelRua(el) {
  const rua = el.getAttribute('data-rua') || el.closest('[data-rua]')?.getAttribute('data-rua') || '';
  const isBv = rua.startsWith('BV');
  const painel = document.getElementById('painel-conteudo');

  // Tipos aplicáveis: BV tem passeio; ruas normais têm pavimentação, SAA, drenagem, SES
  const tiposAplicaveis = isBv
    ? TIPOS_RUA.filter(t => ['pavimentacao','passeio','saa','drenagem','ses'].includes(t.tipo))
    : TIPOS_RUA;

  painel.innerHTML = `
    <h3 class="painel-titulo-lote">${rua || 'Rua'}</h3>
    <p class="rua-subtitulo">Novo checklist para esta rua:</p>
    <div class="rua-tipos-grid">
      ${tiposAplicaveis.map(t => `
        <a href="/checklist/novo?tipo=${t.tipo}${rua ? '&rua=' + encodeURIComponent(rua) : ''}"
           class="btn-tipo-rua">
          <span class="tipo-icone">${t.icone}</span>
          <span>${t.label}</span>
        </a>`).join('')}
    </div>
    <div id="rua-checklists-area">
      <div class="lote-carregando">Carregando checklists…</div>
    </div>`;

  document.getElementById('painel-lateral').classList.add('aberto');

  // Busca todos os checklists desta rua (todos os tipos)
  if (!rua) {
    document.getElementById('rua-checklists-area').innerHTML =
      '<p class="sem-checklist">Rua não identificada.</p>';
    return;
  }

  let todos = [];
  try {
    const resp = await fetch('/api/mapa/status?' + new URLSearchParams({ rua }));
    todos = (await resp.json()).checklists || [];
  } catch (_) {}

  const area = document.getElementById('rua-checklists-area');
  if (todos.length === 0) {
    area.innerHTML = '<p class="sem-checklist">Nenhum checklist registrado para esta rua.</p>';
    return;
  }

  // Agrupa por tipo
  const grupos = {};
  todos.forEach(c => {
    if (!grupos[c.tipo]) grupos[c.tipo] = [];
    grupos[c.tipo].push(c);
  });

  const tipoLabel = { pavimentacao:'Pavimentação', passeio:'Passeio', saa:'SAA',
                      drenagem:'Drenagem', ses:'SES' };
  let html = '<div class="rua-grupos">';
  Object.entries(grupos).forEach(([tipo, lista]) => {
    html += `<div class="rua-grupo">
      <div class="rua-grupo-titulo">${tipoLabel[tipo] || tipo}</div>
      ${lista.map(c => itemChecklistHtml(c)).join('')}
    </div>`;
  });
  html += '</div>';
  area.innerHTML = html;
}

// ── Painel genérico (equipamento) ──
async function abrirPainelGenerico(el, tipo) {
  const eq = el.getAttribute('data-equipamento') || el.closest('[data-equipamento]')?.getAttribute('data-equipamento');
  const params = new URLSearchParams({ tipo });
  if (eq) params.set('equipamento', eq);

  const resp = await fetch('/api/mapa/status?' + params);
  const data = await resp.json();
  const checklists = data.checklists || [];
  const titulo = eq ? eq.replace(/-/g, ' ').toUpperCase() : tipo.toUpperCase();
  const painel = document.getElementById('painel-conteudo');

  let html = `<h3>${titulo}</h3>
    <a href="/checklist/novo?${params}" class="btn-novo-checklist">+ Novo Checklist</a>`;

  if (checklists.length > 0) {
    html += '<ul class="lista-checklists">';
    checklists.forEach(c => { html += `<li>${itemChecklistHtml(c)}</li>`; });
    html += '</ul>';
  } else {
    html += `<p class="sem-checklist">Nenhum checklist registrado para este local.</p>`;
  }

  painel.innerHTML = html;
  document.getElementById('painel-lateral').classList.add('aberto');
}

function itemChecklistHtml(c) {
  return `<div class="checklist-lista-item">
    <span class="data">${c.data_vistoria || 'sem data'}</span>
    ${badgeHtml(c.resultado)}
    <span class="resp">${c.responsavel_ude || ''}</span>
    ${!c.finalizado ? '<span class="rascunho-tag">(rascunho)</span>' : ''}
    <div class="acoes">
      <a href="/checklist/${c.id}">👁 Ver</a>
      <a href="/api/checklist/${c.id}/pdf" target="_blank">📥 PDF</a>
      <a href="/checklist/${c.id}/editar">✏ Editar</a>
    </div>
  </div>`;
}

function registrarFechaPanel() {
  document.getElementById('painel-fechar').addEventListener('click', () => {
    document.getElementById('painel-lateral').classList.remove('aberto');
    document.querySelectorAll('.clicavel.selecionado')
      .forEach(x => x.classList.remove('selecionado'));
  });
}

function badgeHtml(resultado) {
  const cores = {
    'APROVADO': '#22c55e',
    'APROVADO COM RESSALVAS': '#f59e0b',
    'REPROVADO': '#ef4444',
    'PENDENTE': '#94a3b8'
  };
  return `<span class="badge" style="background:${cores[resultado] || '#94a3b8'}">${resultado || 'PENDENTE'}</span>`;
}

// ── Anotações no mapa ─────────────────────────────────────────────────────────

async function carregarAnotacoes() {
  try {
    const resp = await fetch('/api/mapa/anotacoes');
    const lista = await resp.json();
    lista.forEach(a => renderizarPin(a));
  } catch (e) {
    console.warn('Erro ao carregar anotações:', e);
  }
}

function renderizarPin(a) {
  if (!SVG_EL) return;
  const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  g.setAttribute('class', 'pin-anotacao');
  g.setAttribute('data-aid', a.id);
  g.setAttribute('data-texto', a.texto || '');
  g.setAttribute('data-foto', a.foto_caminho || '');
  g.setAttribute('data-rua', a.rua || '');
  g.style.cursor = 'pointer';

  const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
  circle.setAttribute('cx', a.svg_x);
  circle.setAttribute('cy', a.svg_y);
  circle.setAttribute('r', 5);
  circle.setAttribute('fill', '#F59E0B');
  circle.setAttribute('stroke', '#fff');
  circle.setAttribute('stroke-width', '1.5');

  const icon = document.createElementNS('http://www.w3.org/2000/svg', 'text');
  icon.setAttribute('x', a.svg_x);
  icon.setAttribute('y', a.svg_y + 2.5);
  icon.setAttribute('text-anchor', 'middle');
  icon.setAttribute('font-size', '5');
  icon.setAttribute('pointer-events', 'none');
  icon.textContent = '!';
  icon.setAttribute('fill', '#fff');
  icon.setAttribute('font-weight', 'bold');

  g.appendChild(circle);
  g.appendChild(icon);
  SVG_EL.appendChild(g);
  return g;
}

function posicionarBalao(clientX, clientY) {
  const balao = document.getElementById('balao-anotacao');
  balao.style.display = 'block';
  const bw = 272, bh = 260;
  let left = clientX + 14;
  let top  = clientY - 20;
  if (left + bw > window.innerWidth)  left = clientX - bw - 14;
  if (top  + bh > window.innerHeight) top  = clientY - bh;
  if (top < 0) top = 4;
  if (left < 0) left = 4;
  balao.style.left = left + 'px';
  balao.style.top  = top  + 'px';
}

function abrirBalaoNovo(clientX, clientY, svgX, svgY, rua) {
  _balaoState = { mode: 'new', anotacaoId: null, svgX, svgY, rua, fotoFile: null };
  document.getElementById('balao-titulo').textContent = 'Nova Anotação';
  document.getElementById('balao-rua-label').textContent = rua || 'Rua não identificada';
  document.getElementById('balao-texto').value = '';
  document.getElementById('balao-foto-preview').style.display = 'none';
  document.getElementById('balao-foto-input').value = '';
  document.getElementById('balao-modo-ver').style.display = 'none';
  document.getElementById('balao-texto').style.display = '';
  document.getElementById('balao-btn-salvar').style.display = '';
  document.querySelector('.btn-foto-balao').style.display = '';
  posicionarBalao(clientX, clientY);
}

function abrirBalaoVerPin(clientX, clientY, id, texto, fotoCaminho, rua) {
  _balaoState = { mode: 'view', anotacaoId: id, svgX: 0, svgY: 0, rua, fotoFile: null };
  document.getElementById('balao-titulo').textContent = `Anotação #${id}`;
  document.getElementById('balao-rua-label').textContent = rua || '';
  document.getElementById('balao-view-texto').textContent = texto || '(sem texto)';

  const fotoVer = document.getElementById('balao-view-foto');
  if (fotoCaminho) {
    fotoVer.src = `/fotos/${fotoCaminho}`;
    fotoVer.style.display = 'block';
  } else {
    fotoVer.style.display = 'none';
  }

  document.getElementById('balao-modo-ver').style.display = 'block';
  document.getElementById('balao-texto').style.display = 'none';
  document.getElementById('balao-btn-salvar').style.display = 'none';
  document.querySelector('.btn-foto-balao').style.display = 'none';
  document.getElementById('balao-foto-preview').style.display = 'none';
  posicionarBalao(clientX, clientY);
}

function balaoModoEditar() {
  const id = _balaoState.anotacaoId;
  const texto = document.getElementById('balao-view-texto').textContent;
  _balaoState.mode = 'edit';
  document.getElementById('balao-titulo').textContent = `Editar Anotação #${id}`;
  document.getElementById('balao-texto').value = texto === '(sem texto)' ? '' : texto;
  document.getElementById('balao-texto').style.display = '';
  document.getElementById('balao-btn-salvar').style.display = '';
  document.querySelector('.btn-foto-balao').style.display = '';
  document.getElementById('balao-modo-ver').style.display = 'none';
}

function fecharBalao() {
  document.getElementById('balao-anotacao').style.display = 'none';
  _balaoState.fotoFile = null;
}

function balaoFotoSelecionada(input) {
  const file = input.files[0];
  if (!file) return;
  _balaoState.fotoFile = file;
  const preview = document.getElementById('balao-foto-preview');
  preview.src = URL.createObjectURL(file);
  preview.style.display = 'block';
}

async function salvarAnotacao() {
  const texto = document.getElementById('balao-texto').value.trim();
  const { mode, anotacaoId, svgX, svgY, rua, fotoFile } = _balaoState;

  let id = anotacaoId;

  if (mode === 'new') {
    const resp = await fetch('/api/mapa/anotacoes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ rua, svg_x: svgX, svg_y: svgY, texto })
    });
    const data = await resp.json();
    id = data.id;
    renderizarPin({ id, svg_x: svgX, svg_y: svgY, texto, foto_caminho: '', rua });
  } else {
    await fetch(`/api/mapa/anotacoes/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ texto })
    });
    // Atualiza atributos do pin existente
    const pin = SVG_EL?.querySelector(`.pin-anotacao[data-aid="${id}"]`);
    if (pin) pin.setAttribute('data-texto', texto);
  }

  if (fotoFile && id) {
    const fd = new FormData();
    fd.append('file', fotoFile);
    const r = await fetch(`/api/mapa/anotacoes/${id}/foto`, { method: 'POST', body: fd });
    const d = await r.json();
    const pin = SVG_EL?.querySelector(`.pin-anotacao[data-aid="${id}"]`);
    if (pin && d.caminho) pin.setAttribute('data-foto', d.caminho);
  }

  fecharBalao();
}

async function excluirAnotacao() {
  const id = _balaoState.anotacaoId;
  if (!id || !confirm('Excluir esta anotação?')) return;
  await fetch(`/api/mapa/anotacoes/${id}`, { method: 'DELETE' });
  SVG_EL?.querySelector(`.pin-anotacao[data-aid="${id}"]`)?.remove();
  fecharBalao();
}

// ── Zoom e Pan do mapa via viewBox — renderiza nítido em qualquer zoom ──
function inicializarZoom() {
  const viewport = document.getElementById('svg-viewport');
  const container = document.getElementById('svg-container');
  if (!viewport || !SVG_EL) return;

  const svg = SVG_EL;
  const vb0 = (svg.getAttribute('viewBox') || '').split(/[\s,]+/).map(Number);
  if (vb0.length < 4) return;

  const [ox, oy, ow, oh] = vb0;
  let vx = ox, vy = oy, vw = ow, vh = oh;
  const MAX_ZOOM = 12;  // viewBox pode encolher até 1/12 do original

  function applyVB() {
    _viewBox = { x: vx, y: vy, w: vw, h: vh };
    svg.setAttribute('viewBox', `${vx} ${vy} ${vw} ${vh}`);
  }

  function clamp() {
    vx = Math.max(ox, Math.min(ox + ow - vw, vx));
    vy = Math.max(oy, Math.min(oy + oh - vh, vy));
  }

  // Converte coordenada de client (px) para coordenada SVG aproximada
  function c2s(clientX, clientY) {
    const r = viewport.getBoundingClientRect();
    return {
      x: vx + (clientX - r.left) / r.width  * vw,
      y: vy + (clientY - r.top)  / r.height * vh,
    };
  }

  // Zoom centrado em (clientX, clientY); factor > 1 = aproximar
  function zoomAt(factor, clientX, clientY) {
    const p = c2s(clientX, clientY);
    const newVw = Math.max(ow / MAX_ZOOM, Math.min(ow, vw / factor));
    const ratio = newVw / vw;
    vx = p.x - ratio * (p.x - vx);
    vy = p.y - ratio * (p.y - vy);
    vw = newVw;
    vh = oh * (vw / ow);
    if (vw >= ow * 0.99) { vw = ow; vh = oh; vx = ox; vy = oy; }
    else clamp();
    applyVB();
  }

  function panByPx(dxPx, dyPx) {
    if (vw >= ow * 0.99) return;
    const r = viewport.getBoundingClientRect();
    vx -= dxPx / r.width  * vw;
    vy -= dyPx / r.height * vh;
    clamp();
    applyVB();
  }

  // ── Botões ──
  document.getElementById('btn-zoom-in')?.addEventListener('click', e => {
    e.stopPropagation();
    const r = viewport.getBoundingClientRect();
    zoomAt(1.8, r.left + r.width / 2, r.top + r.height / 2);
  });
  document.getElementById('btn-zoom-out')?.addEventListener('click', e => {
    e.stopPropagation();
    const r = viewport.getBoundingClientRect();
    zoomAt(1 / 1.8, r.left + r.width / 2, r.top + r.height / 2);
  });
  document.getElementById('btn-zoom-reset')?.addEventListener('click', e => {
    e.stopPropagation();
    vw = ow; vh = oh; vx = ox; vy = oy; applyVB();
  });

  // ── Mouse wheel (desktop) ──
  viewport.addEventListener('wheel', e => {
    e.preventDefault();
    zoomAt(e.deltaY < 0 ? 1.15 : 1 / 1.15, e.clientX, e.clientY);
  }, { passive: false });

  // ── Mouse drag (desktop) ──
  let mdDown = false, mdX = 0, mdY = 0;
  viewport.addEventListener('mousedown', e => {
    if (e.button !== 0) return;
    mdDown = true; mdX = e.clientX; mdY = e.clientY;
    container.classList.add('grabbing');
  });
  window.addEventListener('mousemove', e => {
    if (!mdDown) return;
    panByPx(e.clientX - mdX, e.clientY - mdY);
    mdX = e.clientX; mdY = e.clientY;
  });
  window.addEventListener('mouseup', () => {
    mdDown = false;
    container.classList.remove('grabbing');
  });

  // ── Touch: pinch-to-zoom + pan (mobile) ──
  let t0 = null, touchMoves = 0;

  viewport.addEventListener('touchstart', e => {
    _zoomTouchMoved = false;
    touchMoves = 0;
    const r = viewport.getBoundingClientRect();
    t0 = {
      touches: Array.from(e.touches).map(t => ({ id: t.identifier, cx: t.clientX, cy: t.clientY })),
      vx, vy, vw, vh,
      ...(e.touches.length === 2 && {
        dist: Math.hypot(
          e.touches[0].clientX - e.touches[1].clientX,
          e.touches[0].clientY - e.touches[1].clientY),
        midX: (e.touches[0].clientX + e.touches[1].clientX) / 2,
        midY: (e.touches[0].clientY + e.touches[1].clientY) / 2,
      }),
    };
  }, { passive: true });

  viewport.addEventListener('touchmove', e => {
    touchMoves++;
    if (touchMoves > 2) _zoomTouchMoved = true;
    if (!t0) return;
    const r = viewport.getBoundingClientRect();

    if (e.touches.length === 2 && t0.dist) {
      e.preventDefault();
      const curDist = Math.hypot(
        e.touches[0].clientX - e.touches[1].clientX,
        e.touches[0].clientY - e.touches[1].clientY);
      const curMidX = (e.touches[0].clientX + e.touches[1].clientX) / 2;
      const curMidY = (e.touches[0].clientY + e.touches[1].clientY) / 2;
      const factor = curDist / t0.dist;

      // Zoom absoluto a partir do estado inicial (sem acúmulo de erro)
      const newVw = Math.max(ow / MAX_ZOOM, Math.min(ow, t0.vw / factor));
      const ratio = newVw / t0.vw;
      // Pivô: ponto SVG sob o centro inicial da pinça
      const pivX = t0.vx + (t0.midX - r.left) / r.width  * t0.vw;
      const pivY = t0.vy + (t0.midY - r.top)  / r.height * t0.vh;
      vx = pivX - ratio * (pivX - t0.vx);
      vy = pivY - ratio * (pivY - t0.vy);
      vw = newVw;
      vh = oh * (vw / ow);
      if (vw >= ow * 0.99) { vw = ow; vh = oh; vx = ox; vy = oy; }
      else {
        // Pan pela diferença de centro da pinça
        vx -= (curMidX - t0.midX) / r.width  * vw;
        vy -= (curMidY - t0.midY) / r.height * vh;
        clamp();
      }
      applyVB();

    } else if (e.touches.length === 1 && vw < ow * 0.99) {
      e.preventDefault();
      const t = t0.touches.find(t => t.id === e.touches[0].identifier);
      if (t) {
        // Pan absoluto a partir do estado inicial do toque
        vx = t0.vx - (e.touches[0].clientX - t.cx) / r.width  * t0.vw;
        vy = t0.vy - (e.touches[0].clientY - t.cy) / r.height * t0.vh;
        clamp();
        applyVB();
      }
    }
  }, { passive: false });

  viewport.addEventListener('touchend', e => {
    // Recalibra estado inicial para os toques restantes
    if (e.touches.length > 0) {
      t0 = {
        touches: Array.from(e.touches).map(t => ({ id: t.identifier, cx: t.clientX, cy: t.clientY })),
        vx, vy, vw, vh,
      };
    } else {
      t0 = null;
    }
  }, { passive: true });
}
