#!/usr/bin/env python3
"""Regenera `public/css/style.css` en los repos hermanos de landings a partir
de `libra_web_kit.css_gen` — fuente de verdad unica para el CSS compartido.

Uso: correr desde cualquier lado con el venv de libra-web-kit activo.
    .venv/bin/python scripts/generate_css.py            # escribe todos
    .venv/bin/python scripts/generate_css.py --check     # solo verifica, no escribe (exit 1 si difiere)

Asume que los repos viven como hermanos de `libra-web-kit` en `~/proyectos/`
(mismo layout que documenta wiki/entities/*-web.md). El que no este clonado se
saltea con un aviso.
"""
import argparse
import sys
from pathlib import Path

from libra_web_kit.css_gen import render_all

#: 🔴 Un sitio nuevo en `site_css_tokens.SITES` que no aparezca aca **no se
#: escribe en ningun lado**, y el script termina en 0 igual. Por eso hay un
#: test que exige que las dos listas coincidan
#: (tests/test_css_gen.py::test_todos_los_sitios_tienen_repo_destino) en vez de
#: confiar en que quien agrega un sitio se acuerde de las dos mitades.
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="No escribe nada; falla (exit 1) si algun style.css quedaria distinto.")
    parser.add_argument("--proyectos-dir", default=str(Path(__file__).resolve().parents[2]),
                        help="Directorio que contiene los repos hermanos (default: el padre de libra-web-kit).")
    args = parser.parse_args()

    proyectos_dir = Path(args.proyectos_dir)
    rendered = render_all()

    changed = []
    for site, css in rendered.items():
        target = proyectos_dir / REPO_DIR_BY_SITE[site] / "public" / "css" / "style.css"
        if not target.parent.exists():
            print(f"[SKIP] {site}: no existe {target.parent} (¿repo no clonado?)")
            continue
        current = target.read_text(encoding="utf-8") if target.exists() else None
        if current == css:
            print(f"[OK] {site}: sin cambios ({target})")
            continue
        changed.append(site)
        if args.check:
            print(f"[DIFF] {site}: {target} quedaria distinto")
        else:
            target.write_text(css, encoding="utf-8")
            print(f"[WRITE] {site}: {target}")

    if args.check and changed:
        print(f"\n{len(changed)} sitio(s) desactualizados: {changed}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
