"""Tests para libra_web_kit.docs_gen -- extraido 2026-07-27 de las 82
paginas HTML reales de /docs/ (19 Contalibra, 23 Restolibra, 12
Gestiolibra, 16 MedLibra, 12 VentaLibra). Ver
wiki/analyses/auditoria-duplicacion-familia-libra.md.

No se compara byte a byte (a diferencia de css_gen): el HTML original
tenia formato inconsistente entre paginas (indentacion, espacios en
blanco) por ser copy-paste a mano, asi que normalizar el formato es
parte del objetivo, no una regresion. Se compara en cambio el TEXTO
VISIBLE y el estado de los links (incluido cual queda "active") -- eso
es lo que le importa a un usuario navegando la pagina."""
from bs4 import BeautifulSoup

from libra_web_kit.docs_gen import list_pages, render, render_all
from libra_web_kit.docs_pages import PAGES
from libra_web_kit.docs_sidebars import SIDEBARS


def _visible(html: str):
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text(separator="|", strip=True)
    links = {(a.get("href"), "active" in (a.get("class") or [])) for a in soup.find_all("a")}
    return text, links


def test_render_all_covers_every_site_and_page():
    rendered = render_all()
    assert set(rendered) == set(PAGES)
    for site in PAGES:
        assert set(rendered[site]) == set(PAGES[site])


def test_toda_pagina_registrada_tiene_su_contenido():
    """🔴 Agregar una página toca TRES lugares: el fragmento en
    `docs_content/`, la entrada en `PAGES` y el link en `SIDEBARS`. Olvidarse
    de uno no siempre se ve.

    Este test cubre el olvido más caro: una página registrada sin contenido.

    Reemplaza a `test_total_page_count_is_82`, que sólo aseveraba el número.
    Un conteo fijo no distingue "faltó el fragmento" de "hay una página de
    más", y encima hay que actualizarlo cada vez que se agrega una — con lo
    cual el reflejo es cambiar el número, no mirar qué pasó.
    """
    from libra_web_kit.docs_gen import _CONTENT_DIR

    faltan = [
        f"{site}/{fname}"
        for site, pages in PAGES.items()
        for fname in pages
        if not (_CONTENT_DIR / site / fname).is_file()
    ]
    assert not faltan, f"registradas en PAGES sin fragmento en docs_content: {faltan}"


def test_todo_contenido_esta_registrado():
    """La contracara: un fragmento que nadie renderiza es trabajo escrito que
    no llega a ninguna landing, y no hay forma de notarlo mirando el sitio."""
    from libra_web_kit.docs_gen import _CONTENT_DIR

    huerfanos = [
        f"{site}/{p.name}"
        for site in PAGES
        for p in sorted((_CONTENT_DIR / site).iterdir())
        if p.suffix == ".html" and p.name not in PAGES[site]
    ]
    assert not huerfanos, f"en docs_content pero sin entrada en PAGES: {huerfanos}"


def test_todo_link_del_sidebar_apunta_a_una_pagina_que_existe():
    """Un link del sidebar a una página no registrada es un 404 en la
    navegación de la documentación — visible para el cliente, y sólo se
    encuentra haciendo clic."""
    rotos = []
    for site, cfg in SIDEBARS.items():
        for item in cfg["sidebar"]:
            if item["type"] != "link":
                continue
            href = item["href"]
            fname = "index.html" if href == "/docs/" else href.removeprefix("/docs/")
            if fname not in PAGES[site]:
                rotos.append(f"{site}: {href}")
    assert not rotos, f"links del sidebar sin página: {rotos}"


def test_todo_link_interno_del_contenido_resuelve():
    """Los links dentro del texto —el pie «← anterior / siguiente →» y las
    referencias cruzadas— se escriben **a mano** en cada fragmento, así que un
    typo pasa el generador sin ruido y termina siendo un 404 que ve el cliente.

    El sidebar lo genera el kit y ya está cubierto; esto cubre lo escrito a
    mano, que es donde se equivoca una persona.
    """
    import re

    from libra_web_kit.docs_gen import _CONTENT_DIR

    rotos = []
    for site, pages in PAGES.items():
        for fname in pages:
            html = (_CONTENT_DIR / site / fname).read_text(encoding="utf-8")
            for href in re.findall(r'href="(/docs/[^"#]*)', html):
                destino = "index.html" if href in ("/docs/", "/docs") else href.removeprefix("/docs/")
                if destino and destino not in pages:
                    rotos.append(f"{site}/{fname} → {href}")
    assert not rotos, f"links internos que no resuelven: {rotos}"


