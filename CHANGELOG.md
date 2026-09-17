# Changelog

Todas as mudanças notáveis deste projeto são documentadas aqui.

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/).

## [0.2.0.0] - 2026-09-17

### Added

- Coletor da Eureca (`src/scraper/eureca.py`): busca vagas paginando o
  endpoint `/opportunities`, filtra por termo no cliente (a API não oferece
  busca por palavra-chave) e normaliza os campos da fonte para o modelo
  interno (`workModel` → vocabulário `remote`/`hybrid`/`on-site`, sigla de
  estado → nome completo). Ainda não conectado ao pipeline principal
  (`src/main.py`) — issue de integração fica para um próximo ship.
- Roadmap de expansão de fontes documentado em `CLAUDE.md` e
  `specs/0001-bot-vagas-estagio-jr-sp.md`: Vagas.com.br, Catho, Cia de
  Talentos, Sólides Vagas, Cia de Estágios e EstágioTrainee somam-se aos
  alvos já previstos (Hipsters.jobs, Handshake).

### Changed

- "Out of Scope" do épico agora cobre LinkedIn, Indeed e Glassdoor
  explicitamente, com o motivo documentado (proteção anti-bot forte —
  Cloudflare, CAPTCHA — incompatível com a restrição de custo zero do
  projeto).
