const LABELS_TIPO = {
  lote:'Lote', pavimentacao:'Pavimentação', passeio:'Passeio',
  saa:'SAA', drenagem:'Drenagem', ses:'SES',
  guarita:'Guarita', quiosque:'Quiosques', dep_lixo:'Dep. Lixo',
  deck:'Deck', salao:'Salão de Festas'
};

document.addEventListener('DOMContentLoaded', async function () {
  const resp = await fetch('/api/dashboard');
  const d = await resp.json();

  document.getElementById('total').textContent = d.total;
  document.getElementById('aprovados').textContent = d.por_resultado['APROVADO'] || 0;
  document.getElementById('ressalvas').textContent = d.por_resultado['APROVADO COM RESSALVAS'] || 0;
  document.getElementById('reprovados').textContent = d.por_resultado['REPROVADO'] || 0;
  document.getElementById('rascunhos').textContent = d.rascunhos || 0;

  const pct = d.lotes_total > 0
    ? Math.round((d.lotes_avaliados / d.lotes_total) * 100) : 0;
  document.getElementById('lotes-barra').style.width = pct + '%';
  document.getElementById('lotes-pct').textContent =
    `${d.lotes_avaliados} / ${d.lotes_total} (${pct}%)`;

  // Por tipo
  const tbody = document.querySelector('#tabela-tipo tbody');
  d.por_tipo.forEach(r => {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${LABELS_TIPO[r.tipo]||r.tipo}</td><td><b>${r.qtd}</b></td>`;
    tbody.appendChild(tr);
  });

  // Por resultado
  const rl = document.getElementById('resultado-lista');
  const total = d.total || 1;
  const cores = {
    'APROVADO': '#22c55e',
    'APROVADO COM RESSALVAS': '#f59e0b',
    'REPROVADO': '#ef4444',
    'PENDENTE': '#94a3b8'
  };
  Object.entries(d.por_resultado).forEach(([res, qtd]) => {
    const pct = Math.round(qtd / total * 100);
    const cor = cores[res] || '#94a3b8';
    rl.innerHTML += `
      <div class="resultado-linha">
        <span class="resultado-ponto" style="background:${cor}"></span>
        <span class="resultado-nome">${res}</span>
        <div class="resultado-barra-bg">
          <div class="resultado-barra-fill" style="width:${pct}%;background:${cor}"></div>
        </div>
        <span class="resultado-pct">${pct}%</span>
      </div>`;
  });

  // Recentes
  const tbody2 = document.getElementById('recentes-body');
  d.recentes.forEach(c => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${labelLocal(c)}</td>
      <td><span class="badge badge-${badgeClass(c.resultado)}">${c.resultado||'PENDENTE'}</span></td>
      <td>${c.data_vistoria||'—'}</td>
      <td>${c.responsavel_ude||'—'}</td>
      <td>
        <a href="/checklist/${c.id}" class="link-acao">👁</a>
        <a href="/api/checklist/${c.id}/pdf" target="_blank" class="link-acao">📥</a>
      </td>`;
    tbody2.appendChild(tr);
  });
});

function labelLocal(c) {
  if (c.tipo === 'lote') return `Lote ${c.lote} — Q.${c.quadra}`;
  if (c.rua) return c.rua;
  if (c.equipamento) return c.equipamento;
  return LABELS_TIPO[c.tipo] || c.tipo;
}

function badgeClass(r) {
  return {
    'APROVADO':'green','APROVADO COM RESSALVAS':'yellow',
    'REPROVADO':'red','PENDENTE':'gray'
  }[r]||'gray';
}
