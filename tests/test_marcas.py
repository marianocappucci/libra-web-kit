"""La marca dibujada de libra-ui (ADR-034) que el kit copia y publica en las landings.

El kit no dibuja nada: `libra_web_kit/marcas/*.svg` son copias byte a byte de libra-ui y
estos tests verifican que estén las 16, que cada una sea un SVG del color de su producto
(`IDENTIDAD`, la tabla que guarda `test_identidad.py`) y que los templates, el script que
las publica y el que las sincroniza hagan lo que dicen.
"""
import importlib.util
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from libra_web_kit.docs_gen import list_pages, render as render_doc
from libra_web_kit.docs_sidebars import SIDEBARS
from libra_web_kit.identidad import IDENTIDAD
from libra_web_kit.legal_gen import render as render_legal
from libra_web_kit.marcas_gen import RUTA_FAVICON, RUTA_MARCA, render_all, svg_favicon, svg_marca

RAIZ = Path(__file__).resolve().parents[1]
MARCAS = RAIZ / "libra_web_kit" / "marcas"
SVG_NS = "{http://www.w3.org/2000/svg}"
LA_IMG = '<img src="/img/marca.svg" alt="" class="logo-icon" width="32" height="32">'


def _script(nombre: str):
    spec = importlib.util.spec_from_file_location(nombre, RAIZ / "scripts" / f"{nombre}.py")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


# ── los 16 archivos ──────────────────────────────────────────────────────────


def test_estan_los_16_svg_y_no_sobra_ninguno():
    esperados = {f"{s}{v}.svg" for s in IDENTIDAD for v in ("", "-favicon")}
    assert len(esperados) == 16
    assert {p.name for p in MARCAS.glob("*.svg")} == esperados
    assert (MARCAS / "ORIGEN.txt").is_file()


@pytest.mark.parametrize("variante", ["", "-favicon"])
@pytest.mark.parametrize("site", sorted(IDENTIDAD))
def test_cada_svg_empieza_con_svg_y_lleva_el_color_de_la_identidad(site, variante):
    contenido = (MARCAS / f"{site}{variante}.svg").read_bytes().decode("utf-8")
    assert contenido.startswith("<svg"), f"{site}{variante}.svg no empieza con <svg"
    assert IDENTIDAD[site].color in contenido.lower(), f"{site}{variante}.svg no lleva {IDENTIDAD[site].color}"
    raiz = ET.fromstring(contenido)
    assert raiz.tag == f"{SVG_NS}svg"
    assert raiz.get("viewBox") == "0 0 120 120"
    # El primer elemento dibujado es el cuadrado redondeado del color de marca.
    cuadrado = raiz.find(f"{SVG_NS}rect")
    assert cuadrado.get("fill") == IDENTIDAD[site].color
    assert cuadrado.get("rx")


def test_las_16_son_distintas_entre_si():
    assert len({p.read_bytes() for p in MARCAS.glob("*.svg")}) == 16


def test_marcas_gen_sirve_los_bytes_del_archivo():
    for site, (marca, favicon) in render_all().items():
        assert marca == (MARCAS / f"{site}.svg").read_bytes() == svg_marca(site)
        assert favicon == (MARCAS / f"{site}-favicon.svg").read_bytes() == svg_favicon(site)
        assert isinstance(marca, bytes) and marca != favicon


def test_sitio_desconocido():
    with pytest.raises(KeyError):
        svg_marca("no-existe")
    with pytest.raises(KeyError):
        svg_favicon("no-existe")


def test_el_origen_dice_de_que_version_de_libra_ui_salen():
    sincronizar = _script("sincronizar_marcas")
    origen = (MARCAS / "ORIGEN.txt").read_text(encoding="utf-8")
    assert f"libra-ui {sincronizar.TAG_POR_DEFECTO} (" in origen
    assert "scripts/sincronizar_marcas.py" in origen


# ── lo que genera el kit: docs, legales, pie de Restolibra ───────────────────


