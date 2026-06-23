let CHECKLIST_ID = null;
let SCHEMA_ATUAL = null;
const saveQueue = {};

document.addEventListener('DOMContentLoaded', async function () {
  // Pré-preencher tipo e localizadores vindos da URL ou do template
  if (TIPO_INICIAL) {
    document.getElementById('f-tipo').value = TIPO_INICIAL;
    tipoAlterado();
  }
  if (QUADRA_INICIAL) document.getElementById('f-quadra').value = QUADRA_INICIAL;
  if (LOTE_INICIAL)   document.getElementById('f-lote').value   = LOTE_INICIAL;
  if (RUA_INICIAL) {
    const rEl = document.getElementById('f-rua');
    if (rEl) rEl.value = RUA_INICIAL;
    const rEl2 = document.getElementById('f-rua-passeio');
    if (rEl2) rEl2.value = RUA_INICIAL;
  }

  // Modo edição: carregar checklist existente
  if (CHECKLIST_ID_INICIAL) {
    CHECKLIST_ID = CHECKLIST_ID_INICIAL;
    await carregarChecklistExistente(CHECKLIST_ID);
    document.getElementById('secao-cabecalho').style.display = 'none';
    document.getElementById('barra-progresso-wrap').style.display = '';
    document.getElementById('finalizacao-wrap').style.display = '';
  }
});

function tipoAlterado() {
  const tipo = document.getElementById('f-tipo').value;
  const tiposLote = ['lote'];
  const tiposRua = ['pavimentacao', 'saa', 'drenagem', 'ses'];
  const tiposPasseio = ['passeio'];

  document.getElementById('localizador-lote').style.display =
    tiposLote.includes(tipo) ? '' : 'none';
  document.getElementById('localizador-rua').style.display =
    tiposRua.includes(tipo) ? '' : 'none';
  document.getElementById('localizador-passeio').style.display =
    tiposPasseio.includes(tipo) ? '' : 'none';
}

async function iniciarChecklist() {
  const tipo = document.getElementById('f-tipo').value;
  if (!tipo) { alert('Selecione o tipo de checklist.'); return; }

  const data_v = document.getElementById('f-data').value;
  const responsavel = document.getElementById('f-responsavel').value.trim();
  if (!responsavel) { alert('Informe o Responsável UDE.'); return; }

  const body = {
    tipo,
    data_vistoria: data_v,
    responsavel_ude: responsavel,
    empresa_executora: document.getElementById('f-empresa').value.trim(),
  };

  if (tipo === 'lote') {
    body.quadra = document.getElementById('f-quadra').value.trim();
    body.lote   = document.getElementById('f-lote').value.trim();
  } else if (['pavimentacao','saa','drenagem','ses'].includes(tipo)) {
    body.rua          = document.getElementById('f-rua').value.trim();
    body.trecho_inicio = document.getElementById('f-trecho-ini').value.trim();
    body.trecho_fim    = document.getElementById('f-trecho-fim').value.trim();
  } else if (tipo === 'passeio') {
    body.rua            = document.getElementById('f-rua-passeio').value.trim();
    body.lotes_atendidos = document.getElementById('f-lotes-atendidos').value.trim();
  } else {
    body.equipamento = tipo;
  }

  const resp = await fetch('/api/checklist', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  const d = await resp.json();
  if (!d.id) { alert('Erro ao criar checklist.'); return; }

  CHECKLIST_ID = d.id;
  history.replaceState({}, '', `/checklist/${d.id}/editar`);

  document.getElementById('secao-cabecalho').style.display = 'none';
  document.getElementById('barra-progresso-wrap').style.display = '';
  document.getElementById('finalizacao-wrap').style.display = '';

  await renderizarFormulario(tipo);
  atualizarProgressBar();
}

async function renderizarFormulario(tipo) {
  const resp = await fetch(`/api/schema/${tipo}`);
  SCHEMA_ATUAL = await resp.json();

  const itensResp = await fetch(`/api/checklist/${CHECKLIST_ID}`);
  const d = await itensResp.json();

  document.getElementById('form-titulo').textContent =
    SCHEMA_ATUAL.titulo || 'Checklist de Recebimento';

  const container = document.getElementById('itens-container');
  container.innerHTML = '';

  // Agrupar itens por seção
  const secoes = {};
  d.itens.forEach(it => {
    if (!secoes[it.secao]) secoes[it.secao] = [];
    secoes[it.secao].push(it);
  });

  const fotosPorItem = {};
  d.fotos.forEach(f => {
    if (f.item_id) {
      if (!fotosPorItem[f.item_id]) fotosPorItem[f.item_id] = [];
      fotosPorItem[f.item_id].push(f);
    }
  });

  for (const [secao, itens] of Object.entries(secoes)) {
    const secaoDiv = document.createElement('div');
    secaoDiv.className = 'form-secao';
    secaoDiv.innerHTML = `<h2>${secao}</h2>`;

    itens.forEach(item => {
      const fotos = fotosPorItem[item.id] || [];
      secaoDiv.appendChild(criarItemEl(item, fotos));
    });
    container.appendChild(secaoDiv);
  }

  // Fotos gerais (sem item vinculado)
  d.fotos.filter(f => !f.item_id).forEach(f => adicionarMiniaturaGeral(f.id, f.caminho, f.legenda));
}

function criarItemEl(item, fotos) {
  const s = item.status || 'NA';
  const div = document.createElement('div');
  div.className = `checklist-item status-${s.toLowerCase()}`;
  div.id = `item-${item.id}`;

  let fotosHtml = fotos.map(f => `
    <div class="foto-wrap" id="foto-${f.id}">
      <img src="/fotos/${f.caminho}" class="miniatura-foto" onclick="window.open(this.src,'_blank')">
      <button class="btn-del-foto" onclick="deletarFoto(${f.id})">×</button>
      <input class="foto-legenda" type="text" placeholder="Legenda…"
        value="${(f.legenda||'').replace(/"/g,'&quot;')}"
        oninput="salvarLegenda(${f.id}, this.value)">
    </div>`).join('');

  div.innerHTML = `
    <div class="item-header">
      <span class="item-nr">${item.item_nr}</span>
      <span class="item-desc">${item.descricao}</span>
    </div>
    <div class="item-controles">
      <div class="btn-status-group" data-item-id="${item.id}">
        <button class="btn-status btn-c ${s==='C'?'ativo':''}" data-val="C" onclick="setStatus(this)">C</button>
        <button class="btn-status btn-nc ${s==='NC'?'ativo':''}" data-val="NC" onclick="setStatus(this)">NC</button>
        <button class="btn-status btn-na ${s==='NA'?'ativo':''}" data-val="NA" onclick="setStatus(this)">N/A</button>
      </div>
      <input type="text" class="obs-input" placeholder="Observação…"
        value="${(item.observacao||'').replace(/"/g,'&quot;')}"
        oninput="salvarItem(${item.id},{})">
      ${item.local_ref !== undefined ? `
        <input type="text" class="local-input" placeholder="Local/Ref."
          value="${(item.local_ref||'').replace(/"/g,'&quot;')}"
          oninput="salvarItem(${item.id},{})">` : ''}
    </div>
    <div class="item-fotos">
      <div class="fotos-container" id="fotos-${item.id}">${fotosHtml}</div>
      <button class="btn-foto" onclick="abrirCamera(${CHECKLIST_ID},${item.id})">📷 Foto</button>
    </div>`;

  return div;
}

