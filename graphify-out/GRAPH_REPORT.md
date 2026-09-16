# Graph Report - bot-vagas  (2026-09-16)

## Corpus Check
- 38 files · ~21,736 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 272 nodes · 433 edges · 30 communities (23 shown, 7 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 5 edges (avg confidence: 0.68)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `531542e6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Épico: bot de vagas de estágio/jr em SP com alerta no Telegram
- Implementation Details
- test_matcher.py
- format_message
- What You Must Do When Invoked
- base.py
- test_gupy_scraper.py
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
- VIP/blacklist de empresas, filtro de formação e export Markdown ATS
- append_ats_entry
- vagas_ats.md

## God Nodes (most connected - your core abstractions)
1. `run()` - 27 edges
2. `classify_seniority()` - 13 edges
3. `passes_formacao_filter()` - 13 edges
4. `Épico: bot de vagas de estágio/jr em SP com alerta no Telegram` - 13 edges
5. `Vaga` - 12 edges
6. `What You Must Do When Invoked` - 12 edges
7. `matched_stack_terms()` - 11 edges
8. `make_vaga()` - 11 edges
9. `/graphify` - 11 edges
10. `VIP/blacklist de empresas, filtro de formação e export Markdown ATS` - 10 edges

## Surprising Connections (you probably didn't know these)
- `test_format_message_includes_essentials()` --calls--> `format_message()`  [EXTRACTED]
  tests/test_telegram.py → src/alerter/telegram.py
- `test_format_message_non_vip_unaffected_by_new_param()` --calls--> `format_message()`  [EXTRACTED]
  tests/test_telegram.py → src/alerter/telegram.py
- `test_format_message_remote_job_shows_remoto_label()` --calls--> `format_message()`  [EXTRACTED]
  tests/test_telegram.py → src/alerter/telegram.py
- `test_send_message_posts_token_and_payload()` --calls--> `send_message()`  [EXTRACTED]
  tests/test_telegram.py → src/alerter/telegram.py
- `test_send_message_propagates_http_errors()` --calls--> `send_message()`  [EXTRACTED]
  tests/test_telegram.py → src/alerter/telegram.py

## Import Cycles
- None detected.

## Communities (30 total, 7 thin omitted)

### Community 0 - "Épico: bot de vagas de estágio/jr em SP com alerta no Telegram"
Cohesion: 0.09
Nodes (21): Acceptance Criteria, Adzuna — parcialmente confirmado, Child Issues, Context, Current State, Dependency Graph, Effort Estimate, Evidência coletada das fontes (2026-09-15) (+13 more)

### Community 1 - "Implementation Details"
Cohesion: 0.18
Nodes (11): Coleta na Gupy (dois passes por termo), Decisões travadas, Filtro de senioridade (D4), Filtro geográfico (D3), Implementation Details, Mensagem do Telegram (D2 + D14), Proposed Change, Regra de dedupe (D10) (+3 more)

### Community 2 - "test_matcher.py"
Cohesion: 0.08
Nodes (52): datetime, main(), classify_seniority(), _company_haystack(), is_blacklisted(), is_stack_match(), is_vip(), matched_stack_terms() (+44 more)

### Community 3 - "format_message"
Cohesion: 0.26
Nodes (11): format_message(), Vaga, Mensagem enxuta por vaga (D2/D14 completo — script de apresentacao pronto pra…, send_message(), Vaga alertada so por bypass de empresa VIP (spec 0002) nao pode deixar "Match:…, test_format_message_empty_terms_with_vip_explains_bypass(), test_format_message_includes_essentials(), test_format_message_non_vip_unaffected_by_new_param() (+3 more)

### Community 4 - "What You Must Do When Invoked"
Cohesion: 0.07
Nodes (26): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+18 more)

### Community 5 - "base.py"
Cohesion: 0.22
Nodes (16): ABC, Connection, Busca vagas para um termo, já aplicando o filtro geográfico da fonte., Scraper, Vaga, connect(), insert_vaga(), mark_alerted() (+8 more)

### Community 6 - "test_gupy_scraper.py"
Cohesion: 0.17
Nodes (15): Client, GupyScraper, parse_gupy_job(), Mapeia um item de `data[]` da API da Gupy para o modelo interno. Campos usados…, Dois passes por termo (achado 2 da spec): a API devolve `city`/`state` vazios…, fixture_record(), load_fixture(), Vaga real SP/hibrido, capturada em 2026-09-16 — campos exatamente como a API… (+7 more)

### Community 7 - "run"
Cohesion: 0.25
Nodes (19): GupyScraper, collect_candidates(), Vaga, Busca todos os termos e funde por external_id — a mesma vaga pode aparecer sob…, run(), make_vaga(), Vaga, Idempotencia: dedupe por (source, external_id) impede reenvio. (+11 more)

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

### Community 26 - "VIP/blacklist de empresas, filtro de formação e export Markdown ATS"
Cohesion: 0.12
Nodes (15): 1. VIP / Blacklist (`src/matcher/rules.py`), 2. Filtro de formação (`src/matcher/rules.py`), 3. Export Markdown ATS — `src/exporter/markdown.py` (módulo novo), 4. `format_message` (`src/alerter/telegram.py:8`), Acceptance Criteria, Context, Current State, Effort Estimate (+7 more)

### Community 27 - "append_ats_entry"
Cohesion: 0.31
Nodes (8): append_ats_entry(), Vaga, Append-only (spec 0002): nunca reescreve o arquivo, pra preservar checkboxes…, Append-only (spec 0002): nao pode apagar checkboxes ja marcados pelo usuario em…, test_append_creates_file_with_header_when_missing(), test_append_formats_vip_with_empty_terms(), test_append_no_vip_tag_when_not_vip(), test_append_preserves_previous_entries()

## Knowledge Gaps
- **92 isolated node(s):** `Context`, `Current State`, `1. VIP / Blacklist (`src/matcher/rules.py`)`, `2. Filtro de formação (`src/matcher/rules.py`)`, `3. Export Markdown ATS — `src/exporter/markdown.py` (módulo novo)` (+87 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `run()` connect `run` to `append_ats_entry`, `test_matcher.py`, `format_message`, `base.py`?**
  _High betweenness centrality (0.072) - this node is a cross-community bridge._
- **Why does `Vaga` connect `base.py` to `append_ats_entry`, `test_gupy_scraper.py`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Why does `format_message()` connect `format_message` to `test_matcher.py`, `run`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **What connects `Context`, `Current State`, `1. VIP / Blacklist (`src/matcher/rules.py`)` to the rest of the system?**
  _92 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Épico: bot de vagas de estágio/jr em SP com alerta no Telegram` be split into smaller, more focused modules?**
  _Cohesion score 0.09090909090909091 - nodes in this community are weakly interconnected._
- **Should `test_matcher.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08080808080808081 - nodes in this community are weakly interconnected._
- **Should `What You Must Do When Invoked` be split into smaller, more focused modules?**
  _Cohesion score 0.07407407407407407 - nodes in this community are weakly interconnected._