@pytest.mark.parametrize("site", sorted(SIDEBARS))
def test_las_paginas_de_docs_llevan_la_marca_y_el_favicon(site):
    html = render_doc(site, list_pages(site)[0])
    assert LA_IMG in html
    assert 'rel="icon" type="image/svg+xml" href="/img/favicon.svg"' in html
    assert '<div class="logo-icon"' not in html


@pytest.mark.parametrize("site", sorted(SIDEBARS))
def test_la_pagina_legal_lleva_la_marca_y_el_favicon(site):
    html = render_legal(site)
    assert LA_IMG in html
    assert 'rel="icon" type="image/svg+xml" href="/img/favicon.svg"' in html
    assert '<div class="logo-icon"' not in html


def test_el_pie_de_restolibra_lleva_la_marca_de_28():
    footer = SIDEBARS["restolibra"]["footer_html"]
    assert '<img src="/img/marca.svg" alt="" class="logo-icon" width="28" height="28">' in footer
    assert "@@" not in footer and "<i class=\"bi bi-cup-hot\"" not in footer


@pytest.mark.parametrize("site", sorted(SIDEBARS))
def test_ningun_footer_queda_con_cuadrado_de_fondo(site):
    footer = SIDEBARS[site]["footer_html"]
    assert "@@" not in footer
    assert not re.search(r'<div[^>]*class="logo-icon', footer)


# ── scripts/generate_favicon.py ──────────────────────────────────────────────

HOME_OK = (
    '<link rel="icon" type="image/svg+xml" href="/img/favicon.svg">\n'
    '<img src="/img/marca.svg" alt="" class="logo-icon" width="32" height="32">\n'
    '<img src="/img/marca.svg" alt="" class="logo-icon" width="28" height="28">\n'
)


def test_home_alineada_no_da_problemas():
    assert _script("generate_favicon").problemas_de_la_home(HOME_OK) == []


def test_home_con_cuadrado_viejo_sin_favicon_o_sin_pie_da_problemas():
    problemas = _script("generate_favicon").problemas_de_la_home
    viejo = HOME_OK.replace(
        '<img src="/img/marca.svg" alt="" class="logo-icon" width="28" height="28">',
        '<div class="logo-icon"><i class="bi bi-truck"></i></div>',
    )
    assert any("se esperan 2" in p for p in problemas(viejo))
    assert any("marca anterior" in p for p in problemas(viejo))
    assert any("favicon" in p for p in problemas(HOME_OK.replace('<link rel="icon" type="image/svg+xml" href="/img/favicon.svg">', "")))
    assert any("width y height" in p for p in problemas(HOME_OK.replace(' width="28" height="28"', "")))


def test_el_script_copia_byte_a_byte_y_el_check_lo_detecta(tmp_path, monkeypatch):
    script = _script("generate_favicon")
    for dir_repo in script.REPO_DIR_BY_SITE.values():
        (tmp_path / dir_repo / "public").mkdir(parents=True)
    monkeypatch.setattr("sys.argv", ["generate_favicon.py", "--proyectos-dir", str(tmp_path)])
    assert script.main() == 0
    for site, (marca, favicon) in render_all().items():
        img = tmp_path / script.REPO_DIR_BY_SITE[site] / "public" / "img"
        assert (img / "marca.svg").read_bytes() == marca == (MARCAS / f"{site}.svg").read_bytes()
        assert (img / "favicon.svg").read_bytes() == favicon == (MARCAS / f"{site}-favicon.svg").read_bytes()

    # Los SVG ya estan, pero faltan las homes: --check falla...
    monkeypatch.setattr("sys.argv", ["generate_favicon.py", "--check", "--proyectos-dir", str(tmp_path)])
    assert script.main() == 1
    # ...con las homes alineadas pasa...
    for dir_repo in script.REPO_DIR_BY_SITE.values():
        (tmp_path / dir_repo / "public" / "index.html").write_text(HOME_OK, encoding="utf-8")
    assert script.main() == 0
    # ...y un solo byte distinto en una marca publicada lo rompe.
    marca_publicada = tmp_path / script.REPO_DIR_BY_SITE["medlibra"] / "public" / "img" / "marca.svg"
    marca_publicada.write_bytes(marca_publicada.read_bytes() + b"\n")
    assert script.main() == 1


