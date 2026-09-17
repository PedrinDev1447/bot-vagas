# VIP/blacklist de empresas, filtro de formação e export Markdown ATS

## Context

O matcher da issue #1 (`src/matcher/rules.py`) filtra por geografia, senioridade e
presença de termos de `MINHA_STACK` — sem noção de empresa. Duas lacunas do dev
solo que usa o bot:

1. Vagas de empresas de alto valor (bancos/fintechs consolidadas) podem não citar
   termos de `MINHA_STACK` no texto (ex.: vaga descreve "backend" sem citar "Java"
   explicitamente) e são descartadas silenciosamente, mesmo sendo vagas que ele
   quer ver sempre.
2. Vagas de estágio frequentemente travam elegibilidade a uma janela de
   formatura. O usuário se forma em 12/2027 e quer descartar automaticamente
   vagas cuja janela de formatura é estritamente anterior a essa data.

Além disso, o usuário quer um artefato de tracking pessoal (Markdown, formato de
checklist) com as vagas que passaram no match, para colar num board de
candidaturas — hoje o único output é o alerta efêmero no Telegram.

## Current State

Verificado em 2026-09-16, branch `feature/matcher-and-ats`:

| Item | Estado |
|---|---|
| `src/matcher/rules.py` | `MINHA_STACK` fixa (L9), `passes_geo_filter` (L35), `classify_seniority` (L44), `matched_stack_terms`/`is_stack_match` (L57-65), `within_backfill_window` (L68). Nenhuma noção de empresa ou formação. |
| `src/main.py:58-83` | Loop por vaga: geo → seniority → backfill → `is_stack_match` (obrigatório) → insert → send/mark_alerted. |
| `src/scraper/base.py` | `Vaga.company` já mapeia `careerPageName` da Gupy (ex.: `"Globalweb"`). |
| `src/storage/db.py` | Só tem `insert_vaga`/`mark_alerted`. Nenhuma função de leitura em massa (não precisamos de uma). |
| `src/alerter/telegram.py:8` | `format_message(vaga, matched_terms)` sempre assume `matched_terms` não-vazio. |
| `tests/fixtures/gupy_search_response.json` | Conferido: nenhum exemplo real de menção a data de formatura/conclusão. Os 3 trechos usados para desenhar o regex de formação vieram do usuário nesta conversa. |
| Export de vagas em Markdown | Não existe. |

## Proposed Change

Pipeline em `main.py`, dentro do loop `for vaga in candidates.values()`:

```
1. is_blacklisted(vaga)            -> reject (hard exclude, sempre)
2. passes_geo_filter(vaga)         -> como hoje
3. classify_seniority(vaga)        -> como hoje
4. within_backfill_window(vaga)    -> como hoje
5. passes_formacao_filter(vaga)    -> NOVO
6. matched_stack_terms(vaga)       -> como hoje
   is_vip(vaga)                    -> NOVO
   reject se not terms and not vip -> ALTERADO (VIP bypassa stack match)
7. insert_vaga (dedupe como hoje)
8. append_ats_entry(vaga, terms, vip)  -> NOVO, só fora de --debug
9. send_message / mark_alerted     -> como hoje
```

### Implementation Details

#### 1. VIP / Blacklist (`src/matcher/rules.py`)

```python
VIP_COMPANIES = [
    "itau",
    "itaú",
    "nubank",
    "mercado livre",
    "ifood",
    "stone",
    "xp",
    "inter",
    "quintoandar",
    "ambev tech",
    "aws",
    "microsoft",
    "google",
]
BLACKLIST_COMPANIES: list[str] = []


def _company_haystack(vaga: Vaga) -> str:
    return normalize(f"{vaga.company}\n{vaga.title}\n{vaga.description[:500]}")


def _matches_company_list(vaga: Vaga, companies: list[str]) -> bool:
    haystack = _company_haystack(vaga)
    return any(normalize(c) in haystack for c in companies)


def is_vip(vaga: Vaga) -> bool:
    return _matches_company_list(vaga, VIP_COMPANIES)


def is_blacklisted(vaga: Vaga) -> bool:
    return _matches_company_list(vaga, BLACKLIST_COMPANIES)
```

