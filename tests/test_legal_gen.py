"""La página pública de Términos: que exista en los ocho, que sea verificable
y que no quede detrás del login.

Lo que fijan estos tests, en orden de lo que se rompe sin que se note:

1. 🔴 **Que la página sea accesible sin registro previo.** Es la cláusula 30.4.
   Si cayera bajo `/docs/`, el `auth_request` de nginx la gatearía y el contrato
   quedaría publicado sólo para quien ya es cliente — que es exactamente al revés
   de lo que tiene que pasar. Se verifica contra el `default.conf.template` real,
   no contra la intención.
2. 🔴 **Que el hash anunciado sea el del Markdown publicado al lado.** Ese par
   es lo único que hace verificable la cláusula 30.3 desde afuera: si el `.md`
   que se publica no es byte por byte el que se hashea, la página anuncia una
   huella que no se puede reproducir y nadie se entera hasta que alguien la
   compara.
3. Que el texto publicado sea el mismo que la instancia exige aceptar — o sea,
   que salga de `libraauth` y no de una copia.
4. Que las tablas del contrato lleven la clase que el CSS del kit ya define.
"""
import hashlib
import re
from pathlib import Path

import pytest

from libra_web_kit.docs_sidebars import SIDEBARS
from libra_web_kit.legal_gen import (
    RUTA_HTML, RUTA_MARKDOWN, markdown_publicado, render, render_all, sitios,
)
from libraauth.terminos import VERSION_VIGENTE, hash_vigente, texto_vigente

RAIZ = Path(__file__).resolve().parents[1]


def test_rinde_los_ocho_sitios():
    paginas = render_all()
    assert len(paginas) == 8
    assert set(paginas) == set(SIDEBARS)


@pytest.mark.parametrize("site", sorted(SIDEBARS))
def test_cada_pagina_lleva_el_branding_de_su_sitio(site):
    html = render(site)
    assert SIDEBARS[site]["brand"] in html
    assert SIDEBARS[site]["footer_html"] in html


# ── 1. Pública, no gateada ───────────────────────────────────────────────────

def test_la_ruta_no_cae_bajo_docs():
    assert RUTA_HTML.startswith("legal/")
    assert RUTA_MARKDOWN.startswith("legal/")
    assert "/docs/" not in RUTA_HTML


def test_nginx_no_pide_auth_para_legal():
    """Control sobre el archivo real: el `auth_request` cuelga de `location
    /docs/`, así que `/legal/` tiene que caer en el `location /` público.

    Sin este test, mover el bloque de nginx dejaría el contrato detrás del login
    sin que ninguna otra cosa fallara.
    """
    conf = (RAIZ / "nginx" / "default.conf.template").read_text(encoding="utf-8")
    bloques = re.findall(r"location\s+([^\s{]+)\s*\{([^}]*)\}", conf, re.S)
    con_auth = [ruta for ruta, cuerpo in bloques if "auth_request" in cuerpo]
    assert con_auth == ["/docs/"], (
        f"El auth_request dejó de estar sólo en /docs/: {con_auth}. "
        "La página de Términos tiene que seguir siendo pública (cláusula 30.4)."
    )


# ── 2. El hash es verificable desde afuera ───────────────────────────────────

def test_el_markdown_publicado_es_exactamente_el_que_se_hashea():
    publicado = markdown_publicado()
    assert publicado == texto_vigente()
    assert hashlib.sha256(publicado.encode("utf-8")).hexdigest() == hash_vigente()


def test_la_pagina_anuncia_el_hash_del_texto_publicado():
    html = render("contalibra")
    assert hash_vigente() in html
    assert "/" + RUTA_MARKDOWN in html
    assert f"Versión {VERSION_VIGENTE}" in html


def test_el_markdown_publicado_no_tiene_crlf():
    """Un CRLF en el archivo servido cambia su `sha256sum` y deja la huella
    anunciada sin forma de reproducirse."""
    assert "\r" not in markdown_publicado()


# ── 3. El texto sale del motor, no de una copia ──────────────────────────────

@pytest.mark.parametrize("frase", [
    "se actualiza cada seis (6) meses",
    "Los Datos del Cliente son de su exclusiva propiedad",
    "El Software es de propiedad exclusiva del Prestador",
])
def test_el_html_publica_las_clausulas_del_contrato(frase):
    html = render("medlibra")
    # El renderizador de Markdown puede partir la frase con etiquetas de negrita;
    # se compara sobre el texto sin marcado.
    plano = re.sub(r"<[^>]+>", "", html)
    assert frase in plano


# ── 4. Presentación ──────────────────────────────────────────────────────────

def test_las_tablas_llevan_la_clase_del_kit():
    html = render("libraclub")
    assert "<table>" not in html
    assert html.count('<table class="docs-table">') == 2  # severidades + Anexo II


def test_las_paginas_de_docs_linkean_a_los_terminos():
    """La página publicada tiene que ser alcanzable. Sin este link sólo llega
    quien ya tiene la URL."""
    from libra_web_kit.docs_gen import render as render_docs
    from libra_web_kit.docs_gen import list_pages

    html = render_docs("contalibra", list_pages("contalibra")[0])
    assert 'href="/legal/terminos"' in html
