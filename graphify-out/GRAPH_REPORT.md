# Graph Report - bot-vagas  (2026-09-16)

## Corpus Check
- 46 files · ~27,579 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 392 nodes · 690 edges · 32 communities (24 shown, 8 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS · INFERRED: 2 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a292589b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Épico: bot de vagas de estágio/jr em SP com alerta no Telegram
- Fix: falso positivo de substring em VIP/blacklist e VIP sem filtro de área
- test_matcher.py
- test_telegram.py
- What You Must Do When Invoked
- append_ats_entry
- main.py
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
- test_eureca.py
- vagas_ats.md
- GupyScraper
- Client

## God Nodes (most connected - your core abstractions)
1. `Vaga` - 40 edges
2. `run()` - 34 edges
3. `parse_eureca_opportunity()` - 24 edges
4. `fixture_record()` - 18 edges
5. `is_vip()` - 15 edges
6. `make_vaga()` - 15 edges
7. `setup_run()` - 14 edges
8. `EurecaScraper` - 13 edges
9. `classify_seniority()` - 13 edges
10. `is_stack_match()` - 13 edges

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

## Communities (32 total, 8 thin omitted)

### Community 0 - "Épico: bot de vagas de estágio/jr em SP com alerta no Telegram"
Cohesion: 0.06
Nodes (33): Acceptance Criteria, Adzuna — parcialmente confirmado, Child Issues, Coleta na Gupy (dois passes por termo), Context, Current State, Decisões travadas, Dependency Graph (+25 more)

### Community 1 - "Fix: falso positivo de substring em VIP/blacklist e VIP sem filtro de área"
Cohesion: 0.17
Nodes (11): 1. `_matches_company_list` com word boundary, 2. `is_it_title` — novo filtro de área, obrigatório pra todas as vagas, 3. Pipeline em `main.py`, Acceptance Criteria, Context, Current State, Files Reference, Fix: falso positivo de substring em VIP/blacklist e VIP sem filtro de área (+3 more)

### Community 2 - "test_matcher.py"
Cohesion: 0.05
Nodes (76): classify_seniority(), _company_haystack(), is_blacklisted(), is_it_title(), is_stack_match(), is_vip(), matched_adjacent_terms(), matched_core_terms() (+68 more)

### Community 3 - "test_telegram.py"
Cohesion: 0.29
Nodes (10): format_message(), Mensagem enxuta por vaga (D2/D14 completo — script de apresentacao pronto pra…, send_message(), Vaga alertada so por bypass de empresa VIP (spec 0002) nao pode deixar "Match:…, test_format_message_empty_terms_with_vip_explains_bypass(), test_format_message_includes_essentials(), test_format_message_non_vip_unaffected_by_new_param(), test_format_message_remote_job_shows_remoto_label() (+2 more)

### Community 4 - "What You Must Do When Invoked"
Cohesion: 0.07
Nodes (26): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+18 more)

### Community 5 - "append_ats_entry"
Cohesion: 0.36
Nodes (7): append_ats_entry(), Append-only (spec 0002): nunca reescreve o arquivo, pra preservar checkboxes…, Append-only (spec 0002): nao pode apagar checkboxes ja marcados pelo usuario em…, test_append_creates_file_with_header_when_missing(), test_append_formats_vip_with_empty_terms(), test_append_no_vip_tag_when_not_vip(), test_append_preserves_previous_entries()

### Community 6 - "main.py"
Cohesion: 0.15
Nodes (21): ABC, Connection, log_rejection(), datetime, Append-only (mesmo padrao do ATS export, spec 0002) — nunca reescreve o…, main(), Busca vagas para um termo, já aplicando o filtro geográfico da fonte., Scraper (+13 more)

### Community 7 - "run"
Cohesion: 0.24
Nodes (24): run(), make_vaga(), VIP bypassa so matched_stack_terms — o titulo ainda precisa ser de TI (fix spec…, Fix spec 0003: empresa VIP tambem contrata fora de TI (RH, juridico) — VIP…, Fix spec 0003: "inter"/"xp" nao podem bater como substring dentro de…, Categoria de auditoria 'senioridade' (issue #4): titulo sem termo de entrada…, Issue #4: log de auditoria roda sempre, inclusive em --debug (ao contrario do…, Idempotencia: dedupe por (source, external_id) impede reenvio. (+16 more)

### Community 8 - "bot-vagas"
Cohesion: 0.20
Nodes (9): bot-vagas, Estrutura, graphify, gstack, Regras do projeto, Roadmap de fontes, Skill routing, Stack técnica (+1 more)

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

### Community 27 - "test_eureca.py"
Cohesion: 0.05
Nodes (64): Client, Scraper, EurecaScraper, _normalize(), parse_eureca_opportunity(), O endpoint /opportunities nao aceita filtro de busca por palavra- chave…, Cacheado por instancia: `search()` e chamado uma vez por termo de busca em…, Lowercase, sem acento — mesma tecnica de matcher/rules.py, duplicada aqui pra… (+56 more)

### Community 30 - "GupyScraper"
Cohesion: 0.15
Nodes (17): collect_candidates(), Busca todos os termos e funde por external_id — a mesma vaga pode aparecer sob…, GupyScraper, parse_gupy_job(), Client, Mapeia um item de `data[]` da API da Gupy para o modelo interno. Campos usados…, Dois passes por termo (achado 2 da spec): a API devolve `city`/`state` vazios…, fixture_record() (+9 more)

## Knowledge Gaps
- **103 isolated node(s):** `bot-vagas`, `vagas`, `graphify`, `Usage`, `What graphify is for` (+98 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Vaga` connect `test_matcher.py` to `test_telegram.py`, `append_ats_entry`, `main.py`, `run`, `GupyScraper`?**
  _High betweenness centrality (0.088) - this node is a cross-community bridge._
- **Why does `run()` connect `run` to `test_matcher.py`, `test_telegram.py`, `append_ats_entry`, `main.py`, `GupyScraper`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **What connects `bot-vagas`, `vagas`, `graphify` to the rest of the system?**
  _103 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Épico: bot de vagas de estágio/jr em SP com alerta no Telegram` be split into smaller, more focused modules?**
  _Cohesion score 0.058823529411764705 - nodes in this community are weakly interconnected._
- **Should `test_matcher.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05427905427905428 - nodes in this community are weakly interconnected._
- **Should `What You Must Do When Invoked` be split into smaller, more focused modules?**
  _Cohesion score 0.07407407407407407 - nodes in this community are weakly interconnected._
- **Should `VIP/blacklist de empresas, filtro de formação e export Markdown ATS` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._