# Graph Report - bot-vagas  (2026-09-16)

## Corpus Check
- 33 files · ~19,234 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 215 nodes · 326 edges · 27 communities (21 shown, 6 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 5 edges (avg confidence: 0.68)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6a5ff9d3`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Épico: bot de vagas de estágio/jr em SP com alerta no Telegram
- Implementation Details
- test_matcher.py
- Vaga
- What You Must Do When Invoked
- insert_vaga
- /graphify
- run
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
- main.py

## God Nodes (most connected - your core abstractions)
1. `run()` - 21 edges
2. `Vaga` - 18 edges
3. `Épico: bot de vagas de estágio/jr em SP com alerta no Telegram` - 13 edges
4. `classify_seniority()` - 12 edges
5. `What You Must Do When Invoked` - 12 edges
6. `/graphify` - 11 edges
7. `matched_stack_terms()` - 10 edges
8. `insert_vaga()` - 10 edges
9. `passes_geo_filter()` - 9 edges
10. `within_backfill_window()` - 9 edges

## Surprising Connections (you probably didn't know these)
- `test_format_message_includes_essentials()` --calls--> `format_message()`  [EXTRACTED]
  tests/test_telegram.py → src/alerter/telegram.py
- `test_format_message_remote_job_shows_remoto_label()` --calls--> `format_message()`  [EXTRACTED]
  tests/test_telegram.py → src/alerter/telegram.py
- `test_send_message_posts_token_and_payload()` --calls--> `send_message()`  [EXTRACTED]
  tests/test_telegram.py → src/alerter/telegram.py
- `test_send_message_propagates_http_errors()` --calls--> `send_message()`  [EXTRACTED]
  tests/test_telegram.py → src/alerter/telegram.py
- `test_run_sends_new_matching_vaga_and_marks_alerted()` --calls--> `connect()`  [EXTRACTED]
  tests/test_main.py → src/storage/db.py

## Import Cycles
- None detected.

## Communities (27 total, 6 thin omitted)

### Community 0 - "Épico: bot de vagas de estágio/jr em SP com alerta no Telegram"
Cohesion: 0.09
Nodes (21): Acceptance Criteria, Adzuna — parcialmente confirmado, Child Issues, Context, Current State, Dependency Graph, Effort Estimate, Evidência coletada das fontes (2026-09-15) (+13 more)

### Community 1 - "Implementation Details"
Cohesion: 0.18
Nodes (11): Coleta na Gupy (dois passes por termo), Decisões travadas, Filtro de senioridade (D4), Filtro geográfico (D3), Implementation Details, Mensagem do Telegram (D2 + D14), Proposed Change, Regra de dedupe (D10) (+3 more)

### Community 2 - "test_matcher.py"
Cohesion: 0.12
Nodes (29): datetime, classify_seniority(), is_stack_match(), matched_stack_terms(), normalize(), passes_geo_filter(), Lowercase, sem acento, espacos nas pontas — base de comparacao pro filtro…, D3: SP capital (presencial/hibrido) + remoto Brasil. Vaga remota vem com… (+21 more)

### Community 3 - "Vaga"
Cohesion: 0.14
Nodes (19): ABC, Client, Busca vagas para um termo, já aplicando o filtro geográfico da fonte., Scraper, Vaga, GupyScraper, parse_gupy_job(), Mapeia um item de `data[]` da API da Gupy para o modelo interno. Campos usados… (+11 more)

### Community 4 - "What You Must Do When Invoked"
Cohesion: 0.13
Nodes (15): Part A - Structural extraction for code files, Part B - Semantic extraction (parallel subagents), Part C - Merge AST + semantic into final extraction, Step 0 - GitHub repos and multi-path merge (only if a URL or several paths), Step 1 - Ensure graphify is installed, Step 2.5 - Video and audio (only if video files detected), Step 2 - Detect files, Step 3 - Extract entities and relationships (+7 more)

### Community 5 - "insert_vaga"
Cohesion: 0.34
Nodes (12): Connection, connect(), insert_vaga(), mark_alerted(), Insere a vaga se for nova. Retorna True se inseriu, False se já existia (mesma…, make_vaga(), Regra de dedupe da issue #1: UNIQUE(source, external_id) apenas., Issue #1 nao tem hash canonico ainda (issue #X) — dedupe e so por (source,… (+4 more)

### Community 6 - "/graphify"
Cohesion: 0.17
Nodes (11): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, PowerShell 5.1: Vertical scrolling stops working (+3 more)

### Community 7 - "run"
Cohesion: 0.26
Nodes (16): GupyScraper, collect_candidates(), Vaga, Busca todos os termos e funde por external_id — a mesma vaga pode aparecer sob…, run(), make_vaga(), Vaga, Idempotencia: dedupe por (source, external_id) impede reenvio. (+8 more)

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

### Community 26 - "main.py"
Cohesion: 0.29
Nodes (9): format_message(), Vaga, Mensagem enxuta por vaga (D2/D14 completo — script de apresentacao pronto pra…, send_message(), main(), test_format_message_includes_essentials(), test_format_message_remote_job_shows_remoto_label(), test_send_message_posts_token_and_payload() (+1 more)

## Knowledge Gaps
- **79 isolated node(s):** `bot-vagas`, `vagas`, `graphify`, `Usage`, `What graphify is for` (+74 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Vaga` connect `Vaga` to `test_matcher.py`, `insert_vaga`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Why does `run()` connect `run` to `main.py`, `test_matcher.py`, `insert_vaga`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **What connects `bot-vagas`, `vagas`, `graphify` to the rest of the system?**
  _79 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Épico: bot de vagas de estágio/jr em SP com alerta no Telegram` be split into smaller, more focused modules?**
  _Cohesion score 0.09090909090909091 - nodes in this community are weakly interconnected._
- **Should `test_matcher.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12473118279569892 - nodes in this community are weakly interconnected._
- **Should `Vaga` be split into smaller, more focused modules?**
  _Cohesion score 0.14461538461538462 - nodes in this community are weakly interconnected._
- **Should `What You Must Do When Invoked` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._