-- Issue #1 (escopo enxuto): dedupe apenas por UNIQUE(source, external_id).
-- Sem canonical_hash (issue #X) e sem match_score ponderado (issue #Z) ainda.
CREATE TABLE IF NOT EXISTS vagas (
    id                   INTEGER PRIMARY KEY AUTOINCREMENT,
    source               TEXT    NOT NULL,   -- gupy|greenhouse|lever|adzuna
    external_id          TEXT    NOT NULL,   -- gupy: data[].id
    title                TEXT    NOT NULL,
    company              TEXT    NOT NULL,
    city                 TEXT,               -- '' quando remoto (Gupy)
    state                TEXT,
    workplace_type       TEXT,               -- remote|hybrid|on-site
    url                  TEXT    NOT NULL,
    published_at         TEXT,               -- ISO8601
    application_deadline TEXT,
    description          TEXT,
    seniority            TEXT,               -- internship|junior|trainee
    matched_terms        TEXT    NOT NULL,   -- JSON array dos termos de MINHA_STACK encontrados
    first_seen_at        TEXT    NOT NULL,
    alerted_at           TEXT,               -- NULL = ainda nao enviada
    UNIQUE(source, external_id)
);

CREATE INDEX IF NOT EXISTS idx_vagas_pending ON vagas(alerted_at);
