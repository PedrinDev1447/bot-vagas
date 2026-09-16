from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Vaga:
    source: str
    external_id: str
    title: str
    company: str
    city: str
    state: str
    workplace_type: str
    url: str
    published_at: str | None
    application_deadline: str | None
    description: str
    # Dica de senioridade vinda direto da fonte (ex.: campo `type` da Gupy),
    # quando a fonte já distingue estágio por campo em vez de regex no título (D4).
    source_seniority_hint: str | None = None


class Scraper(ABC):
    source: str

    @abstractmethod
    def search(self, term: str) -> list[Vaga]:
        """Busca vagas para um termo, já aplicando o filtro geográfico da fonte."""
