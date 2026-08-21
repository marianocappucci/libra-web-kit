"""La guarda que impide que el generador deje paginas huerfanas.

🔴 **El caso real, y por eso existe.** `libradesk_web` tiene 21 archivos en
`public/docs/` y el kit conoce 15: alguien escribio `recorrido.html`,
`agenda.html`, `stock.html`, `compras.html`, `facturacion.html` y
`ventas-cobranzas.html` **en el repo generado** en vez de en `docs_content/`.

Sin la guarda, correr `generate_docs.py` por cualquier otro motivo —agregar un
sitio nuevo, por ejemplo— reescribe las 15 paginas que el kit SI conoce, con un
sidebar que no menciona a las otras 6. Las 6 siguen en el disco y **sin ningun
link que lleve a ellas**: no hay error, no hay 404, y el unico sintoma es
documentacion publicada que el cliente ya no encuentra.

Paso dos veces en la misma sesion (2026-08-20/21) antes de que esto existiera.
"""
import importlib.util
from pathlib import Path

import pytest

from libra_web_kit.docs_pages import PAGES

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
SITIO = "libraclub"


@pytest.fixture
def generate_docs():
    spec = importlib.util.spec_from_file_location("generate_docs", SCRIPTS / "generate_docs.py")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


@pytest.fixture
def falso_repo(tmp_path, generate_docs):
    """Un `proyectos-dir` de mentira con un solo sitio adentro."""
    docs = tmp_path / generate_docs.REPO_DIR_BY_SITE[SITIO] / "public" / "docs"
    docs.mkdir(parents=True)
    return tmp_path, docs


def _correr(generate_docs, raiz, monkeypatch, *, forzar=False):
    argv = ["generate_docs.py", "--proyectos-dir", str(raiz)]
    if forzar:
        argv.append("--forzar-divergentes")
    monkeypatch.setattr("sys.argv", argv)
    return generate_docs.main()


def test_un_sitio_alineado_se_escribe(generate_docs, falso_repo, monkeypatch, capsys):
    """El control positivo. Sin el, un generador que no escribiera NUNCA
    pasaria el test de la guarda igual."""
    raiz, docs = falso_repo
    assert _correr(generate_docs, raiz, monkeypatch) == 0
    escritas = sorted(p.name for p in docs.iterdir())
    assert escritas == sorted(PAGES[SITIO]), capsys.readouterr().out


def test_una_pagina_desconocida_saltea_el_sitio_entero(generate_docs, falso_repo, monkeypatch, capsys):
    """Y no escribe **ninguna**: el problema no es la pagina de mas, es que las
    otras quedarian regeneradas con un sidebar que no la nombra."""
    raiz, docs = falso_repo
    (docs / "recorrido.html").write_text("la pagina que alguien escribio acá", encoding="utf-8")

    assert _correr(generate_docs, raiz, monkeypatch) == 0
    salida = capsys.readouterr().out
    assert "[SALTEADO]" in salida
    assert "recorrido.html" in salida
    # Lo que importa: no escribio nada mas.
    assert sorted(p.name for p in docs.iterdir()) == ["recorrido.html"]
    assert (docs / "recorrido.html").read_text(encoding="utf-8").startswith("la pagina")


def test_forzar_divergentes_escribe_igual(generate_docs, falso_repo, monkeypatch):
    """La salida de emergencia sigue existiendo, y sigue sin borrar la pagina
    de mas — la deja huerfana, que es exactamente lo que la guarda avisa."""
    raiz, docs = falso_repo
    (docs / "recorrido.html").write_text("la pagina que alguien escribio acá", encoding="utf-8")

    assert _correr(generate_docs, raiz, monkeypatch, forzar=True) == 0
    escritas = sorted(p.name for p in docs.iterdir())
    assert escritas == sorted([*PAGES[SITIO], "recorrido.html"])
