# Graph Report - bot-vagas  (2026-09-16)

## Corpus Check
- 13 files · ~14,965 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 33 nodes · 32 edges · 5 communities (4 shown, 1 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b75bb8a2`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Épico: bot de vagas de estágio/jr em SP com alerta no Telegram
- Implementation Details
- Child Issues
- Evidência coletada das fontes (2026-09-15)
- Proposed Change

## God Nodes (most connected - your core abstractions)
1. `Épico: bot de vagas de estágio/jr em SP com alerta no Telegram` - 13 edges
2. `Implementation Details` - 9 edges
3. `Child Issues` - 6 edges
4. `Evidência coletada das fontes (2026-09-15)` - 5 edges
5. `Proposed Change` - 3 edges
6. `Context` - 1 edges
7. `Current State` - 1 edges
8. `Gupy — confirmado, HTTP 200, sem autenticação` - 1 edges
9. `Adzuna — parcialmente confirmado` - 1 edges
10. `Greenhouse / Lever — não probados ainda` - 1 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities (5 total, 1 thin omitted)

### Community 0 - "Épico: bot de vagas de estágio/jr em SP com alerta no Telegram"
Cohesion: 0.18
Nodes (10): Acceptance Criteria, Context, Current State, Effort Estimate, Files Reference, Out of Scope, Pré-requisitos (bloqueiam o início), Rollback Plan (+2 more)

### Community 1 - "Implementation Details"
Cohesion: 0.22
Nodes (9): Coleta na Gupy (dois passes por termo), Filtro de senioridade (D4), Filtro geográfico (D3), Implementation Details, Mensagem do Telegram (D2 + D14), Regra de dedupe (D10), Regra de match (D9) — `config/matcher.yaml`, Schema SQLite (+1 more)

### Community 2 - "Child Issues"
Cohesion: 0.33
Nodes (6): Child Issues, Dependency Graph, Issue #1 — Fundação + Gupy ponta a ponta (escopo enxuto), Issue #X — Dedupe cross-source, Issue #Y — Digest 2x/dia, Issue #Z — Score ponderado

### Community 3 - "Evidência coletada das fontes (2026-09-15)"
Cohesion: 0.40
Nodes (5): Adzuna — parcialmente confirmado, Evidência coletada das fontes (2026-09-15), Greenhouse / Lever — não probados ainda, Gupy — confirmado, HTTP 200, sem autenticação, Itens NÃO confirmados (validar antes de implementar)

## Knowledge Gaps
- **27 isolated node(s):** `Context`, `Current State`, `Gupy — confirmado, HTTP 200, sem autenticação`, `Adzuna — parcialmente confirmado`, `Greenhouse / Lever — não probados ainda` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Épico: bot de vagas de estágio/jr em SP com alerta no Telegram` connect `Épico: bot de vagas de estágio/jr em SP com alerta no Telegram` to `Child Issues`, `Evidência coletada das fontes (2026-09-15)`, `Proposed Change`?**
  _High betweenness centrality (0.839) - this node is a cross-community bridge._
- **Why does `Proposed Change` connect `Proposed Change` to `Épico: bot de vagas de estágio/jr em SP com alerta no Telegram`, `Implementation Details`?**
  _High betweenness centrality (0.462) - this node is a cross-community bridge._
- **Why does `Implementation Details` connect `Implementation Details` to `Proposed Change`?**
  _High betweenness centrality (0.444) - this node is a cross-community bridge._
- **What connects `Context`, `Current State`, `Gupy — confirmado, HTTP 200, sem autenticação` to the rest of the system?**
  _27 weakly-connected nodes found - possible documentation gaps or missing edges._