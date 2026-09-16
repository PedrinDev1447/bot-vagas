# Graph Report - bot-vagas  (2026-09-16)

## Corpus Check
- 31 files · ~18,624 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 193 nodes · 283 edges · 26 communities (20 shown, 6 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 5 edges (avg confidence: 0.68)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5f6e3686`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Épico: bot de vagas de estágio/jr em SP com alerta no Telegram
- Implementation Details
- test_matcher.py
- main.py
- What You Must Do When Invoked
- insert_vaga
- test_gupy_scraper.py
- /graphify
- bot-vagas
- graphify reference: extra exports and benchmark
- graphify reference: query, path, explain
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- graphify reference: GitHub clone and cross-repo merge
- graphify reference: transcribe video and audio
- .claude/CLAUDE.md
- extraction-spec.md
- schema.sql
- bot-vagas

## God Nodes (most connected - your core abstractions)
1. `Vaga` - 20 edges
2. `run()` - 13 edges
3. `classify_seniority()` - 13 edges
4. `Épico: bot de vagas de estágio/jr em SP com alerta no Telegram` - 13 edges
5. `What You Must Do When Invoked` - 12 edges
6. `matched_stack_terms()` - 11 edges
7. `GupyScraper` - 11 edges
8. `insert_vaga()` - 11 edges
9. `/graphify` - 11 edges
10. `passes_geo_filter()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `test_geo_filter_accepts_sp_capital_hybrid()` --calls--> `passes_geo_filter()`  [EXTRACTED]
  tests/test_matcher.py → src/matcher/rules.py
- `test_geo_filter_rejects_other_state_hybrid()` --calls--> `passes_geo_filter()`  [EXTRACTED]
  tests/test_matcher.py → src/matcher/rules.py
- `test_seniority_exclusion_only_title_is_rejected()` --calls--> `classify_seniority()`  [EXTRACTED]
  tests/test_matcher.py → src/matcher/rules.py
- `test_seniority_no_match_is_rejected()` --calls--> `classify_seniority()`  [EXTRACTED]
  tests/test_matcher.py → src/matcher/rules.py
- `test_seniority_positive_regex_junior()` --calls--> `classify_seniority()`  [EXTRACTED]
  tests/test_matcher.py → src/matcher/rules.py

## Import Cycles
- None detected.

## Communities (26 total, 6 thin omitted)

### Community 0 - "Épico: bot de vagas de estágio/jr em SP com alerta no Telegram"
Cohesion: 0.09
Nodes (21): Acceptance Criteria, Adzuna — parcialmente confirmado, Child Issues, Context, Current State, Dependency Graph, Effort Estimate, Evidência coletada das fontes (2026-09-15) (+13 more)

### Community 1 - "Implementation Details"
Cohesion: 0.18
Nodes (11): Coleta na Gupy (dois passes por termo), Decisões travadas, Filtro de senioridade (D4), Filtro geográfico (D3), Implementation Details, Mensagem do Telegram (D2 + D14), Proposed Change, Regra de dedupe (D10) (+3 more)

### Community 2 - "test_matcher.py"
Cohesion: 0.13
Nodes (28): datetime, classify_seniority(), matched_stack_terms(), normalize(), passes_geo_filter(), Lowercase, sem acento, espacos nas pontas — base de comparacao pro filtro…, D3: SP capital (presencial/hibrido) + remoto Brasil. Vaga remota vem com…, D4: campo `type` da Gupy decide estagio direto; caso contrario, regex positiva… (+20 more)

### Community 3 - "main.py"
Cohesion: 0.20
Nodes (13): ABC, Client, send_message(), collect_candidates(), main(), Busca todos os termos e funde por external_id — a mesma vaga pode aparecer sob…, run(), is_stack_match() (+5 more)

### Community 4 - "What You Must Do When Invoked"
Cohesion: 0.13
Nodes (15): Part A - Structural extraction for code files, Part B - Semantic extraction (parallel subagents), Part C - Merge AST + semantic into final extraction, Step 0 - GitHub repos and multi-path merge (only if a URL or several paths), Step 1 - Ensure graphify is installed, Step 2.5 - Video and audio (only if video files detected), Step 2 - Detect files, Step 3 - Extract entities and relationships (+7 more)

### Community 5 - "insert_vaga"
Cohesion: 0.34
Nodes (12): Connection, connect(), insert_vaga(), mark_alerted(), Insere a vaga se for nova. Retorna True se inseriu, False se já existia (mesma…, make_vaga(), Regra de dedupe da issue #1: UNIQUE(source, external_id) apenas., Issue #1 nao tem hash canonico ainda (issue #X) — dedupe e so por (source,… (+4 more)

### Community 6 - "test_gupy_scraper.py"
Cohesion: 0.26
Nodes (12): parse_gupy_job(), Mapeia um item de `data[]` da API da Gupy para o modelo interno. Campos usados…, fixture_record(), load_fixture(), Vaga real SP/hibrido, capturada em 2026-09-16 — campos exatamente como a API…, Achado 2 da spec: vaga remota vem com city/state vazios na Gupy., type == vacancy_type_effective (nao-estagio) nao deve virar hint de estagio —…, Passe A (state=SP) pega presencial/hibrido de SP; Passe B (sem state) mantem so… (+4 more)

### Community 7 - "/graphify"
Cohesion: 0.17
Nodes (11): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, PowerShell 5.1: Vertical scrolling stops working (+3 more)

### Community 8 - "bot-vagas"
Cohesion: 0.22
Nodes (8): bot-vagas, Estrutura, graphify, gstack, Regras do projeto, Skill routing, Stack técnica, Visão geral

### Community 9 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 10 - "graphify reference: query, path, explain"
Cohesion: 0.33
Nodes (5): For /graphify explain, For /graphify path, graphify reference: query, path, explain, Step 0 — Constrained query expansion (REQUIRED before traversal), Step 1 — Traversal

### Community 11 - "graphify reference: add a URL and watch a folder"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 12 - "graphify reference: commit hook and native CLAUDE.md integration"
Cohesion: 0.50
Nodes (3): For git commit hook, For native CLAUDE.md integration, graphify reference: commit hook and native CLAUDE.md integration

### Community 13 - "graphify reference: incremental update and cluster-only"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

## Knowledge Gaps
- **79 isolated node(s):** `bot-vagas`, `vagas`, `graphify`, `Usage`, `What graphify is for` (+74 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Vaga` connect `main.py` to `test_matcher.py`, `insert_vaga`, `test_gupy_scraper.py`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Why does `parse_gupy_job()` connect `test_gupy_scraper.py` to `main.py`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Why does `GupyScraper` connect `main.py` to `test_gupy_scraper.py`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **What connects `bot-vagas`, `vagas`, `graphify` to the rest of the system?**
  _79 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Épico: bot de vagas de estágio/jr em SP com alerta no Telegram` be split into smaller, more focused modules?**
  _Cohesion score 0.09090909090909091 - nodes in this community are weakly interconnected._
- **Should `test_matcher.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12873563218390804 - nodes in this community are weakly interconnected._
- **Should `What You Must Do When Invoked` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._