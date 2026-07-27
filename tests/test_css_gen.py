"""Tests para libra_web_kit.css_gen -- extraido 2026-07-27 de los 5
`style.css` de las landings (Contalibra, Restolibra, Gestiolibra,
MedLibra, VentaLibra), que eran copy-paste ~88-96% identico. Ver
wiki/analyses/auditoria-duplicacion-familia-libra.md.

Los dos fixtures `tests/fixtures/*_style.css.golden` son copias exactas
de lo que esos dos sitios tenian desplegado antes de esta extraccion --
protegen contra una regresion futura del template/tokens sin depender
de que los 5 repos hermanos esten clonados (no lo estan en CI)."""
from pathlib import Path

import pytest

from libra_web_kit.css_gen import render, render_all
from libra_web_kit.site_css_tokens import SITES

FIXTURES = Path(__file__).parent / "fixtures"


def test_render_all_covers_every_site():
    rendered = render_all()
    assert set(rendered) == set(SITES)


@pytest.mark.parametrize("site", sorted(SITES))
def test_render_has_no_leftover_markers(site):
    css = render(site)
    assert "@@" not in css, f"{site}: quedaron marcadores de slot sin reemplazar"


@pytest.mark.parametrize("site", sorted(SITES))
def test_render_is_structurally_balanced(site):
    css = render(site)
    assert css.count("{") == css.count("}")
    # Los 13 tokens que nunca varian por sitio tienen que seguir ahi.
    for token in ("--white:", "--radius:", "--shadow:", "--shadow-sm:"):
        assert token in css


def test_render_matches_original_bytes_contalibra():
    golden = (FIXTURES / "contalibra_style.css.golden").read_text(encoding="utf-8")
    assert render("contalibra") == golden


def test_render_matches_original_bytes_restolibra():
    golden = (FIXTURES / "restolibra_style.css.golden").read_text(encoding="utf-8")
    assert render("restolibra") == golden


def test_render_unknown_site_raises():
    with pytest.raises(KeyError):
        render("no-existe")