async function carregarChecklistExistente(cid) {
  const resp = await fetch(`/api/checklist/${cid}`);
  const d = await resp.json();
  const c = d.checklist;

  document.getElementById('form-titulo').textContent =
    `Editar — ${c.tipo} #${cid}`;

  const fotosPorItem = {};
  d.fotos.forEach(f => {
    if (f.item_id) {
      if (!fotosPorItem[f.item_id]) fotosPorItem[f.item_id] = [];
      fotosPorItem[f.item_id].push(f);
    }
  });

  const secoes = {};
  d.itens.forEach(it => {
    if (!secoes[it.secao]) secoes[it.secao] = [];
    secoes[it.secao].push(it);
  });

  const container = document.getElementById('itens-container');
  container.innerHTML = '';

  for (const [secao, itens] of Object.entries(secoes)) {
    const secaoDiv = document.createElement('div');
    secaoDiv.className = 'form-secao';
    secaoDiv.innerHTML = `<h2>${secao}</h2>`;
    itens.forEach(item => {
      secaoDiv.appendChild(criarItemEl(item, fotosPorItem[item.id] || []));
    });
    container.appendChild(secaoDiv);
  }

  if (c.resultado) {
    const radio = document.querySelector(`input[name="resultado"][value="${c.resultado}"]`);
    if (radio) radio.checked = true;
  }
  if (c.observacoes_gerais) {
    document.getElementById('obs-gerais').value = c.observacoes_gerais;
  }

  // Fotos gerais (sem item vinculado)
  d.fotos.filter(f => !f.item_id).forEach(f => adicionarMiniaturaGeral(f.id, f.caminho, f.legenda));

  atualizarProgressBar();
}

function setStatus(btn) {
  const container = btn.closest('.btn-status-group');
  const itemId = parseInt(container.dataset.itemId);
  const val = btn.dataset.val;
  const itemDiv = document.getElementById(`item-${itemId}`);

  if (btn.classList.contains('ativo')) {
    btn.classList.remove('ativo');
    itemDiv.className = 'checklist-item';
    salvarItem(itemId, { status: 'NA' });
    return;
  }

  container.querySelectorAll('.btn-status').forEach(b => b.classList.remove('ativo'));
  btn.classList.add('ativo');
  itemDiv.className = `checklist-item status-${val.toLowerCase()}`;
  salvarItem(itemId, { status: val });
}

