# Épico: bot de vagas de estágio/jr em SP com alerta no Telegram

## Context

Busca ativa por vaga de estágio/júnior em São Paulo. Vaga de entrada em tech
publicada na Gupy fica no ar poucos dias e a janela de candidatura é o diferencial
real: quem vê primeiro se candidata primeiro. Hoje a busca é manual, em abas de
Gupy e páginas de carreira, e vaga publicada numa terça à noite é vista na quinta
ou não é vista.

Este épico entrega um bot que coleta vagas de fontes públicas, filtra por match com
um perfil de stack definido (Java, Spring Boot, React, TypeScript, AWS), e manda um
digest no Telegram duas vezes por dia, sem nunca repetir uma vaga já enviada.

Quem é afetado: um dev solo. Sem outros usuários, sem multi-tenant, sem perfil
configurável por usuário.

## Current State

Repo greenfield. Verificado em 2026-09-15:

| Item | Estado |
|---|---|
| Código-fonte | Nenhum. `find . -name "*.py"` retorna vazio |
| Commits | 2, ambos de scaffold (`6871f87`, `467055a`) |
| Python na máquina de dev | **Ausente.** `python`, `python3`, `py` todos não encontrados |
| uv | Presente, 0.12.1 |
| node | Presente, v24.18.0 |
| Remote no GitHub | **Nenhum.** `git remote -v` vazio |
| Telegram bot | Não criado |
| Conta Adzuna | Não criada |

## Evidência coletada das fontes (2026-09-15)

Tudo abaixo foi confirmado batendo no endpoint real, não de memória.

### Gupy — confirmado, HTTP 200, sem autenticação

```
GET https://employability-portal.gupy.io/api/v1/jobs?jobName=&state=&limit=&offset=
```

Resposta: `{ "data": [...], "pagination": { "total", "limit", "offset" } }`

Campos reais do objeto vaga:

| Campo | Tipo | Exemplo observado |
|---|---|---|
| `id` | int | `11725862` |
| `companyId` | int | `30945` |
| `name` | string | `"ANALISTA DESENVOLVEDOR JAVA PL"` |
| `description` | string | HTML/texto longo |
| `careerPageName` | string | `"Globalweb"` |
| `careerPageUrl` | string | URL com token base64 |
| `type` | enum | `vacancy_type_effective`, `vacancy_type_internship` |
| `publishedDate` | ISO8601 | `"2026-09-15T22:38:58.349Z"` |
| `applicationDeadline` | date | `"2026-09-19"` |
| `isRemoteWork` | bool | `true` |
| `city` | string | `"São Paulo"` ou `""` |
| `state` | string | `"São Paulo"` ou `""` |
| `country` | string | `"Brasil"` |
| `jobUrl` | string | URL com token base64 contendo `source` |
| `workplaceType` | enum | `remote`, `hybrid`, `on-site` |
| `badges` | object | `{"friendlyBadge":true,"isPWD":true}` |
| `skills` | array | **sempre `[]` nas amostras** |

Três achados que determinam o desenho:

1. **`type` distingue estágio por campo.** `vacancy_type_internship` aparece em
   100% das amostras de busca por "estagio" (total: 1719). Estágio não precisa de
   regex no título. Júnior e trainee não têm campo equivalente e continuam sendo
   regex.

2. **Vaga remota vem com `city` e `state` como string vazia.** Query com
   `state=São Paulo` derruba o total de 594 para 66 e devolve apenas
   `hybrid`/`on-site`. Filtrar por estado no servidor **exclui silenciosamente
   todas as vagas remotas**, que são metade do escopo geográfico definido. O
   coletor precisa de duas queries por termo de busca.

3. **`skills` vem vazio.** O match de stack sai obrigatoriamente de `name` +
   `description`.

### Adzuna — parcialmente confirmado

Endpoint documentado: `https://api.adzuna.com/v1/api/jobs/{country}/search/{page}`
com `app_id`, `app_key`, `what` obrigatórios; `where`, `results_per_page`,
`max_days_old`, `sort_by` opcionais. Campos de resposta documentados: `id`,
`title`, `description` (snippet), `created`, `redirect_url`, `company.display_name`,
`location.area[]`, `location.display_name`, `salary_min`, `salary_max`,
`contract_type`, `contract_time`.

