-- PostgreSQL schema for UDE Checklists — Obra 38
-- Equivalent to schema.sql; uses SERIAL, NOW(), and TEXT where SQLite used INTEGER/TEXT.

CREATE TABLE IF NOT EXISTS checklists (
    id                SERIAL PRIMARY KEY,
    tipo              TEXT NOT NULL,
    quadra            TEXT,
    lote              TEXT,
    rua               TEXT,
    trecho_inicio     TEXT,
    trecho_fim        TEXT,
    lotes_atendidos   TEXT,
    equipamento       TEXT,
    subequipamento    TEXT,
    responsavel_ude   TEXT,
    empresa_executora TEXT,
    data_vistoria     TEXT,
    resultado         TEXT DEFAULT 'PENDENTE',
    observacoes_gerais TEXT,
    criado_em         TIMESTAMP DEFAULT NOW(),
    atualizado_em     TIMESTAMP DEFAULT NOW(),
    finalizado        INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS checklist_itens (
    id            SERIAL PRIMARY KEY,
    checklist_id  INTEGER NOT NULL REFERENCES checklists(id) ON DELETE CASCADE,
    secao         TEXT NOT NULL,
    item_nr       TEXT NOT NULL,
    descricao     TEXT NOT NULL,
    status        TEXT DEFAULT 'NA',
    observacao    TEXT,
    requer_foto   INTEGER DEFAULT 0,
    local_ref     TEXT
);

CREATE TABLE IF NOT EXISTS fotos (
    id            SERIAL PRIMARY KEY,
    checklist_id  INTEGER NOT NULL REFERENCES checklists(id) ON DELETE CASCADE,
    item_id       INTEGER REFERENCES checklist_itens(id),
    caminho       TEXT NOT NULL,
    legenda       TEXT,
    capturado_em  TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS config (
    chave TEXT PRIMARY KEY,
    valor TEXT
);

INSERT INTO config (chave, valor) VALUES ('nome_obra',   'Recanto das Oliveiras')
    ON CONFLICT (chave) DO NOTHING;
INSERT INTO config (chave, valor) VALUES ('numero_obra', '38')
    ON CONFLICT (chave) DO NOTHING;
INSERT INTO config (chave, valor) VALUES ('construtora', 'Viana & Moura Construções')
    ON CONFLICT (chave) DO NOTHING;

CREATE INDEX IF NOT EXISTS idx_checklists_tipo ON checklists(tipo);
CREATE INDEX IF NOT EXISTS idx_checklists_quadra_lote ON checklists(quadra, lote);
CREATE INDEX IF NOT EXISTS idx_checklists_rua ON checklists(rua);
CREATE INDEX IF NOT EXISTS idx_itens_checklist ON checklist_itens(checklist_id);
CREATE INDEX IF NOT EXISTS idx_fotos_checklist ON fotos(checklist_id);

CREATE TABLE IF NOT EXISTS anotacoes_mapa (
    id            SERIAL PRIMARY KEY,
    rua           TEXT,
    svg_x         REAL NOT NULL,
    svg_y         REAL NOT NULL,
    texto         TEXT,
    foto_caminho  TEXT,
    criado_em     TIMESTAMPTZ DEFAULT NOW()
);