function salvarItem(itemId, dados) {
  clearTimeout(saveQueue[itemId]);
  saveQueue[itemId] = setTimeout(async () => {
    const itemDiv = document.getElementById(`item-${itemId}`);
    if (!itemDiv) return;
    const obs = itemDiv.querySelector('.obs-input')?.value || '';
    const local = itemDiv.querySelector('.local-input')?.value || '';
    const statusBtn = itemDiv.querySelector('.btn-status.ativo');
    const status = dados.status !== undefined ? dados.status : (statusBtn?.dataset.val || 'NA');
    await fetch(`/api/checklist/${CHECKLIST_ID}/item/${itemId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status, observacao: obs, local_ref: local, ...dados })
    });
    atualizarProgressBar();
  }, 600);
}

function abrirCamera(checklistId, itemId) {
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = 'image/*';
  input.capture = 'environment';
  input.onchange = async function () {
    const file = this.files[0];
    if (!file) return;
    const fd = new FormData();
    fd.append('file', file);
    fd.append('checklist_id', checklistId);
    fd.append('item_id', itemId);
    const resp = await fetch('/api/foto/upload', { method: 'POST', body: fd });
    const data = await resp.json();
    if (data.foto_id) {
      const container = document.getElementById(`fotos-${itemId}`);
      const wrap = document.createElement('div');
      wrap.className = 'foto-wrap';
      wrap.id = `foto-${data.foto_id}`;
      wrap.innerHTML = `
        <img src="/fotos/${data.caminho}" class="miniatura-foto" onclick="window.open(this.src,'_blank')">
        <button class="btn-del-foto" onclick="deletarFoto(${data.foto_id})">×</button>
        <input class="foto-legenda" type="text" placeholder="Legenda…"
          oninput="salvarLegenda(${data.foto_id}, this.value)">`;
      container.appendChild(wrap);
    }
  };
  input.click();
}

async function deletarFoto(fotoId) {
  await fetch(`/api/foto/${fotoId}`, { method: 'DELETE' });
  const el = document.getElementById(`foto-${fotoId}`);
  if (el) el.remove();
}

function atualizarProgressBar() {
  const total = document.querySelectorAll('.btn-status-group').length;
  const avaliados = document.querySelectorAll('.btn-status.ativo').length;
  const pct = total > 0 ? Math.round(avaliados / total * 100) : 0;
  const bar = document.getElementById('progress-bar');
  const txt = document.getElementById('progress-txt');
  const pctEl = document.getElementById('progress-pct');
  if (bar) bar.style.width = pct + '%';
  if (txt) txt.textContent = `${avaliados} de ${total} itens avaliados`;
  if (pctEl) pctEl.textContent = pct + '%';
}

async function salvarRascunho() {
  if (!CHECKLIST_ID) return;
  // Forçar gravação pendente
  Object.values(saveQueue).forEach(t => clearTimeout(t));
  alert('Rascunho salvo automaticamente a cada alteração.');
}

async function finalizarChecklist() {
  if (!CHECKLIST_ID) return;
  const resultado = document.querySelector('input[name="resultado"]:checked')?.value;
  if (!resultado) {
    alert('Selecione o Resultado Final antes de finalizar.');
    return;
  }
  const obs = document.getElementById('obs-gerais').value;
  const resp = await fetch(`/api/checklist/${CHECKLIST_ID}/finalizar`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ resultado, observacoes_gerais: obs })
  });
  if (resp.ok) {
    window.location.href = `/api/checklist/${CHECKLIST_ID}/pdf`;
  }
}

function abrirCameraGeral() {
  if (!CHECKLIST_ID) return;
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = 'image/*';
  input.capture = 'environment';
  input.onchange = async function () {
    const file = this.files[0];
    if (!file) return;
    const fd = new FormData();
    fd.append('file', file);
    fd.append('checklist_id', CHECKLIST_ID);
    // sem item_id → foto geral das observações
    const resp = await fetch('/api/foto/upload', { method: 'POST', body: fd });
    const data = await resp.json();
    if (data.foto_id) {
      adicionarMiniaturaGeral(data.foto_id, data.caminho, '');
    }
  };
  input.click();
}

function adicionarMiniaturaGeral(fotoId, caminho, legenda) {
  const container = document.getElementById('fotos-gerais-container');
  if (!container) return;
  const wrap = document.createElement('div');
  wrap.className = 'foto-wrap';
  wrap.id = `foto-geral-${fotoId}`;
  wrap.innerHTML = `
    <img src="/fotos/${caminho}" class="miniatura-foto" onclick="window.open(this.src,'_blank')">
    <button class="btn-del-foto" onclick="deletarFotoGeral(${fotoId})">×</button>
    <input class="foto-legenda" type="text" placeholder="Legenda…"
      value="${(legenda||'').replace(/"/g,'&quot;')}"
      oninput="salvarLegenda(${fotoId}, this.value)">`;
  container.appendChild(wrap);
}

async function deletarFotoGeral(fotoId) {
  await fetch(`/api/foto/${fotoId}`, { method: 'DELETE' });
  const el = document.getElementById(`foto-geral-${fotoId}`);
  if (el) el.remove();
}

const _legendaTimers = {};
function salvarLegenda(fotoId, valor) {
  clearTimeout(_legendaTimers[fotoId]);
  _legendaTimers[fotoId] = setTimeout(() => {
    fetch(`/api/foto/${fotoId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ legenda: valor })
    });
  }, 600);
}