**Não confirmado em primeira mão.** Chamadas sem chave retornam uma página de erro
HTML genérica para qualquer país, inclusive um código inexistente (`zz`), então o
probe é inconclusivo. Suporte a Brasil (`br`) vem da documentação e de fontes
secundárias. **Bloqueia a issue #3 até ser validado com chave real.**

### Greenhouse / Lever — não probados ainda

Endpoints públicos por empresa. Formato exato a confirmar na issue #2, antes de
escrever o parser.

### Itens NÃO confirmados (validar antes de implementar)

| Item | Por quê importa | Como confirmar |
|---|---|---|
| Adzuna suporta `br` | Decide se a issue #3 existe | Criar conta, 1 chamada real |
| Cota diária do plano free da Adzuna | Decide a cadência do coletor | Documentação da conta |
| Limite de caracteres por mensagem no Telegram | Decide o chunking do digest | 1 chamada real de teste |
| Formato exato do feed Greenhouse/Lever | Decide o parser | 1 GET em empresa real |
| Existe `vacancy_type_trainee` na Gupy? | Decide se trainee é campo ou regex | Query por "trainee" |

## Proposed Change

```
GitHub Actions (cron)
  |
  +-- coleta (a cada 4h)              +-- alerta (09:00 e 18:00 BRT)
  |     scraper.gupy                  |     storage: WHERE alerted_at IS NULL
  |     scraper.greenhouse            |            AND match_score >= threshold
  |     scraper.lever                 |     alerter: monta digest + script
  |     scraper.adzuna                |         |
  |         |                         |         v
  |     matcher (geo -> nivel -> stack)|     Telegram sendMessage
  |         |                         |         |
  |         v                         |         v
  |     storage.upsert (dedupe)       |     storage: marca alerted_at
  |         |                         |         |
  +-- commit vagas.db de volta no repo <--------+
```

### Decisões travadas

| # | Decisão | Escolha |
|---|---|---|
| D1 | Definição de pronto | Recall-first: 7 dias, zero vagas achadas manualmente que o bot não alertou |
| D2 | Volume | Digest 2x/dia, uma mensagem por run |
| D3 | Geografia | SP capital (presencial/híbrido) + remoto Brasil |
| D4 | Senioridade | Estágio + júnior + trainee |
| D5 | Corte MVP | Uma fonte ponta a ponta primeiro, depois as outras |
| D6 | Persistência | Commitar `vagas.db` de volta no repo ao fim de cada run |
| D7 | Cadência | Coleta 4/4h, alerta 2x/dia |
| D9 | Match | Score por grupo, pesos em config YAML |
| D10 | Dedupe | Id nativo + hash canônico (empresa+título+cidade) |
| D11 | ATS | Greenhouse + Lever, lista de empresas versionada |
| D12 | Toolchain | uv + pyproject.toml + .python-version 3.13 |
| D13 | Custo | Zero dinheiro. Cadastro gratuito permitido (Adzuna fica) |
| D14 | Script | Mensagem de apresentação pronta para colar, por template |

### Implementation Details

#### Schema SQLite

```sql
CREATE TABLE jobs (
    id                   INTEGER PRIMARY KEY AUTOINCREMENT,
    source               TEXT    NOT NULL,   -- gupy|greenhouse|lever|adzuna
    external_id          TEXT    NOT NULL,   -- gupy: data[].id
    canonical_hash       TEXT    NOT NULL,   -- sha256(company|title|city) normalizados
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
    match_score          REAL    NOT NULL,
    matched_terms        TEXT    NOT NULL,   -- JSON array
    first_seen_at        TEXT    NOT NULL,
    alerted_at           TEXT,               -- NULL = ainda nao enviada
    UNIQUE(source, external_id)
);

CREATE INDEX idx_jobs_canonical ON jobs(canonical_hash);
CREATE INDEX idx_jobs_pending   ON jobs(alerted_at, match_score);
```

#### Regra de dedupe (D10)

