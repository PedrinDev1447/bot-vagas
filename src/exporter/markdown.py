from pathlib import Path

from src.scraper.base import Vaga

ATS_EXPORT_PATH = "vagas_ats.md"


def append_ats_entry(
    vaga: Vaga,
    terms: list[str],
    seniority: str,
    vip: bool,
    path: str = ATS_EXPORT_PATH,
) -> None:
    """Append-only (spec 0002): nunca reescreve o arquivo, pra preservar
    checkboxes marcados manualmente pelo usuario no board de candidaturas.
    So deve ser chamado fora de --debug."""
    file_path = Path(path)
    is_new_file = not file_path.exists()

    terms_label = ", ".join(terms) if terms else "sem termo de stack (via empresa VIP)"
    vip_tag = " ⭐VIP" if vip else ""
    line = (
        f"- [ ] **[{vaga.title}]({vaga.url})** — {vaga.company} · "
        f"{vaga.workplace_type} · {seniority} · Termos: {terms_label}{vip_tag}\n"
    )

    with file_path.open("a", encoding="utf-8") as f:
        if is_new_file:
            f.write("# Vagas ATS\n\n")
        f.write(line)
