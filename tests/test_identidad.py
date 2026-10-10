"""Guardianes de la identidad de producto (color + icono).

La fuente es la tabla «La identidad de cada producto» de
`wiki/analyses/identidad-de-producto-diseno.md`, en el repo del wiki. Este archivo la
**hardcodea a proposito**: no se importa de `identidad.py` ni se lee del documento,
porque un test que lee de lo que testea nunca falla. Si alguien cambia un color o un
icono en `identidad.py` sin tocar el documento (o al reves), este test se pone rojo
y obliga a cambiar los dos -- y `libra-ui/src/identidad.ts`, que tiene su propio test
contra la misma tabla.
"""
import re

import pytest

from libra_web_kit.docs_sidebars import SIDEBARS
from libra_web_kit.identidad import IDENTIDAD
from libra_web_kit.site_css_tokens import SITES

# (clave, nombre, rubro, color, oscuro, claro, sobre oscuro, icono bootstrap)
TABLA_DEL_DOCUMENTO = [
    ("contalibra", "ContaLibra", "Comercios y PyMEs", "#2563eb", "#1d4ed8", "#eff6ff", "#60a5fa", "bi-receipt-cutoff"),
    ("restolibra", "RestoLibra", "Restaurantes, bares y delivery", "#ea580c", "#c2410c", "#fff7ed", "#fb923c", "bi-cup-hot"),
    ("gestiolibra", "GestioLibra", "Negocios de servicios", "#7c3aed", "#6d28d9", "#f5f3ff", "#a78bfa", "bi-calendar-check"),
    ("medlibra", "MedLibra", "Consultorios y centros médicos", "#0d9488", "#0f766e", "#f0fdfa", "#2dd4bf", "bi-heart-pulse"),
    ("ventalibra", "VentaLibra", "Punto de venta para retail", "#d97706", "#b45309", "#fffbeb", "#fbbf24", "bi-upc-scan"),
    ("libradesk", "LibraDesk", "Empresas de IT", "#4f46e5", "#4338ca", "#eef2ff", "#818cf8", "bi-headset"),
    ("libracargo", "LibraCargo", "Agencias de cargas", "#012c83", "#001d5c", "#eef3fc", "#7aa2f7", "bi-truck"),
    ("libraclub", "LibraClub", "Complejos deportivos", "#017b4b", "#015c38", "#ecfdf5", "#34d399", "bi-trophy"),
]


def test_la_tabla_cubre_los_ocho_productos():
    assert sorted(IDENTIDAD) == sorted(fila[0] for fila in TABLA_DEL_DOCUMENTO)
    assert len(TABLA_DEL_DOCUMENTO) == 8


@pytest.mark.parametrize("fila", TABLA_DEL_DOCUMENTO, ids=lambda f: f[0])
def test_identidad_coincide_con_la_tabla_del_documento(fila):
    clave, nombre, rubro, color, oscuro, claro, sobre_oscuro, icono = fila
    ident = IDENTIDAD[clave]
    assert (ident.nombre, ident.rubro) == (nombre, rubro)
    assert (ident.color, ident.color_oscuro, ident.color_claro, ident.color_sobre_oscuro) == (
        color, oscuro, claro, sobre_oscuro,
    )
    assert ident.icono_bootstrap == icono


def _token(site: str, nombre: str) -> str:
    return re.search(rf"--{nombre}:\s*(#[0-9a-fA-F]{{6}})", SITES[site]["tokens"]).group(1).lower()


@pytest.mark.parametrize("site", sorted(IDENTIDAD))
def test_el_brand_de_site_css_tokens_es_el_color_de_la_identidad(site):
    """El documento dice «los colores de SITES no cambian, porque ya son estos»: este es
    el test que lo sostiene. El `--brand` es lo que pinta el cuadrado de la marca."""
    assert _token(site, "brand") == IDENTIDAD[site].color


@pytest.mark.parametrize("site", sorted(IDENTIDAD))
def test_brand_dark_y_brand_light_son_el_oscuro_y_el_claro(site):
    assert _token(site, "brand-dark") == IDENTIDAD[site].color_oscuro
    assert _token(site, "brand-light") == IDENTIDAD[site].color_claro


def test_identidad_y_sites_tienen_las_mismas_claves():
    assert set(IDENTIDAD) == set(SITES) == set(SIDEBARS)


def test_los_ocho_iconos_son_distintos():
    assert len({i.icono_bootstrap for i in IDENTIDAD.values()}) == 8, "dos productos no pueden compartir icono"


def test_un_icono_con_prefijo_bi_y_sin_espacios():
    for sitio, ident in IDENTIDAD.items():
        assert re.fullmatch(r"bi-[a-z0-9-]+", ident.icono_bootstrap), sitio


def test_los_colores_son_hex_de_seis_digitos_en_minuscula():
    for sitio, ident in IDENTIDAD.items():
        for campo in ("color", "color_oscuro", "color_claro", "color_sobre_oscuro"):
            assert re.fullmatch(r"#[0-9a-f]{6}", getattr(ident, campo)), (sitio, campo)


def test_ningun_pie_de_docs_dice_ecosistema_compulibra():
    """Los sitios son parte de LibraSuite: el pie viejo de RestoLibra decía «ecosistema Compulibra»."""
    for sitio, sidebar in SIDEBARS.items():
        pie = sidebar.get("footer_html", "").lower()
        assert "ecosistema" not in pie and "compulibra" not in pie and "neuroflow" not in pie, sitio
        if "parte de" in pie:
            assert 'href="https://librasuite.com.ar"' in pie, sitio