# ── scripts/sincronizar_marcas.py ────────────────────────────────────────────


def _libra_ui_falso(tmp_path: Path) -> Path:
    """Un repo git con `marcas/` etiquetado v9.9.9, con un contenido que no es el del kit."""
    repo = tmp_path / "libra-ui"
    (repo / "marcas").mkdir(parents=True)
    sincronizar = _script("sincronizar_marcas")
    for n in sincronizar.nombres_de_archivo():
        (repo / "marcas" / n).write_bytes(f'<svg id="{n}">\r\n'.encode())  # \r\n: se copia sin normalizar
    git = ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false"]
    subprocess.run(["git", "-C", str(repo), "init", "-q"], check=True)
    subprocess.run([*git, "add", "."], check=True)
    subprocess.run([*git, "commit", "-q", "-m", "marcas"], check=True)
    subprocess.run([*git, "tag", "v9.9.9"], check=True)
    return repo


def test_sincronizar_desde_un_tag_copia_los_16_byte_a_byte_y_deja_el_origen(tmp_path, monkeypatch):
    script = _script("sincronizar_marcas")
    repo = _libra_ui_falso(tmp_path)
    destino = tmp_path / "marcas-kit"
    argv = ["sincronizar_marcas.py", "--libra-ui", str(repo), "--tag", "v9.9.9", "--destino", str(destino)]
    monkeypatch.setattr("sys.argv", argv)
    assert script.main() == 0
    for n in script.nombres_de_archivo():
        assert (destino / n).read_bytes() == (repo / "marcas" / n).read_bytes()
    origen = (destino / "ORIGEN.txt").read_text(encoding="utf-8")
    assert "libra-ui v9.9.9 (" in origen and "--tag v9.9.9" in origen

    monkeypatch.setattr("sys.argv", [*argv, "--check"])
    assert script.main() == 0
    (destino / "ventalibra.svg").write_bytes(b"<svg/>")
    assert script.main() == 1


def test_sincronizar_con_un_tag_que_no_existe_falla_sin_escribir(tmp_path, monkeypatch):
    script = _script("sincronizar_marcas")
    repo = _libra_ui_falso(tmp_path)
    destino = tmp_path / "marcas-kit"
    monkeypatch.setattr(
        "sys.argv",
        ["sincronizar_marcas.py", "--libra-ui", str(repo), "--tag", "v0.0.0", "--destino", str(destino)],
    )
    assert script.main() == 2
    assert not destino.exists()


def test_sincronizar_desde_un_directorio(tmp_path, monkeypatch):
    script = _script("sincronizar_marcas")
    repo = _libra_ui_falso(tmp_path)
    destino = tmp_path / "marcas-kit"
    monkeypatch.setattr(
        "sys.argv",
        ["sincronizar_marcas.py", "--desde-dir", str(repo / "marcas"), "--destino", str(destino)],
    )
    assert script.main() == 0
    assert (destino / "libraclub-favicon.svg").read_bytes() == (repo / "marcas" / "libraclub-favicon.svg").read_bytes()
    assert "sin versión" in (destino / "ORIGEN.txt").read_text(encoding="utf-8")


def test_el_kit_esta_sincronizado_con_el_tag_que_declara():
    """Con un checkout de libra-ui a mano, lo que hay en `marcas/` es lo del tag declarado.
    Sin checkout (CI) no hay con qué comparar y se saltea."""
    script = _script("sincronizar_marcas")
    if not (script.LIBRA_UI_POR_DEFECTO / ".git").exists():
        pytest.skip("no hay un checkout de libra-ui al lado del kit")
    try:
        marcas, _ = script.leer_de_tag(script.LIBRA_UI_POR_DEFECTO, script.TAG_POR_DEFECTO)
    except subprocess.CalledProcessError:
        pytest.skip(f"el checkout de libra-ui no tiene el tag {script.TAG_POR_DEFECTO}")
    for n, contenido in marcas.items():
        assert (MARCAS / n).read_bytes() == contenido, n