Match por substring normalizada (lowercase, sem acento) em `company` OU `title`
OU primeiros 500 caracteres de `description` — mitigação de slogan de carreira
estilizado (ex.: `#SANGUELARANJA`).

#### 2. Filtro de formação (`src/matcher/rules.py`)

```python
MINHA_FORMACAO_ANO = 2027
FORMACAO_KEYWORD_PATTERN = re.compile(r"formaca|formatura|conclu|formand")
FORMACAO_YEAR_PATTERN = re.compile(r"\b(20[2-3]\d)\b")
FORMACAO_WINDOW_CHARS = 100


def passes_formacao_filter(vaga: Vaga) -> bool:
    """Conservador: só rejeita se a description citar formatura/conclusão
    limitada a ano estritamente anterior a MINHA_FORMACAO_ANO. Sem menção
    ou ambíguo -> aceita (recall-first, D1 da spec 0001)."""
    text = normalize(vaga.description)
    years_found = [
        int(year)
        for match in FORMACAO_KEYWORD_PATTERN.finditer(text)
        for year in FORMACAO_YEAR_PATTERN.findall(
            text[match.end() : match.end() + FORMACAO_WINDOW_CHARS]
        )
    ]
    if not years_found:
        return True
    return max(years_found) >= MINHA_FORMACAO_ANO
```

Validado manualmente contra os 3 exemplos reais do usuário (todos passam, maior
ano ≥2027) e 2 casos de rejeição sintéticos derivados da regra que ele descreveu
(`"formatura até dez/2026"`, `"conclusão em 2025"` — ambos rejeitam, maior ano
<2027).

Exemplos reais fornecidos pelo usuário (viram fixture de teste):

1. `"Previsão de conclusão do curso: entre Dezembro/2026 e Dezembro/2027."`
2. `"Formação superior em andamento com previsão de formatura a partir de 12/2027."`
3. `"Disponibilidade para estagiar por pelo menos 1 ano (conclusão entre 2026 e 2027)."`

#### 3. Export Markdown ATS — `src/exporter/markdown.py` (módulo novo)

```python
ATS_EXPORT_PATH = "vagas_ats.md"


def append_ats_entry(vaga: Vaga, terms: list[str], vip: bool, path: str = ATS_EXPORT_PATH) -> None:
    """Append-only: nunca reescreve o arquivo, pra preservar checkboxes
    marcados manualmente pelo usuário. Só chamado fora de --debug."""
```

Formato por linha:
```
- [ ] **[ANALISTA DESENVOLVEDOR JAVA PL](https://...)** — Globalweb · hybrid · internship · Termos: java ⭐VIP
```
(`⭐VIP` só aparece quando `vip=True`; `Termos:` mostra
`sem termo de stack (via empresa VIP)` quando `terms` está vazio.)

#### 4. `format_message` (`src/alerter/telegram.py:8`)

Ganha parâmetro `vip: bool = False`. Não pode quebrar com `matched_terms` vazio
(hoje renderiza `"Match: "` em branco se uma vaga VIP sem termos chegar lá).

## Acceptance Criteria

1. Vaga de empresa em `BLACKLIST_COMPANIES` nunca gera alerta nem entra em
   `vagas_ats.md`, mesmo com stack match e formação ok.
2. Vaga de empresa em `VIP_COMPANIES` com `matched_stack_terms == []` ainda é
   alertada (bypassa o requisito de stack match), desde que passe
   geo/senioridade/backfill/formação.
3. Vaga com `description` citando `"conclusão entre 2026 e 2027"` passa no
   filtro de formação (ano 2027 presente).
