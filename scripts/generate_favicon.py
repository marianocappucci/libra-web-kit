#!/usr/bin/env python3
"""Escribe `public/img/favicon.svg` en los repos hermanos de landings a partir de
`libra_web_kit.favicon_gen` -- el icono plano de cada producto (cuadrado redondeado
del color de marca con el icono de Bootstrap Icons en blanco), tomado de
`libra_web_kit.identidad`.

La home (`public/index.html`) es **a mano**, no la genera el kit, asi que el script
tambien la *mira*: que el `<head>` apunte al favicon y que el cuadrado de la marca
del navbar y del pie lleve el icono del producto y no una inicial. Si no, un cambio
de icono en `identidad.py` regeneraria el favicon y dejaria la home vieja sin avisar.
Las paginas de `/docs/` y de `/legal/` si las genera el kit (`generate_docs.py`,
`generate_legal.py`).

Uso, con el venv del kit:
    .venv/bin/python scripts/generate_favicon.py            # escribe los SVG, avisa de las homes
    .venv/bin/python scripts/generate_favicon.py --check    # no escribe; exit 1 si algo difiere

Sin PNG: ver el docstring de `favicon_gen.py`.
"""
import argparse
import re
import sys
from pathlib import Path

from libra_web_kit.favicon_gen import render_all
from libra_web_kit.identidad import marca_icono_html

#: 🔴 Mismo riesgo que en los otros tres scripts: un sitio de `IDENTIDAD` que falte
#: aca no se escribe en ningun lado. `tests/test_scripts_destinos.py` exige que
#: coincidan.
REPO_DIR_BY_SITE = {
    "contalibra": "contalibra.com.ar",
    "restolibra": "restolibra.com.ar",
    "gestiolibra": "gestiolibra_web",
    "medlibra": "medlibra_web",
    "ventalibra": "ventalibra_web",
    "libradesk": "libradesk_web",
    "libracargo": "libracargo_web",
    "libraclub": "libraclub_web",
}

RUTA_FAVICON = "img/favicon.svg"
LINK_FAVICON = '<link rel="icon" type="image/svg+xml" href="/img/favicon.svg">'
_LOGO_ICON = re.compile(r'<div class="logo-icon[^"]*"[^>]*>(.*?)</div>', re.S)


def problemas_de_la_home(site: str, html: str) -> list[str]:
    """Lo que le falta a la home de `site` para estar alineada con el kit."""
    problemas = []
    if LINK_FAVICON not in html:
        problemas.append(f"le falta {LINK_FAVICON}")
    esperado = marca_icono_html(site)
    marcas = [m.strip() for m in _LOGO_ICON.findall(html)]
    if len(marcas) < 2:
        problemas.append(f"tiene {len(marcas)} cuadrado(s) .logo-icon y se esperan 2 (navbar y pie)")
    distintas = sorted({m for m in marcas if m != esperado})
    if distintas:
        problemas.append(f"el .logo-icon dice {distintas} y deberia decir {esperado}")
    return problemas


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="No escribe nada; falla (exit 1) si algun favicon o home quedaria distinto.")
    parser.add_argument("--proyectos-dir", default=str(Path(__file__).resolve().parents[2]),
                        help="Directorio que contiene los repos hermanos (default: el padre de libra-web-kit).")
    args = parser.parse_args()

    proyectos_dir = Path(args.proyectos_dir)
    fallas = []
    for site, svg in render_all().items():
        raiz = proyectos_dir / REPO_DIR_BY_SITE[site] / "public"
        if not raiz.exists():
            print(f"[SKIP] {site}: no existe {raiz} (¿repo no clonado?)")
            continue

        destino = raiz / RUTA_FAVICON
        actual = destino.read_text(encoding="utf-8") if destino.exists() else None
        if actual == svg:
            print(f"[OK] {site}: favicon sin cambios")
        elif args.check:
            print(f"[DIFF] {site}: {destino} quedaria distinto")
            fallas.append(f"{site}/{RUTA_FAVICON}")
        else:
            destino.parent.mkdir(parents=True, exist_ok=True)
            destino.write_text(svg, encoding="utf-8", newline="")
            print(f"[WRITE] {site}: {destino}")

        home = raiz / "index.html"
        if not home.exists():
            print(f"[HOME] {site}: no existe {home}")
            fallas.append(f"{site}/index.html")
            continue
        for problema in problemas_de_la_home(site, home.read_text(encoding="utf-8")):
            print(f"[HOME] {site}: {problema}")
            fallas.append(f"{site}/index.html")

    if args.check and fallas:
        print(f"\n{len(fallas)} problema(s)")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
