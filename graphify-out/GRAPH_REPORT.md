# Graph Report - bot-vagas  (2026-09-16)

## Corpus Check
- 46 files · ~27,579 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 402 nodes · 704 edges · 39 communities (32 shown, 7 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 4 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5a9bb827`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Épico: bot de vagas de estágio/jr em SP com alerta no Telegram
- Fix: falso positivo de substring em VIP/blacklist e VIP sem filtro de área
- test_matcher.py
- Vaga
- What You Must Do When Invoked
- Scraper — Eureca
- base.py
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
- rules.py
- [0.2.0.0] - 2026-09-17
- connect
- is_stack_match
- classify_seniority
- is_it_title
- matched_stack_terms
- passes_geo_filter

## God Nodes (most connected - your core abstractions)
1. `Vaga` - 44 edges
2. `run()` - 34 edges
3. `parse_eureca_opportunity()` - 24 edges
4. `fixture_record()` - 18 edges
5. `is_vip()` - 15 edges
6. `make_vaga()` - 15 edges
7. `EurecaScraper` - 14 edges
8. `setup_run()` - 14 edges
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

## Communities (39 total, 7 thin omitted)

### Community 0 - "Épico: bot de vagas de estágio/jr em SP com alerta no Telegram"
Cohesion: 0.06
Nodes (33): Acceptance Criteria, Adzuna — parcialmente confirmado, Child Issues, Coleta na Gupy (dois passes por termo), Context, Current State, Decisões travadas, Dependency Graph (+25 more)

### Community 1 - "Fix: falso positivo de substring em VIP/blacklist e VIP sem filtro de área"
Cohesion: 0.17
Nodes (11): 1. `_matches_company_list` com word boundary, 2. `is_it_title` — novo filtro de área, obrigatório pra todas as vagas, 3. Pipeline em `main.py`, Acceptance Criteria, Context, Current State, Files Reference, Fix: falso positivo de substring em VIP/blacklist e VIP sem filtro de área (+3 more)

### Community 2 - "test_matcher.py"
Cohesion: 0.18
Nodes (19): is_vip(), passes_formacao_filter(), Conservador (spec 0002): so rejeita se a description citar formatura/conclusao…, Mitigacao de slogan de carreira estilizado (ex.: Gupy #SANGUELARANJA): o termo…, test_formacao_accepts_from_target_year_onward(), test_formacao_accepts_range_including_target_year(), test_formacao_accepts_range_phrasing_without_month(), test_formacao_accepts_when_no_mention() (+11 more)

### Community 3 - "Vaga"
Cohesion: 0.24
Nodes (13): format_message(), Mensagem enxuta por vaga (D2/D14 completo — script de apresentacao pronto pra…, send_message(), collect_candidates(), Busca todos os termos e funde por external_id — a mesma vaga pode aparecer sob…, Vaga, Vaga alertada so por bypass de empresa VIP (spec 0002) nao pode deixar "Match:…, test_format_message_empty_terms_with_vip_explains_bypass() (+5 more)

### Community 4 - "What You Must Do When Invoked"
Cohesion: 0.07
Nodes (26): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+18 more)

### Community 5 - "Scraper — Eureca"
Cohesion: 0.25
Nodes (7): Completed, Confirmar se HTML na `description` da Eureca afeta o matcher, Eliminar duplicação de `_normalize()` entre scraper e matcher, Logar quando `_fetch_all` bate no teto de `MAX_PAGES`, Scraper — Eureca, TODOS, Validar shape do payload da API da Eureca antes de indexar

### Community 6 - "base.py"
Cohesion: 0.15
Nodes (15): ABC, log_rejection(), datetime, Append-only (mesmo padrao do ATS export, spec 0002) — nunca reescreve o…, append_ats_entry(), Append-only (spec 0002): nunca reescreve o arquivo, pra preservar checkboxes…, Busca vagas para um termo, já aplicando o filtro geográfico da fonte., Scraper (+7 more)

### Community 7 - "run"
Cohesion: 0.23
Nodes (25): main(), run(), make_vaga(), VIP bypassa so matched_stack_terms — o titulo ainda precisa ser de TI (fix spec…, Fix spec 0003: empresa VIP tambem contrata fora de TI (RH, juridico) — VIP…, Fix spec 0003: "inter"/"xp" nao podem bater como substring dentro de…, Categoria de auditoria 'senioridade' (issue #4): titulo sem termo de entrada…, Issue #4: log de auditoria roda sempre, inclusive em --debug (ao contrario do… (+17 more)

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
Cohesion: 0.06
Nodes (62): EurecaScraper, _normalize(), parse_eureca_opportunity(), Client, O endpoint /opportunities nao aceita filtro de busca por palavra- chave…, Cacheado por instancia: `search()` e chamado uma vez por termo de busca em…, Lowercase, sem acento — mesma tecnica de matcher/rules.py, duplicada aqui pra…, Prefere São Paulo (capital) se estiver entre as cidades elegiveis da vaga… (+54 more)

### Community 30 - "GupyScraper"
Cohesion: 0.17
Nodes (15): GupyScraper, parse_gupy_job(), Client, Mapeia um item de `data[]` da API da Gupy para o modelo interno. Campos usados…, Dois passes por termo (achado 2 da spec): a API devolve `city`/`state` vazios…, fixture_record(), load_fixture(), Vaga real SP/hibrido, capturada em 2026-09-16 — campos exatamente como a API… (+7 more)

### Community 31 - "rules.py"
Cohesion: 0.15
Nodes (16): _company_haystack(), is_blacklisted(), _matches_company_list(), normalize(), datetime, company (careerPageName) + title + primeiros 500 chars da description,…, Word boundary, nao substring puro (fix spec 0003): nome curto de VIP tipo…, Issue #1 ponto 6: primeiro run so considera vagas publicadas dentro da janela… (+8 more)

### Community 32 - "[0.2.0.0] - 2026-09-17"
Cohesion: 0.40
Nodes (4): [0.2.0.0] - 2026-09-17, Added, Changed, Changelog

### Community 33 - "connect"
Cohesion: 0.34
Nodes (12): Connection, connect(), insert_vaga(), mark_alerted(), Insere a vaga se for nova. Retorna True se inseriu, False se já existia (mesma…, make_vaga(), Regra de dedupe da issue #1: UNIQUE(source, external_id) apenas., Issue #1 nao tem hash canonico ainda (issue #X) — dedupe e so por (source,… (+4 more)

### Community 34 - "is_stack_match"
Cohesion: 0.27
Nodes (10): is_stack_match(), matched_adjacent_terms(), matched_core_terms(), Matching simples (mesmo mecanismo da antiga matched_stack_terms): quais termos…, Aprova com >=1 termo de CORE_STACK OU >=2 termos de ADJACENT_STACK (issue #4)., test_stack_match_false_with_no_terms(), test_stack_match_false_with_single_adjacent_term(), test_stack_match_true_with_core_and_one_adjacent() (+2 more)

### Community 35 - "classify_seniority"
Cohesion: 0.22
Nodes (9): classify_seniority(), D4: campo `type` da Gupy decide estagio direto; caso contrario, regex positiva…, D4: titulo tipo 'Junior/Pleno' ainda e vaga de entrada valida., test_seniority_exclusion_only_title_is_rejected(), test_seniority_mixed_title_positive_wins(), test_seniority_no_match_is_rejected(), test_seniority_positive_regex_junior(), test_seniority_positive_regex_trainee() (+1 more)

### Community 36 - "is_it_title"
Cohesion: 0.25
Nodes (8): is_it_title(), Issue #4: devops/infraestrutura/cloud sao termos novos; dados/ti/…, Bug real: vaga 'Estágio | Trabalhista' (Direito) de empresa VIP não pode passar…, Regra pedida pelo usuário: só o título conta, não a description., test_is_it_title_accepts_each_keyword(), test_is_it_title_accepts_expanded_titles_issue_4(), test_is_it_title_ignores_description(), test_is_it_title_rejects_title_without_it_terms()

### Community 37 - "matched_stack_terms"
Cohesion: 0.29
Nodes (7): matched_stack_terms(), Lista combinada (issue #4) pra exibicao na mensagem do Telegram e no export ATS…, "spring boot" da MINHA_STACK (issue #1) virou "spring" em CORE_STACK (issue #4)…, test_matched_stack_terms_combines_core_and_adjacent(), test_matching_counts_multiple_stack_terms(), test_matching_no_terms_returns_empty(), test_matching_single_term_still_counts()

### Community 38 - "passes_geo_filter"
Cohesion: 0.33
Nodes (6): passes_geo_filter(), D3: SP capital (presencial/hibrido) + remoto Brasil. Vaga remota vem com…, Regressao do achado 2: vaga remota tem city/state vazios e ainda assim deve ser…, test_geo_filter_accepts_remote_with_empty_city_state(), test_geo_filter_accepts_sp_capital_hybrid(), test_geo_filter_rejects_other_state_hybrid()

## Knowledge Gaps
- **110 isolated node(s):** `bot-vagas`, `vagas`, `graphify`, `Usage`, `What graphify is for` (+105 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Vaga` connect `Vaga` to `connect`, `is_stack_match`, `classify_seniority`, `is_it_title`, `test_matcher.py`, `base.py`, `matched_stack_terms`, `passes_geo_filter`, `run`, `test_eureca.py`, `GupyScraper`, `rules.py`?**
  _High betweenness centrality (0.204) - this node is a cross-community bridge._
- **Why does `parse_eureca_opportunity()` connect `test_eureca.py` to `Vaga`?**
  _High betweenness centrality (0.083) - this node is a cross-community bridge._
- **Why does `EurecaScraper` connect `test_eureca.py` to `Vaga`, `base.py`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Vaga` (e.g. with `EurecaScraper` and `GupyScraper`) actually correct?**
  _`Vaga` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `bot-vagas`, `vagas`, `graphify` to the rest of the system?**
  _110 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Épico: bot de vagas de estágio/jr em SP com alerta no Telegram` be split into smaller, more focused modules?**
  _Cohesion score 0.058823529411764705 - nodes in this community are weakly interconnected._
- **Should `What You Must Do When Invoked` be split into smaller, more focused modules?**
  _Cohesion score 0.07407407407407407 - nodes in this community are weakly interconnected._