4. Vaga com `description` citando `"formatura a partir de 12/2027"` passa no
   filtro de formação.
5. Vaga com `description` citando `"formatura até dez/2026"` (sem menção a
   2027 ou posterior) é rejeitada pelo filtro de formação.
6. Vaga com `description` citando `"conclusão em 2025"` é rejeitada.
7. Vaga com `description` sem nenhuma menção a formatura/conclusão passa no
   filtro (ambíguo = aceita).
8. Match de VIP/blacklist é case-insensitive e ignora acento (ex.: `"Itaú"`
   bate com `"itau"` na lista).
9. Match de VIP/blacklist funciona via `company`, `title` OU primeiros 500
   caracteres de `description`.
10. `vagas_ats.md` recebe uma linha nova por vaga nova matched, em modo append
    (rodar o bot 2x não duplica linha da mesma vaga, e não apaga linhas
    existentes).
11. Em `--debug`, `vagas_ats.md` não é tocado.
12. `uv run pytest` passa, `uv run ruff check .` e `uv run ruff format --check .`
    passam limpos.

## Testing Plan

| Camada | O quê | Qtd |
|---|---|---|
| Unit | `is_vip`/`is_blacklisted`: match por company, título, description[:500], acento/caixa | +4 |
| Unit | `passes_formacao_filter`: 3 exemplos reais (aceita) + 2 sintéticos (rejeita) + 1 sem menção (aceita) | +6 |
| Unit | `append_ats_entry`: cria arquivo se não existe, append preserva conteúdo anterior, formata VIP vs. termos vazios | +3 |
| Unit | `format_message` com `matched_terms=[]` e `vip=True` não quebra e não deixa "Match: " em branco | +1 |
| Integration | `main.run()`: vaga blacklisted não alerta; vaga VIP sem stack match alerta; vaga rejeitada por formação não alerta | +3 |

## Rollback Plan

- Regra de formação ou VIP/blacklist errada: ajustar as listas/constantes em
  `src/matcher/rules.py`. Não exige mudança de schema nem migração.
- `vagas_ats.md` corrompido ou com entradas erradas: `git checkout <sha> --
  vagas_ats.md` (mesmo padrão de recuperação de `vagas.db`, D6 da spec 0001).

## Effort Estimate

| Componente | CC + gstack |
|---|---|
| VIP/blacklist + testes | ~10 min |
| Filtro de formação + testes | ~12 min |
| Exporter Markdown + testes | ~12 min |
| Integração no `main.py` + testes de integração | ~10 min |

## Files Reference

| Arquivo | Mudança |
|---|---|
| `src/matcher/rules.py` | Novo: `VIP_COMPANIES`, `BLACKLIST_COMPANIES`, `is_vip`, `is_blacklisted`, `passes_formacao_filter` |
| `src/exporter/__init__.py` | Novo |
| `src/exporter/markdown.py` | Novo: `append_ats_entry` |
| `src/alerter/telegram.py:8` | `format_message` ganha parâmetro `vip` |
| `src/main.py:58-83` | Pipeline: blacklist early-reject, formação filter, VIP bypass, chamada ao exporter |
| `tests/test_matcher.py` | Novos testes de VIP/blacklist/formação |
| `tests/test_exporter.py` | Novo |

## Out of Scope

- YAML de configuração para VIP/blacklist/formação (fica pro padrão de
  `config/matcher.yaml` já previsto na issue #Z da spec 0001, quando o score
  ponderado chegar).
- Parsers de ATS Greenhouse/Lever (issue #2 da spec 0001) — este export é um
  arquivo de tracking pessoal, não um scraper de fonte.
- Detecção de mês de formatura (só ano é comparado, conforme regra do usuário).
- Sincronizar/desduplicar `vagas_ats.md` se o usuário editar manualmente e o
  bot reordenar — append simples, sem merge inteligente.
