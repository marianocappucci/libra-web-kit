"""Generador del favicon de cada producto: el ícono plano.

Un cuadrado redondeado del color del producto con el ícono de Bootstrap Icons en
blanco al centro (`wiki/analyses/identidad-de-producto-diseno.md`, «La marca es
siempre el ícono blanco sobre un cuadrado redondeado del color»).

**Sólo SVG, a propósito.** Un PNG (el `favicon-32.png`, el `apple-touch-icon`) exige
rasterizar el trazo, y el kit no tiene con qué: ni Pillow ni cairosvg están entre sus
dependencias, y agregarlas para sacar tres archivos arrastraría un binario nativo a
un paquete que las landings instalan sólo por `docs_auth`. El SVG lo toman Chrome,
Edge, Firefox y Safari de escritorio; lo que queda afuera es el ícono de «agregar a
inicio» de iOS. Si hace falta, se genera una vez con cualquier rasterizador a partir
de `favicon_svg()` y se versiona el PNG en la landing.

`favicon_svg()` es una función pura y su salida es determinista, así que
`scripts/generate_favicon.py --check` puede compararla byte a byte.
"""
from libra_web_kit.iconos_bootstrap import TRAZOS
from libra_web_kit.identidad import IDENTIDAD, nombre_icono

#: Lado del lienzo. El tamaño real lo pone el navegador (`viewBox`).
LADO = 64
#: Radio de las esquinas: 14/64 = 21,9 % del lado (el documento pide ~22 %).
RADIO = 14
#: Lado del ícono respecto del lienzo.
PROPORCION_ICONO = 0.6
#: Los íconos de Bootstrap Icons se dibujan en una grilla de 16 x 16.
GRILLA_ICONO = 16


def _num(valor: float) -> str:
    """12.8 -> '12.8', 2.0 -> '2' (sin ceros de más ni notación científica)."""
    return f"{valor:.4f}".rstrip("0").rstrip(".")


def favicon_svg(sitio: str) -> str:
    """El SVG del favicon de un sitio (clave de `identidad.IDENTIDAD`)."""
    if sitio not in IDENTIDAD:
        raise KeyError(f"sitio desconocido: {sitio!r} (conocidos: {sorted(IDENTIDAD)})")
    ident = IDENTIDAD[sitio]
    escala = LADO * PROPORCION_ICONO / GRILLA_ICONO
    desplazamiento = (LADO - LADO * PROPORCION_ICONO) / 2
    trazos = []
    for d, fill_rule in TRAZOS[nombre_icono(sitio)]:
        regla = f' fill-rule="{fill_rule}"' if fill_rule else ""
        trazos.append(f'<path{regla} d="{d}"/>')
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LADO} {LADO}">'
        f"<title>{ident.nombre}</title>"
        f'<rect width="{LADO}" height="{LADO}" rx="{RADIO}" fill="{ident.color}"/>'
        f'<g transform="translate({_num(desplazamiento)} {_num(desplazamiento)}) scale({_num(escala)})" fill="#fff">'
        + "".join(trazos)
        + "</g></svg>\n"
    )


def render_all() -> dict[str, str]:
    """{sitio: svg} para los ocho sitios."""
    return {sitio: favicon_svg(sitio) for sitio in IDENTIDAD}
