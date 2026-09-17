# TODOS

## Scraper — Eureca

### Eliminar duplicação de `_normalize()` entre scraper e matcher

**What:** `src/scraper/eureca.py:_normalize()` duplica a lógica de
`src/matcher/rules.py:normalize()` (NFKD decompose + strip de acento +
lowercase).

**Why:** Manter a mesma lógica em dois lugares significa que uma correção
futura (ex.: um caractere Unicode não coberto) precisa ser aplicada duas
vezes, ou os dois módulos divergem silenciosamente.

**Context:** A duplicação foi deliberada — evita que `src/scraper/` dependa
de `src/matcher/`, seguindo o mesmo padrão de independência do
`GupyScraper`. Se uma terceira fonte precisar da mesma normalização, mover
a função para um módulo compartilhado (ex.: `src/scraper/base.py` ou um novo
`src/shared/text.py`) que scraper e matcher importem, sem criar acoplamento
scraper → matcher.

**Effort:** S
**Priority:** P3
**Depends on:** None

### Validar shape do payload da API da Eureca antes de indexar

**What:** `parse_eureca_opportunity()` acessa `raw["id"]`, `raw["name"]`,
`raw["companyName"]`, `raw["description"]` diretamente, sem checar tipo ou
presença antes de indexar.

**Why:** Se a API mudar o formato da resposta sem aviso, o scraper quebra
com `KeyError`/`TypeError` não tratado em vez de uma falha clara e
recuperável.

**Context:** Mesmo padrão do `GupyScraper` (também sem validação de schema)
— não é uma regressão introduzida pela Eureca especificamente. Vale revisar
se/quando o bot passar a rodar sem supervisão direta (ex.: alertas de falha
separados do log de auditoria).

**Effort:** M
**Priority:** P3
**Depends on:** None

### Logar quando `_fetch_all` bate no teto de `MAX_PAGES`

**What:** `EurecaScraper._fetch_all()` para silenciosamente ao atingir
`MAX_PAGES` (25 páginas), sem diferenciar "paginação instável" de "mais de
200 vagas abertas de verdade".

**Why:** Projeto é recall-first (D1, `specs/0001`) — um truncamento real
descartaria vagas válidas sem nenhum sinal no log de auditoria explicando
por quê.

**Context:** Achado do adversarial review (2026-09-17). O fix em si é
trivial (log de warning quando o loop esgota sem `len(items) >= total`), mas
onde esse aviso deve aparecer (stdout do GitHub Actions? log de auditoria
existente? outro canal?) é uma decisão de produto, não algo pra decidir
dentro do módulo do scraper isoladamente.

**Effort:** S
**Priority:** P2
**Depends on:** None

### Confirmar se HTML na `description` da Eureca afeta o matcher

**What:** `Vaga.description` da Eureca vem com HTML bruto (`<p>`, `<strong>`,
etc.), diferente de Gupy que vem com texto + entidades HTML soltas
(`&amp;`, `&nbsp;`). O matcher (`matched_core_terms`,
`matched_adjacent_terms`, `passes_formacao_filter`) varre `description`
diretamente por substring.

**Why:** Tags HTML dentro da janela de caracteres usada por
`passes_formacao_filter` (`FORMACAO_WINDOW_CHARS`) podem deslocar quanto
texto real é inspecionado, ou um termo de stack pode ficar dividido por uma
tag.

**Context:** Achado do adversarial review (2026-09-17). Efeito líquido tende
a ser mais falso-aceite, não descarte silencioso — consistente com a
filosofia recall-first do projeto, então severidade baixa. Vale confirmar
que isso foi decisão consciente (ou stripar HTML no parser) antes de plugar
a Eureca no pipeline principal.

**Effort:** S
**Priority:** P3
**Depends on:** None

## Completed
