# Fix: falso positivo de substring em VIP/blacklist e VIP sem filtro de área

## Context

Dois bugs encontrados pelo usuário rodando o bot com dados reais (2026-09-16,
primeiro run real depois da Spec 0002):

1. `_matches_company_list` (`src/matcher/rules.py`) faz `normalize(company) in
   haystack` — substring simples. Nomes curtos de `VIP_COMPANIES` colidem com
   palavras comuns em português/inglês: `"inter"` bate dentro de `"interesse"`
   e `"intern"`; `"xp"` bate dentro de `"experiência"`. Vagas de empresas
   não-VIP estão sendo marcadas como VIP.
2. `is_vip` bypassa `matched_stack_terms` (comportamento pretendido pela Spec
   0002), mas nada no pipeline exige que a vaga seja da área de TI/Dev. Uma
   vaga "Estágio | Trabalhista" (Direito) do Itaú foi alertada só por a
   empresa ser VIP — sem nenhuma checagem de cargo/área.

## Current State

Verificado em 2026-09-16, branch `feature/matcher-and-ats` (commit `531542e`,
que já inclui a Spec 0002 mergeada nesta branch):

| Item | Estado |
|---|---|
| `src/matcher/rules.py:_matches_company_list` (spec 0002) | `any(normalize(c) in haystack for c in companies)` — substring puro, sem word boundary. |
| `src/main.py:61-92` | Pipeline: blacklist → geo → seniority → backfill → formação → (`terms` ou `is_vip`) → insert/alerta. Nenhuma checagem de área/cargo no título. |
| `is_it_title` ou equivalente | Não existe. |

## Proposed Change

### 1. `_matches_company_list` com word boundary

```python
def _matches_company_list(vaga: Vaga, companies: list[str]) -> bool:
    haystack = _company_haystack(vaga)
    return any(
        re.search(rf"\b{re.escape(normalize(company))}\b", haystack) is not None
        for company in companies
    )
```

Aplica-se a todos os termos (não só os curtos) — mais simples de manter que
uma lista de exceção, e não tem efeito colateral em nomes com mais de uma
palavra (`\b` respeita espaço como fronteira também).

### 2. `is_it_title` — novo filtro de área, obrigatório pra todas as vagas

```python
IT_TITLE_KEYWORDS = [
    "desenvolvedor",
    "developer",
    "software",
    "backend",
    "frontend",
    "fullstack",
    "mobile",
    "programador",
    "dados",
    "ti",
    "tecnologia",
]


def is_it_title(vaga: Vaga) -> bool:
    title = normalize(vaga.title)
    return any(
        re.search(rf"\b{re.escape(term)}\b", title) is not None for term in IT_TITLE_KEYWORDS
    )
```

Lista literal fornecida pelo usuário nesta conversa — sem termo adicional.

### 3. Pipeline em `main.py`

`is_it_title(vaga)` vira early-reject **antes** da checagem de `terms`/`vip`,
aplicado a toda vaga, inclusive VIP. VIP continua bypassando só
`matched_stack_terms`; nunca bypassa `is_it_title`.

```
1. is_blacklisted(vaga)     -> reject
2. is_it_title(vaga)        -> reject (NOVO — vale pra VIP tambem)
3. passes_geo_filter(vaga)  -> como hoje
4. classify_seniority(vaga) -> como hoje
5. within_backfill_window   -> como hoje
6. passes_formacao_filter   -> como hoje
7. terms / is_vip           -> como hoje (VIP so bypassa isso)
```

## Acceptance Criteria

1. Vaga de empresa não-VIP com `"interesse"` ou `"experiência"` na
   description **não** é marcada como VIP.
2. Vaga de empresa não-VIP com título contendo `"Internship"`/`"Intern"` não
   bate `"inter"` (Banco Inter) na blacklist/VIP.
3. Vaga com `company="Banco Inter"` (ou variação que contenha a palavra
   isolada `"inter"`) continua sendo corretamente identificada como VIP.
4. Vaga `"Estágio | Trabalhista"` na empresa Itaú (VIP) é **rejeitada** —
   não gera alerta nem entrada no `vagas_ats.md`.
5. Vaga `"Estágio em Desenvolvimento de Software"` de empresa VIP sem termo
   de `MINHA_STACK` no texto continua sendo alertada (bypass de stack
   preservado, só a área é exigida agora).
6. Vaga `"Desenvolvedor Java Junior"` (não-VIP) continua funcionando como
   antes — `is_it_title` não quebra o caminho normal de match por stack.
7. `uv run pytest`, `uv run ruff check .` e `uv run ruff format --check .`
   passam limpos.

## Testing Plan

| Camada | O quê | Qtd |
|---|---|---|
| Unit | `_matches_company_list`/`is_vip`: `"inter"` não bate em `"interesse"`/`"intern"`, `"xp"` não bate em `"experiência"`, mas bate como palavra isolada | +4 |
| Unit | `is_it_title`: aceita cada termo da lista, rejeita título sem nenhum termo (`"Estágio \| Trabalhista"`) | +3 |
| Integration | `main.run()`: vaga VIP com título fora de TI é rejeitada; vaga VIP com título de TI e sem stack term ainda alerta | +2 |

## Files Reference

| Arquivo | Mudança |
|---|---|
| `src/matcher/rules.py` | `_matches_company_list` com regex word-boundary; nova `IT_TITLE_KEYWORDS` + `is_it_title` |
| `src/main.py` | Novo early-reject `is_it_title` no pipeline, antes da checagem de stack/VIP |
| `tests/test_matcher.py` | Testes de word-boundary e de `is_it_title` |
| `tests/test_main.py` | Teste de integração: VIP fora de área é rejeitado; ajuste no teste existente de VIP-bypass pra usar título de TI |

## Out of Scope

- Lista de `IT_TITLE_KEYWORDS` configurável via YAML (mesmo padrão das outras
  listas — fica pra quando `config/matcher.yaml` existir).
- Aplicar `is_it_title` sobre a `description` além do título (usuário pediu
  explicitamente "apenas se o título tiver").
