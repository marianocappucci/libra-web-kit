#!/usr/bin/env python3
"""Copia la marca dibujada de cada producto a los repos hermanos de landings:
`public/img/favicon.svg` (la variante reducida, para 16-32 px) y `public/img/marca.svg`
(la marca completa, la del navbar y del pie). Los SVG son los de libra-ui (ADR-034),
copiados al kit por `scripts/sincronizar_marcas.py` y servidos por
`libra_web_kit.marcas_gen`; esto los pasa **byte a byte**, sin redibujar nada (kit ADR-009,
que reemplaza el dibujo en Python de ADR-008).

La home (`public/index.html`) es **a mano**, no la genera el kit, asi que el script
tambien la *mira*: que el `<head>` apunte al favicon, que el navbar y el pie lleven la
marca (`<img src="/img/marca.svg">`) y que no quede ningun cuadrado `.logo-icon` viejo
(inicial o glifo). Las paginas de `/docs/` y de `/legal/` si las genera el kit
(`generate_docs.py`, `generate_legal.py`).

Uso, con el venv del kit:
    .venv/bin/python scripts/generate_favicon.py            # escribe los SVG, avisa de las homes
    .venv/bin/python scripts/generate_favicon.py --check    # no escribe; exit 1 si algo difiere

Sin PNG: ver el docstring de `marcas_gen.py`.
"""
import argparse
import re
import sys
from pathlib import Path

from libra_web_kit.marcas_gen import RUTA_FAVICON, RUTA_MARCA, render_all

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

LINK_FAVICON = f'<link rel="icon" type="image/svg+xml" href="/{RUTA_FAVICON}">'
#: La marca del navbar y del pie: una <img> al SVG, con las dos medidas.
_MARCA_IMG = re.compile(rf'<img\b[^>]*\bsrc="/{re.escape(RUTA_MARCA)}"[^>]*>')
#: Un cuadrado de la marca anterior (inicial o glifo de Bootstrap Icons).
_CUADRADO_VIEJO = re.compile(r'<div\b[^>]*\bclass="[^"]*\blogo-icon\b')
MARCAS_ESPERADAS = 2  # navbar y pie


def problemas_de_la_home(html: str) -> list[str]:
    """Lo que le falta a una home para estar alineada con el kit (es igual para los ocho)."""
    problemas = []
    if LINK_FAVICON not in html:
        problemas.append(f"le falta {LINK_FAVICON}")
    marcas = _MARCA_IMG.findall(html)
    if len(marcas) != MARCAS_ESPERADAS:
        problemas.append(
            f'tiene {len(marcas)} <img src="/{RUTA_MARCA}"> y se esperan {MARCAS_ESPERADAS} (navbar y pie)'
        )
    for marca in marcas:
        if not re.search(r'\bwidth="\d+"', marca) or not re.search(r'\bheight="\d+"', marca):
            problemas.append(f"la marca {marca} no declara width y height")
    viejos = len(_CUADRADO_VIEJO.findall(html))
    if viejos:
        problemas.append(f"quedan {viejos} cuadrado(s) <div class=\"logo-icon\"> de la marca anterior (inicial o glifo)")
    return problemas


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true",
                        help="No escribe nada; falla (exit 1) si algun SVG o home quedaria distinto.")
    parser.add_argument("--proyectos-dir", default=str(Path(__file__).resolve().parents[2]),
                        help="Directorio que contiene los repos hermanos (default: el padre de libra-web-kit).")
    args = parser.parse_args()

    proyectos_dir = Path(args.proyectos_dir)
    fallas = []
    for site, (marca, favicon) in render_all().items():
        raiz = proyectos_dir / REPO_DIR_BY_SITE[site] / "public"
        if not raiz.exists():
            print(f"[SKIP] {site}: no existe {raiz} (¿repo no clonado?)")
            continue

        for ruta, contenido in ((RUTA_FAVICON, favicon), (RUTA_MARCA, marca)):
            destino = raiz / ruta
            actual = destino.read_bytes() if destino.exists() else None
            if actual == contenido:
                print(f"[OK] {site}: {ruta} sin cambios")
            elif args.check:
                print(f"[DIFF] {site}: {destino} quedaria distinto")
                fallas.append(f"{site}/{ruta}")
            else:
                destino.parent.mkdir(parents=True, exist_ok=True)
                destino.write_bytes(contenido)
                print(f"[WRITE] {site}: {destino}")

        home = raiz / "index.html"
        if not home.exists():
            print(f"[HOME] {site}: no existe {home}")
            fallas.append(f"{site}/index.html")
            continue
        for problema in problemas_de_la_home(home.read_text(encoding="utf-8")):
            print(f"[HOME] {site}: {problema}")
            fallas.append(f"{site}/index.html")

    if args.check and fallas:
        print(f"\n{len(fallas)} problema(s)")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
