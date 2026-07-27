"""Generador de las paginas de `/docs/` de las 5 landings de la familia
Libra -- extraido 2026-07-27 de las 82 paginas HTML reales (19 Contalibra,
23 Restolibra, 12 Gestiolibra, 16 MedLibra, 12 VentaLibra), que repetian
inline el mismo navbar+sidebar+footer en cada archivo, sin ningun paso de
build. Ver wiki/analyses/auditoria-duplicacion-familia-libra.md.

Arquitectura: una sola plantilla Jinja2 (`templates/docs_page.html.jinja2`)
+ el sidebar/branding de cada sitio (`docs_sidebars.SIDEBARS`, un solo
sidebar por sitio -- confirmado identico en las paginas de un mismo sitio
salvo el link activo) + el contenido real de cada pagina, guardado como
fragmento HTML crudo en `docs_content/<sitio>/<archivo>.html` (no se
reescribio el contenido, se extrajo tal cual del `<main class="docs-content">`
de cada archivo original).
"""
from importlib import resources

from jinja2 import Environment, FileSystemLoader, select_autoescape

from libra_web_kit.docs_pages import PAGES
from libra_web_kit.docs_sidebars import SIDEBARS

_TEMPLATES_DIR = resources.files("libra_web_kit").joinpath("templates")
_CONTENT_DIR = resources.files("libra_web_kit").joinpath("docs_content")

_env = Environment(
    loader=FileSystemLoader(str(_TEMPLATES_DIR)),
    autoescape=select_autoescape(enabled_extensions=()),  # el contenido ya es HTML de confianza (extraido, no user input)
    trim_blocks=True,
    lstrip_blocks=True,
)


def list_pages(site: str) -> list[str]:
    if site not in PAGES:
        raise KeyError(f"sitio desconocido: {site!r} (conocidos: {sorted(PAGES)})")
    return sorted(PAGES[site])


def render(site: str, filename: str) -> str:
    """Renderiza una pagina de /docs/ completa (HTML final, listo para
    escribir a disco)."""
    if site not in PAGES:
        raise KeyError(f"sitio desconocido: {site!r} (conocidos: {sorted(PAGES)})")
    if filename not in PAGES[site]:
        raise KeyError(f"{site}: pagina desconocida {filename!r} (conocidas: {sorted(PAGES[site])})")

    meta = PAGES[site][filename]
    site_cfg = SIDEBARS[site]
    content_path = _CONTENT_DIR / site / filename
    content_html = content_path.read_text(encoding="utf-8").rstrip("\n")

    template = _env.get_template("docs_page.html.jinja2")
    return template.render(
        title=meta["title"],
        description=meta["description"],
        is_index=meta["is_index"],
        active_href=meta["active_href"],
        brand=site_cfg["brand"],
        letter=site_cfg["letter"],
        sidebar=site_cfg["sidebar"],
        footer_html=site_cfg["footer_html"],
        content_html=content_html,
    )


def render_all() -> dict[str, dict[str, str]]:
    """{sitio: {archivo: html}} para los 5 sitios completos (82 paginas)."""
    return {site: {fname: render(site, fname) for fname in list_pages(site)} for site in PAGES}
