"""Los dos scripts de generacion tienen que conocer TODOS los sitios.

🔴 Agregar un sitio son dos mitades: los datos (`site_css_tokens.SITES` y
`docs_pages.PAGES`) y el destino donde escribirlos
(`REPO_DIR_BY_SITE` de cada script). Olvidarse de la segunda **no da error**
en `generate_css.py`: el `for` recorre lo renderizado y `REPO_DIR_BY_SITE[site]`
levanta `KeyError` recien al llegar a ese sitio, despues de haber escrito los
anteriores. Y en `--check`, un sitio que nunca se mira sale en verde.

Escrito el 2026-08-20 al sumar LibraCargo y LibraClub, que fueron los primeros
sitios agregados despues de la extraccion original — o sea, los primeros que
pudieron caer en esta trampa.

Los scripts no son un paquete importable (`scripts/` no tiene `__init__.py` y
no esta en el `pyproject`), asi que se cargan por ruta.
"""
import importlib.util
from pathlib import Path

import pytest

from libra_web_kit.docs_pages import PAGES
from libra_web_kit.site_css_tokens import SITES

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"


def _cargar(nombre: str):
    spec = importlib.util.spec_from_file_location(nombre, SCRIPTS / f"{nombre}.py")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


@pytest.mark.parametrize(
    "script,fuente,como_se_llama",
    [
        ("generate_css", SITES, "site_css_tokens.SITES"),
        ("generate_docs", PAGES, "docs_pages.PAGES"),
    ],
)
def test_todos_los_sitios_tienen_repo_destino(script, fuente, como_se_llama):
    destinos = _cargar(script).REPO_DIR_BY_SITE
    faltan = sorted(set(fuente) - set(destinos))
    assert not faltan, (
        f"{script}.py no sabe donde escribir {faltan} — estan en {como_se_llama} "
        f"pero no en REPO_DIR_BY_SITE"
    )


@pytest.mark.parametrize("script", ["generate_css", "generate_docs"])
def test_no_hay_destinos_de_sitios_que_no_existen(script):
    """La contracara: un destino sin datos es un repo que nadie va a escribir
    nunca. No rompe, pero deja creyendo que ese sitio se genera desde el kit."""
    destinos = _cargar(script).REPO_DIR_BY_SITE
    conocidos = set(SITES) | set(PAGES)
    sobran = sorted(set(destinos) - conocidos)
    assert not sobran, f"{script}.py apunta a sitios que no existen: {sobran}"
