"""La marca dibujada de cada producto, tal como la entrega libra-ui (ADR-034).

Las ocho marcas son archivos SVG que el kit **copia, no dibuja**
(`scripts/sincronizar_marcas.py`, origen en `libra_web_kit/marcas/ORIGEN.txt`):

- `marcas/<p>.svg`: la marca completa -- el cuadrado redondeado del color del producto
  y el dibujo encima, lienzo de 120. Es la del navbar y del pie (`/img/marca.svg`).
- `marcas/<p>-favicon.svg`: una sola pieza del ícono, engrosada, para 16-32 px
  (`/img/favicon.svg`).

Este módulo sólo las lee, como **bytes**: se escriben en las landings sin pasar por un
`str`, para que lo publicado sea idéntico al archivo de libra-ui y `--check` pueda
comparar byte a byte. Reemplaza al dibujo en Python de ADR-008 (`favicon_gen` e
`iconos_bootstrap`, retirados; ver ADR-009).

Sólo SVG, sin PNG: ver el motivo en ADR-008 (rasterizar exigiría Pillow o cairosvg).
"""
from importlib import resources

from libra_web_kit.identidad import IDENTIDAD

_MARCAS_DIR = resources.files("libra_web_kit").joinpath("marcas")

#: Dónde se publica cada archivo dentro de `public/` de una landing, y el `href` con
#: que lo enlaza el HTML.
RUTA_MARCA = "img/marca.svg"
RUTA_FAVICON = "img/favicon.svg"

#: Los complementos de la suite: tienen marca dibujada en libra-ui pero no son un sitio
#: de `IDENTIDAD` (libra-ui ADR-078). LibraEdge se muestra en la sección `#libraedge` de
#: cada landing, con su propio archivo.
COMPLEMENTOS = ("libraedge",)
RUTA_LIBRAEDGE = "img/libraedge.svg"


def _leer(nombre: str, sitio: str) -> bytes:
    if sitio not in IDENTIDAD:
        raise KeyError(f"sitio desconocido: {sitio!r} (conocidos: {sorted(IDENTIDAD)})")
    return _MARCAS_DIR.joinpath(nombre).read_bytes()


def svg_marca(sitio: str) -> bytes:
    """La marca completa de un sitio (clave de `identidad.IDENTIDAD`)."""
    return _leer(f"{sitio}.svg", sitio)


def svg_favicon(sitio: str) -> bytes:
    """El favicon (variante reducida) de un sitio."""
    return _leer(f"{sitio}-favicon.svg", sitio)


def svg_libraedge() -> bytes:
    """La marca completa de LibraEdge, el complemento de la suite (libra-ui ADR-078)."""
    return _MARCAS_DIR.joinpath("libraedge.svg").read_bytes()


def render_all() -> dict[str, tuple[bytes, bytes]]:
    """{sitio: (marca, favicon)} para los ocho sitios."""
    return {sitio: (svg_marca(sitio), svg_favicon(sitio)) for sitio in IDENTIDAD}