1. `INSERT ... ON CONFLICT(source, external_id) DO NOTHING` — barra reingestão
   dentro da mesma fonte.
2. Antes de alertar, descartar se existe outra linha com o mesmo
   `canonical_hash` e `alerted_at IS NOT NULL` — barra a mesma vaga vinda de
   outra fonte ou repostada com id novo.
3. Normalização para o hash: lowercase, remoção de acentos, colapso de espaços,
   remoção de sufixos societários (`ltda`, `s.a.`, `me`, `eireli`).

#### Regra de match (D9) — `config/matcher.yaml`

```yaml
groups:
  backend:
    weight: 3
    terms: [java, "spring boot", spring, jpa, hibernate, maven]
  frontend:
    weight: 3
    terms: [react, reactjs, "react.js", typescript, "next.js"]
  infra:
    weight: 2
    terms: [aws, "amazon web services", s3, ec2, lambda, "elastic beanstalk"]

title_bonus: 2     # qualquer termo aparecendo em `name`
threshold: 4       # alerta quando score >= threshold
```

Score = soma dos pesos dos grupos que bateram (cada grupo conta uma vez, não por
termo) + `title_bonus` se qualquer termo aparecer no título.

Consequência desejada, que é o critério de aceite da regra:

| Cenário | Score | Alerta? |
|---|---|---|
| Java + Spring no corpo, React no corpo | 3+3=6 | Sim |
| Java no título, nada mais | 3+2=5 | Sim |
| Só AWS citada em "diferenciais" | 2 | **Não** |
| Só AWS, mas no título | 2+2=4 | Sim |
| Nenhum termo | 0 | Não |

#### Filtro geográfico (D3)

Aceita se `workplace_type == "remote"` **OU**
(`normalize(state) == "sao paulo"` E `normalize(city) == "sao paulo"`).

O ramo remoto não checa city/state, porque a API devolve string vazia nesses
campos para vaga remota. Essa é a razão do teste de regressão AC-2.

#### Filtro de senioridade (D4)

1. Gupy: `type == "vacancy_type_internship"` → `seniority = internship`.
2. Regex positiva no título: `estág|estagi|intern|júnior|junior|\bjr\b|trainee`.
3. Regex de exclusão: `sênior|senior|\bsr\b|pleno|especialista|tech lead|principal`.
4. Se a positiva bater, ela vence a de exclusão (títulos tipo "Júnior/Pleno"
   são vagas de entrada válidas).

#### Coleta na Gupy (dois passes por termo)

Para cada termo em `config/search_terms.yaml`:

- Passe A: `?jobName=<termo>&state=São Paulo&limit=100&offset=N`
- Passe B: `?jobName=<termo>&limit=100&offset=N`, mantendo apenas
  `workplaceType == "remote"`

Paginar enquanto `offset < pagination.total`, com teto de páginas por termo para
não estourar o tempo do runner.

#### Mensagem do Telegram (D2 + D14)

Uma mensagem por run agrupando as vagas novas. Por vaga: título, empresa, modelo
de trabalho, prazo (`applicationDeadline`), link e o texto de apresentação pronto
para colar, montado por template com os termos do stack que aquela vaga pediu.
Sem IA, sem chamada paga.

Chunking obrigatório: se o digest passar do limite de caracteres da API, quebrar
em mensagens sequenciais. O limite exato entra na lista de itens a confirmar.

#### Secrets (GitHub Actions)

