"""Generador de la pagina publica de Terminos y Condiciones de los ocho sitios.

**El texto no vive aca.** Vive en `libraauth.terminos`, que es el mismo modulo
del que las ocho instancias sacan el hash que guardan como prueba de la
aceptacion (clausula 30.3 del contrato). Esa es toda la razon por la que este
generador importa un motor de backend: si el texto se copiara aca, la web y el
sistema podrian publicar y exigir contratos distintos, y el unico sintoma serian
dos cadenas de 64 caracteres que no coinciden el dia que alguien las compare.

**Y por eso la pagina publica el hash.** Cualquiera puede bajar el `.md` que se
escribe al lado y correrle `sha256sum`: si da lo mismo que dice la pagina, el
texto publicado es byte por byte el que la instancia exigio aceptar.

**Va fuera de `/docs/`, a proposito.** Las paginas de `/docs/` estan detras del
`auth_request` de nginx; la clausula 30.4 exige que el contrato sea accesible
**sin registro previo**. Por eso se escribe en `public/legal/`, que cae en el
`location /` publico del `nginx/default.conf.template`.

Depende de `libraauth` y de `markdown`, que estan en el extra `dev`: los
contenedores de las landings sirven HTML ya generado y no necesitan ninguno de
los dos.
"""
from importlib import resources

from jinja2 import Environment, FileSystemLoader, select_autoescape

from libra_web_kit.docs_sidebars import SIDEBARS

try:
    import markdown as _markdown
    from libraauth.terminos import (
        VERSION_VIGENTE, VIGENTE_DESDE, hash_vigente, texto_vigente,
    )
except ModuleNotFoundError as exc:  # pragma: no cover - camino de instalacion
    raise ModuleNotFoundError(
        f"{exc.name} no esta instalado. La generacion de la pagina de Terminos "
        "necesita el extra dev del kit: pip install -e '.[dev]'"
    ) from exc

_TEMPLATES_DIR = resources.files("libra_web_kit").joinpath("templates")

_env = Environment(
    loader=FileSystemLoader(str(_TEMPLATES_DIR)),
    autoescape=select_autoescape(enabled_extensions=()),
    trim_blocks=True,
    lstrip_blocks=True,
)

#: Ruta publica de la pagina. `try_files $uri $uri.html` de nginx hace que el
#: archivo `legal/terminos.html` se sirva tambien como `/legal/terminos`.
RUTA_HTML = "legal/terminos.html"

#: El Markdown crudo, al lado del HTML, para que el hash sea verificable desde
#: afuera. El nombre lleva la version para que las anteriores puedan quedar
#: publicadas sin pisarse (clausula 30.4).
RUTA_MARKDOWN = f"legal/terminos-v{VERSION_VIGENTE}.md"


def sitios() -> list[str]:
    return sorted(SIDEBARS)


def _a_html(texto_md: str) -> str:
    """Markdown -> HTML, con las tablas tomando la clase que el CSS del kit ya
    define.

    `markdown` emite `<table>` pelado y todo el estilo de tablas de
    `style.css.template` cuelga de `.docs-table`. Sin este reemplazo las dos
    tablas del contrato —la de severidades de soporte y la del Anexo II— salen
    sin bordes ni encabezado, que es justo donde se nota.
    """
    html = _markdown.markdown(texto_md, extensions=["tables", "sane_lists"])
    return html.replace("<table>", '<table class="docs-table">')


def render(site: str) -> str:
    """La pagina completa de Terminos para un sitio (HTML final)."""
    if site not in SIDEBARS:
        raise KeyError(f"sitio desconocido: {site!r} (conocidos: {sorted(SIDEBARS)})")

    cfg = SIDEBARS[site]
    plantilla = _env.get_template("legal_page.html.jinja2")
    return plantilla.render(
        brand=cfg["brand"],
        letter=cfg["letter"],
        footer_html=cfg["footer_html"],
        version=VERSION_VIGENTE,
        vigente_desde=VIGENTE_DESDE,
        hash_texto=hash_vigente(),
        archivo_markdown="/" + RUTA_MARKDOWN,
        contenido_html=_a_html(texto_vigente()),
    )


def markdown_publicado() -> str:
    """El mismo texto que se hashea, tal cual, para escribirlo al lado del HTML."""
    return texto_vigente()


def render_all() -> dict[str, str]:
    """{sitio: html} para los ocho sitios."""
    return {site: render(site) for site in sitios()}
