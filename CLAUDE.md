# bot-vagas

## Visão geral

Bot que coleta vagas de estágio e júnior na região de São Paulo, filtra por match
com o perfil do dev e alerta via Telegram quando a stack da vaga bate com o perfil.

Fluxo: coleta (scraper) -> normalização/persistência (storage) -> match por stack
(matcher) -> alerta no Telegram (alerter), sem reenviar vaga já notificada.

Perfil de referência para match: Java, Spring Boot, React, TypeScript, AWS.

## Stack técnica

- **Python** — linguagem principal
- **GitHub Actions** — agendamento e execução das coletas
- **SQLite** — persistência de vagas e controle de deduplicação
- **Telegram Bot API** — canal de alerta
- **pytest** — testes
- **ruff** — lint e formatação

## Estrutura

```
.github/workflows/   agendamento das coletas
specs/               especificações (uma por feature, escritas antes do código)
src/scraper/         coletores por fonte
src/matcher/         regras de match de stack
src/alerter/         envio de alertas no Telegram
src/storage/         schema SQLite, dedupe e queries
tests/               testes (pytest)
docs/                documentação de release e decisões
```

## Regras do projeto

1. **Nunca inventar campo de API ou estrutura de HTML.** Todo campo de resposta de
   API e todo seletor de HTML precisa ser confirmado antes via graphify ou leitura
   real da fonte (response capturada, página baixada, documentação oficial). Se não
   deu para confirmar, pergunte — não chute nome de campo, tipo ou caminho.
2. **Todo parser novo nasce com teste.** Nenhum parser entra sem teste cobrindo pelo
   menos um payload/HTML real capturado da fonte.
3. **Rodar `pytest` e `ruff` antes de considerar qualquer tarefa concluída.** Tarefa
   só é "pronta" com os dois passando; se falharem, reporte a saída em vez de
   declarar conclusão.
4. **Spec antes de implementar.** Ver seção gstack abaixo.

## gstack

Este projeto usa o gstack. Use os comandos:

- `/office-hours` — discutir direção do produto e priorização
- `/spec` — transformar intenção vaga em especificação executável
- `/plan-eng-review` — revisão do plano em modo eng manager
- `/review` — revisão do diff antes de landar
- `/ship` — rodar testes, revisar diff, versionar, commitar, abrir PR
- `/document-release` — documentação pós-ship
- `/qa` — QA sistemático com correção dos bugs encontrados
- `/careful` — guardrails para comandos destrutivos

**Nunca pular a spec antes de implementar.** Toda feature começa em `/spec`, com a
especificação gravada em `specs/`, e só depois vai para plano e código.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).

## Skill routing

When the user's request matches an available skill, invoke it via the Skill tool. When in doubt, invoke the skill.

Key routing rules:
- Product ideas/brainstorming → invoke /office-hours
- Strategy/scope → invoke /plan-ceo-review
- Architecture → invoke /plan-eng-review
- Design system/plan review → invoke /design-consultation or /plan-design-review
- Full review pipeline → invoke /autoplan
- Bugs/errors → invoke /investigate
- QA/testing site behavior → invoke /qa or /qa-only
- Code review/diff check → invoke /review
- Visual polish → invoke /design-review
- Ship/deploy/PR → invoke /ship or /land-and-deploy
- Save progress → invoke /context-save
- Resume context → invoke /context-restore
- Author a backlog-ready spec/issue → invoke /spec