`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `ADZUNA_APP_ID`, `ADZUNA_APP_KEY`.
Nunca em arquivo versionado.

## Child Issues

| # | Título | Prioridade | Esforço (humano / CC) | Depende de |
|---|---|---|---|---|
| 1 | Fundação + Gupy ponta a ponta (escopo enxuto) | Crítica | ~1 dia / ~25 min | — |
| 2 | Greenhouse + Lever atrás da mesma interface | Alta | ~1,5 dia / ~25 min | #1 |
| 3 | Adzuna + validação de `br` | Média | ~1 dia / ~20 min | #1 |
| 4 | Coleta Eureca | Alta | a estimar | #1 |
| 5 | Coleta Catho | Alta | a estimar | #1 |
| 6 | Coleta Hipsters.jobs | Alta | a estimar | #1 |
| 7 | Coleta Handshake | Alta | a estimar | #1 |
| X | Dedupe cross-source (hash canônico) | Baixa — não bloqueia #1, #2 ou #3 | ~2h / ~10 min | #1 |
| Y | Digest 2x/dia (collect/alert separados) | Baixa — não bloqueia #1, #2 ou #3 | ~4h / ~15 min | #1 |
| Z | Score ponderado (YAML por grupo) | Baixa — não bloqueia #1, #2 ou #3 | ~3h / ~10 min | #1 |

### Issue #1 — Fundação + Gupy ponta a ponta (escopo enxuto)

Corte deliberadamente menor que o desenho final do épico (regras D9/D10/D2 em
Implementation Details), para ter uma vaga real caindo no Telegram o mais rápido
possível. As issues #X, #Y e #Z fecham essa distância depois, sem bloquear esta
nem as issues #2 e #3.

1. **Dedupe.** Tabela SQLite `vagas` com `UNIQUE(source, external_id)` apenas.
   Sem hash canônico cross-source ainda — só existe uma fonte (Gupy) nesta issue.
2. **Orquestração.** Um único script `src/main.py`: busca na Gupy, checa
   `UNIQUE`, casa com o perfil, envia no Telegram **imediatamente** por vaga
   nova encontrada. Sem separação `collect`/`alert`, sem workflow duplo, sem
   agendamento de digest nesta issue.
3. **Matching.** Função simples que conta quantos termos de `MINHA_STACK`
   (lista fixa, sem pesos) aparecem em título + descrição da vaga; alerta se
   `count >= 1`. Sem YAML de score nesta issue.
4. **Critérios de aceite.** Rodar `uv run python -m src.main --debug`
   localmente busca vagas reais na Gupy, filtra por SP capital/híbrido/remoto,
   e imprime quais seriam enviadas — sem exigir token do Telegram configurado.
5. **Testes.** Cobrir dedupe (mesma `external_id` não dispara duas vezes) e
   matching (contagem de termos), com fixture real da resposta da Gupy salva em
   `tests/fixtures/`.
6. **Primeiro run (backfill).** O envio imediato por vaga (ponto 2) não tem
   espera entre mensagens. Num banco vazio, um run real pode encontrar dezenas
   de vagas de uma vez, e a API do Telegram tolera só ~1 msg/s por chat antes
   de devolver 429 (bloqueando novos envios pelo `retry_after`). Para não
   depender de lógica de rate-limit nesta issue, o primeiro run considera
   candidatas apenas vagas com `publishedDate` nas últimas 24h — reduz o
   volume do lote inicial sem tocar no design "um alerta por vaga achada".

### Issues #4-#7 — Novas fontes de coleta (Eureca, Catho, Hipsters.jobs, Handshake)

*Registradas no roadmap pela issue #4 (expansão de radar + auditoria, 2026-09-16).
Cada uma depende só de #1 pela interface `Scraper` e vira sua própria issue de
implementação — nenhum parser entra sem payload real capturado da fonte
(regra do projeto em `CLAUDE.md`).*

| # | Fonte | Observação |
|---|---|---|
| 4 | Eureca | Formato do feed a confirmar antes do parser |
| 5 | Catho | Formato do feed a confirmar antes do parser |
| 6 | Hipsters.jobs | Formato do feed a confirmar antes do parser |
| 7 | Handshake | Formato do feed a confirmar antes do parser |

**LinkedIn continua fora do escopo de scraping direto** (reforço do Out of Scope
abaixo): além de não ter API pública usável, a plataforma bloqueia scraping
ativamente por IP ban, o que inviabiliza um coletor confiável sem infraestrutura
de rotação de IP — fora do orçamento de custo zero (D13).

### Issue #X — Dedupe cross-source

*Não bloqueia #1, #2 ou #3. Depende de #1.*

Adicionar o `canonical_hash` (empresa|título|cidade normalizado, regra D10 em
Implementation Details) para unificar a mesma vaga vinda de duas fontes num
único alerta.

**Critério de aceite:** vaga idêntica vinda de Gupy e Greenhouse gera um único
alerta.

### Issue #Y — Digest 2x/dia

*Não bloqueia #1, #2 ou #3. Depende de #1.*

Separar `src/main.py` em `src/collect.py` (grava no banco) e `src/alert.py` (lê
o banco, monta digest, envia às 09h e 18h BRT), com dois workflows no GitHub
Actions substituindo o script único da issue #1.

**Critério de aceite:** os ACs 1, 8, 9 e 13 do épico (idempotência do collect,
digest único do alert, chunking, commit do `.db`) passam a valer.

### Issue #Z — Score ponderado

*Não bloqueia #1, #2 ou #3. Depende de #1.*

Trocar o matching simples da issue #1 (contagem de termos) pelo score YAML por
grupo (`config/matcher.yaml`, regra D9 em Implementation Details), com pesos
configuráveis por grupo, bônus por termo no título, e threshold de alerta
configurável.

**Critério de aceite:** pelo menos uma semana de dados reais das issues #1–#3
revisada antes de calibrar os pesos.

### Dependency Graph

```
#1 Fundacao + Gupy --+--> #2 Greenhouse + Lever
                     +--> #3 Adzuna
                     +--> #X Dedupe cross-source   (nao bloqueia #1/#2/#3)
                     +--> #Y Digest 2x/dia          (nao bloqueia #1/#2/#3)
                     +--> #Z Score ponderado        (nao bloqueia #1/#2/#3)
