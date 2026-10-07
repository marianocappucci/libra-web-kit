"""Favicon (icono plano) y marca del navbar/pie de las paginas que genera el kit."""
import importlib.util
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from libra_web_kit.docs_gen import list_pages, render as render_doc
from libra_web_kit.docs_sidebars import SIDEBARS
from libra_web_kit.favicon_gen import LADO, PROPORCION_ICONO, RADIO, favicon_svg, render_all
from libra_web_kit.iconos_bootstrap import TRAZOS
from libra_web_kit.identidad import IDENTIDAD, marca_icono_html, nombre_icono
from libra_web_kit.legal_gen import render as render_legal

SVG_NS = "{http://www.w3.org/2000/svg}"
SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"


@pytest.mark.parametrize("site", sorted(IDENTIDAD))
def test_el_svg_es_xml_valido_con_cuadrado_del_color_e_icono_blanco(site):
    raiz = ET.fromstring(favicon_svg(site))
    assert raiz.tag == f"{SVG_NS}svg"
    assert raiz.get("viewBox") == f"0 0 {LADO} {LADO}"

    rect = raiz.find(f"{SVG_NS}rect")
    assert rect.get("fill") == IDENTIDAD[site].color
    assert int(rect.get("rx")) == RADIO
    # ~22 % del lado, como pide el documento de identidad.
    assert 0.21 <= RADIO / LADO <= 0.23

    grupo = raiz.find(f"{SVG_NS}g")
    assert grupo.get("fill") == "#fff"
    trazos = TRAZOS[nombre_icono(site)]
    paths = grupo.findall(f"{SVG_NS}path")
    assert [p.get("d") for p in paths] == [d for d, _ in trazos]


@pytest.mark.parametrize("site", sorted(IDENTIDAD))
def test_el_icono_va_centrado_y_ocupa_el_60_por_ciento(site):
    grupo = ET.fromstring(favicon_svg(site)).find(f"{SVG_NS}g")
    transform = grupo.get("transform")
    assert transform == "translate(12.8 12.8) scale(2.4)"
    # 16 (grilla de Bootstrap Icons) * 2.4 = 38.4 = 60 % de 64; margen = (64 - 38.4) / 2.
    assert 16 * 2.4 == pytest.approx(LADO * PROPORCION_ICONO)
    assert 12.8 * 2 + 38.4 == pytest.approx(LADO)


def test_cup_hot_conserva_su_fill_rule():
    assert 'fill-rule="evenodd"' in favicon_svg("restolibra")
    assert "fill-rule" not in favicon_svg("libracargo")


def test_los_ocho_favicons_son_distintos_y_deterministas():
    todos = render_all()
    assert len(set(todos.values())) == 8
    assert todos == render_all()


def test_sitio_desconocido():
    with pytest.raises(KeyError):
        favicon_svg("no-existe")


@pytest.mark.parametrize("site", sorted(SIDEBARS))
def test_las_paginas_de_docs_muestran_el_icono_y_no_la_inicial(site):
    html = render_doc(site, list_pages(site)[0])
    assert f'<div class="logo-icon">{marca_icono_html(site)}</div>' in html
    assert 'rel="icon" type="image/svg+xml" href="/img/favicon.svg"' in html


@pytest.mark.parametrize("site", sorted(SIDEBARS))
def test_la_pagina_legal_muestra_el_icono_y_no_la_inicial(site):
    html = render_legal(site)
    assert f'<div class="logo-icon">{marca_icono_html(site)}</div>' in html
    assert 'rel="icon" type="image/svg+xml" href="/img/favicon.svg"' in html


@pytest.mark.parametrize("site", sorted(SIDEBARS))
def test_ningun_footer_queda_con_marcador_ni_con_inicial(site):
    footer = SIDEBARS[site]["footer_html"]
    assert "@@" not in footer
    if "logo-icon" in footer:
        assert marca_icono_html(site) in footer


def _script():
    spec = importlib.util.spec_from_file_location("generate_favicon", SCRIPTS / "generate_favicon.py")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


HOME_OK = (
    '<link rel="icon" type="image/svg+xml" href="/img/favicon.svg">\n'
    '<div class="logo-icon"><i class="bi bi-truck"></i></div>\n'
    '<div class="logo-icon" style="width:28px"><i class="bi bi-truck"></i></div>\n'
)


def test_home_alineada_no_da_problemas():
    assert _script().problemas_de_la_home("libracargo", HOME_OK) == []


def test_home_con_inicial_o_sin_favicon_da_problemas():
    script = _script()
    con_inicial = HOME_OK.replace('<i class="bi bi-truck"></i>', "C")
    assert any("deberia decir" in p for p in script.problemas_de_la_home("libracargo", con_inicial))
    sin_favicon = HOME_OK.replace('<link rel="icon" type="image/svg+xml" href="/img/favicon.svg">', "")
    assert any("favicon" in p for p in script.problemas_de_la_home("libracargo", sin_favicon))
    sin_pie = HOME_OK.rsplit('<div class="logo-icon"', 1)[0]
    assert any("se esperan 2" in p for p in script.problemas_de_la_home("libracargo", sin_pie))


def test_el_script_escribe_y_el_check_pasa(tmp_path, monkeypatch):
    script = _script()
    for dir_repo in script.REPO_DIR_BY_SITE.values():
        (tmp_path / dir_repo / "public").mkdir(parents=True)
    # Sin homes: el script las pide y --check falla...
    monkeypatch.setattr("sys.argv", ["generate_favicon.py", "--proyectos-dir", str(tmp_path)])
    assert script.main() == 0
    assert (tmp_path / "ventalibra_web" / "public" / "img" / "favicon.svg").read_text(encoding="utf-8") == favicon_svg(
        "ventalibra"
    )
    monkeypatch.setattr("sys.argv", ["generate_favicon.py", "--check", "--proyectos-dir", str(tmp_path)])
    assert script.main() == 1  # ...los favicons ya estan, pero faltan las homes

    # ...y con las homes alineadas pasa.
    for site, dir_repo in script.REPO_DIR_BY_SITE.items():
        marca = marca_icono_html(site)
        (tmp_path / dir_repo / "public" / "index.html").write_text(
            f'{script.LINK_FAVICON}<div class="logo-icon">{marca}</div><div class="logo-icon">{marca}</div>',
            encoding="utf-8",
        )
    assert script.main() == 0