def test_toda_pagina_es_alcanzable_desde_el_sidebar():
    """Y al revés: una página registrada a la que ningún link lleva existe pero
    nadie la encuentra. Es lo que pasa si se agrega a `PAGES` y se olvida
    `SIDEBARS`."""
    inalcanzables = []
    for site, pages in PAGES.items():
        hrefs = {
            "index.html" if i["href"] == "/docs/" else i["href"].removeprefix("/docs/")
            for i in SIDEBARS[site]["sidebar"] if i["type"] == "link"
        }
        inalcanzables += [f"{site}/{f}" for f in pages if f not in hrefs]
    assert not inalcanzables, f"sin link en el sidebar: {inalcanzables}"


def test_render_unknown_site_raises():
    import pytest
    with pytest.raises(KeyError):
        render("no-existe", "index.html")


def test_render_unknown_page_raises():
    import pytest
    with pytest.raises(KeyError):
        render("contalibra", "no-existe.html")


def test_every_page_renders_valid_html_with_expected_shell():
    for site in PAGES:
        for fname in list_pages(site):
            html = render(site, fname)
            soup = BeautifulSoup(html, "lxml")
            assert soup.find("nav", class_="navbar") is not None
            assert soup.find("nav", class_="docs-sidebar") is not None
            assert soup.find("main", class_="docs-content") is not None
            assert soup.find("footer") is not None
            assert soup.title is not None and soup.title.string


def test_active_sidebar_link_matches_current_page():
    """El link del sidebar que corresponde a la pagina actual tiene que
    quedar marcado como activo -- ninguna pagina deberia navegar "a
    ciegas" sin indicar donde esta parada."""
    for site in PAGES:
        for fname in list_pages(site):
            meta = PAGES[site][fname]
            if meta["active_href"] is None:
                continue  # alguna pagina legacy sin active en el original; no se inventa uno
            html = render(site, fname)
            soup = BeautifulSoup(html, "lxml")
            sidebar = soup.find("nav", class_="docs-sidebar")
            active_links = [a for a in sidebar.find_all("a") if "active" in (a.get("class") or [])]
            assert len(active_links) == 1, f"{site}/{fname}: {len(active_links)} links activos, esperaba 1"
            assert active_links[0]["href"] == meta["active_href"]


def test_sidebar_has_same_links_on_every_page_of_a_site():
    for site in PAGES:
        hrefs_by_page = set()
        for fname in list_pages(site):
            html = render(site, fname)
            soup = BeautifulSoup(html, "lxml")
            sidebar = soup.find("nav", class_="docs-sidebar")
            hrefs = tuple(sorted(a["href"] for a in sidebar.find_all("a")))
            hrefs_by_page.add(hrefs)
        assert len(hrefs_by_page) == 1, f"{site}: el sidebar deberia ser igual (salvo activo) en todas sus paginas"


def test_visible_content_matches_extracted_metadata_smoke():
    """Chequeo liviano: el <h1> del contenido no queda vacio y el titulo
    de la pagina aparece en el <title>."""
    for site in PAGES:
        for fname in list_pages(site):
            html = render(site, fname)
            soup = BeautifulSoup(html, "lxml")
            main = soup.find("main", class_="docs-content")
            assert main.get_text(strip=True), f"{site}/{fname}: contenido vacio"
            assert soup.title.string == PAGES[site][fname]["title"]


def test_footer_is_the_one_configured_for_the_site():
    for site in PAGES:
        expected_footer = BeautifulSoup(SIDEBARS[site]["footer_html"], "lxml").get_text(strip=True)
        html = render(site, list_pages(site)[0])
        soup = BeautifulSoup(html, "lxml")
        rendered_footer = soup.find("footer").get_text(strip=True)
        assert rendered_footer == expected_footer