```

Sequência: #1 define a interface `Scraper`, o schema e o pipeline inteiro, no
recorte mínimo que já manda alerta real. #2 e #3 são independentes entre si e
viram só mais um parser. #3 pode travar em credencial, e por isso não é o
primeiro. #X, #Y e #Z fecham a distância entre o recorte enxuto de #1 e o
desenho final do épico (dedupe cross-source, digest agendado, score
ponderado) — rodam depois, sem bloquear o restante do épico.

## Acceptance Criteria

1. `uv run python -m src.collect` grava vagas novas em `vagas.db` e é idempotente:
   rodar duas vezes seguidas não cria linha duplicada.
2. Vaga com `workplaceType == "remote"` e `city == ""` **é aceita** pelo filtro
   geográfico (regressão do achado 2).
3. Vaga com `state == "Minas Gerais"` e `workplaceType == "hybrid"` é rejeitada.
4. Vaga cujo único termo é "AWS" no corpo da descrição **não** alerta (score 2 <
   threshold 4).
5. Vaga com `type == "vacancy_type_internship"` é classificada como
   `seniority = internship` sem depender do título.
6. Vaga já alertada não é reenviada: `alerted_at IS NOT NULL` a exclui da query.
7. Mesma vaga ingerida por duas fontes diferentes gera **um** alerta, não dois
   (mesmo `canonical_hash`).
8. `uv run python -m src.alert` envia uma única mensagem no Telegram por run,
   com digest agrupado, e marca `alerted_at` em todas as vagas enviadas.
9. Digest maior que o limite da API é quebrado em mensagens sequenciais, sem
   perder vaga.
10. Todo parser novo tem teste com payload real capturado da fonte, salvo em
    `tests/fixtures/`.
11. `uv run pytest` passa, sem teste pulado silenciosamente.
12. `uv run ruff check .` e `uv run ruff format --check .` passam limpos.
13. O workflow de coleta commita `vagas.db` de volta e o run seguinte enxerga o
    estado anterior.
14. Nenhum secret aparece em arquivo versionado nem em log do Actions.

## Testing Plan

| Camada | O quê | Qtd |
|---|---|---|
| Unit | `matcher.score()` nos 5 cenários da tabela de score | +5 |
| Unit | `matcher.geo_filter()`: remoto com city vazia, SP capital, outro estado | +3 |
| Unit | `matcher.seniority()`: campo `type`, regex positiva, regex de exclusão, título misto | +4 |
| Unit | `storage.canonical_hash()`: acento, caixa, sufixo societário, espaço duplo | +4 |
| Unit | `alerter.render()`: template do script, escaping, chunking no limite | +3 |
| Integration | Parser Gupy contra fixture real de `tests/fixtures/gupy_*.json` | +2 |
| Integration | Ciclo coleta→match→storage→alerta com Telegram fakeado | +2 |
| Integration | Idempotência: rodar coleta 2x, assertar contagem estável | +1 |
| Integration | Dedupe cross-source: mesmo hash de duas fontes, um alerta | +1 |

## Rollback Plan

- Falha de coleta: o workflow falha sem commitar o `.db`. Estado anterior intacto,
  próximo run em 4h tenta de novo.
- Alerta errado ou spam: desabilitar o workflow de alerta pelo Actions. A coleta
  segue populando o banco.
- Banco corrompido: `git checkout <sha> -- vagas.db`. É essa a vantagem de D6 sobre
  cache, o histórico é versionado.
- Matcher muito permissivo ou restritivo: ajustar `threshold` em
  `config/matcher.yaml`. Não exige deploy nem mudança de código.

## Effort Estimate

| Componente | Humano | CC + gstack |
|---|---|---|
| Setup toolchain (uv, pyproject, ruff, pytest, CI) | 3h | 8 min |
| `storage` (schema, upsert, dedupe, hash canônico) | 4h | 10 min |
| `scraper.gupy` (2 passes, paginação, fixtures) | 5h | 12 min |
| `matcher` (geo, senioridade, score, config) | 5h | 12 min |
| `alerter` (digest, template de script, chunking) | 4h | 10 min |
| Workflows do Actions (coleta, alerta, commit do db) | 3h | 8 min |
| `scraper.greenhouse` + `scraper.lever` | 6h | 15 min |
| `scraper.adzuna` + validação de `br` | 4h | 12 min |
| **Total** | **~34h** | **~1h30** |

## Files Reference

| Arquivo | Mudança |
|---|---|
| `pyproject.toml` | Novo: deps, config de ruff e pytest |
| `.python-version` | Novo: `3.13` |
| `config/matcher.yaml` | Novo: grupos, pesos, threshold |
| `config/search_terms.yaml` | Novo: termos de busca por fonte |
| `config/ats_companies.yaml` | Novo: empresas Greenhouse/Lever |
| `src/storage/schema.sql` | Novo: DDL acima |
| `src/storage/db.py` | Novo: upsert, dedupe, query de pendentes |
| `src/scraper/base.py` | Novo: interface `Scraper` |
| `src/scraper/gupy.py` | Novo: dois passes, paginação |
| `src/scraper/greenhouse.py` | Novo (issue #2) |
| `src/scraper/lever.py` | Novo (issue #2) |
| `src/scraper/adzuna.py` | Novo (issue #3) |
| `src/matcher/rules.py` | Novo: geo, senioridade, score |
| `src/alerter/telegram.py` | Novo: sendMessage, chunking |
| `src/alerter/templates.py` | Novo: template do script de candidatura |
| `.github/workflows/collect.yml` | Novo: cron 4/4h + commit do db |
| `.github/workflows/alert.yml` | Novo: cron 09:00 e 18:00 BRT |
| `tests/fixtures/` | Novo: payloads reais por fonte |

## Out of Scope

- Candidatura automática. Alto risco, quebra termos de uso de ATS, e tira seu
  controle sobre o que sai em seu nome.
- LinkedIn e Indeed. Bloqueiam scraping ativamente e não têm API pública usável.
- Dashboard ou interface web. O Telegram é a interface.
- Ranking com LLM ou embeddings. Adiciona custo por chamada e não-determinismo num
  matcher que precisa ser testável. Contraria a restrição de custo zero.
- Perfil de stack configurável por usuário. É um bot de um usuário só.
- Notificação por e-mail ou outro canal.

## Pré-requisitos (bloqueiam o início)

1. `uv python install 3.13` na máquina de dev (não há Python instalado).
2. Criar o repositório no GitHub e adicionar o remote (`git remote -v` está vazio
   hoje, então não há Actions nem issues).
3. Criar o bot no Telegram via @BotFather e obter `TELEGRAM_BOT_TOKEN` e
   `TELEGRAM_CHAT_ID`.
4. Criar conta gratuita na Adzuna e gerar `app_id`/`app_key` (bloqueia só a
   issue #3).
