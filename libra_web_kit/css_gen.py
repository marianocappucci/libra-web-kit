"""Generador del `style.css` compartido de las 5 landings de la familia
Libra (Contalibra, Restolibra, Gestiolibra, MedLibra, VentaLibra).

Historia: los 5 `style.css` eran copy-paste independientes, ~88-96%
identicos en estructura (layout, botones, `.docs-*`, responsive) y
divergiendo solo en unos pocos bloques (paleta de marca, degradado del
hero, badges de plan, footer). Mantener eso significaba tocar 5 archivos
para cualquier fix/feature compartido. Este modulo invierte eso: un
unico `templates/style.css.template` con marcadores `@@slot@@`, mas
`site_css_tokens.SITES[nombre]` con el contenido real (y ya vigente) de
cada slot por sitio.

`render()` es una funcion pura, sin dependencias externas (ni Jinja2):
el template CSS no necesita logica condicional, solo sustitucion de
bloques de texto — usar un motor de templates completo hubiera sido una
capa de mas para lo que en la practica es `str.replace()` repetido.
"""
from importlib import resources

from libra_web_kit.site_css_tokens import SITES

_TEMPLATE_PATH = resources.files("libra_web_kit").joinpath("templates/style.css.template")


def _load_template() -> str:
    return _TEMPLATE_PATH.read_text(encoding="utf-8")


def render(site: str) -> str:
    """Renderiza el `style.css` completo de un sitio. `site` debe ser una
    clave de `site_css_tokens.SITES`. Lanza `KeyError` si al sitio le
    falta algun slot que el template requiere (mismo criterio que un
    template engine real: mejor fallar en el build que generar CSS roto)."""
    if site not in SITES:
        raise KeyError(f"sitio desconocido: {site!r} (conocidos: {sorted(SITES)})")
    template = _load_template()
    slots = SITES[site]
    out = template
    for name, content in slots.items():
        marker = f"@@{name}@@\n"
        if marker in out:
            out = out.replace(marker, content, 1)
        elif f"@@{name}@@" in out:
            out = out.replace(f"@@{name}@@", content, 1)
    if "@@" in out:
        import re
        faltantes = re.findall(r"@@(\w+)@@", out)
        raise KeyError(f"{site}: faltan valores para los slots {faltantes} — revisar site_css_tokens.py")
    return out


def render_all() -> dict[str, str]:
    """Renderiza los 5 sitios. Util para el script de generacion y para tests."""
    return {site: render(site) for site in SITES}
