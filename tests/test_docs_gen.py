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


def test_total_page_count_is_82():
    total = sum(len(pages) for pages in PAGES.values())
    assert total == 82


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
