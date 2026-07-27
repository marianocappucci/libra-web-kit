#!/usr/bin/env python3
"""Regenera `public/docs/*.html` en los 5 repos hermanos de landings
(Contalibra, Restolibra, Gestiolibra, MedLibra, VentaLibra) a partir de
`libra_web_kit.docs_gen` -- fuente de verdad unica para el shell
(navbar/sidebar/footer) de la documentacion. El contenido de cada pagina
sigue viviendo en `libra_web_kit/docs_content/<sitio>/<archivo>.html`
(fragmento HTML, se edita ahi -- no en el HTML final generado).

Uso: correr desde cualquier lado con el venv de libra-web-kit activo.
    .venv/bin/python scripts/generate_docs.py            # escribe las 82 paginas
    .venv/bin/python scripts/generate_docs.py --check     # solo verifica, no escribe (exit 1 si difiere)
"""
import argparse
import sys
from pathlib import Path

from libra_web_kit.docs_gen import list_pages, render
from libra_web_kit.docs_pages import PAGES

REPO_DIR_BY_SITE = {
    "contalibra": "contalibra.com.ar",
    "restolibra": "restolibra.com.ar",
    "gestiolibra": "gestiolibra_web",
    "medlibra": "medlibra_web",
    "ventalibra": "ventalibra_web",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="No escribe nada; falla (exit 1) si alguna pagina quedaria distinta.")
    parser.add_argument("--proyectos-dir", default=str(Path(__file__).resolve().parents[2]),
                        help="Directorio que contiene los repos hermanos (default: el padre de libra-web-kit).")
    args = parser.parse_args()

    proyectos_dir = Path(args.proyectos_dir)
    changed = []
    written = 0
    for site in PAGES:
        docs_dir = proyectos_dir / REPO_DIR_BY_SITE[site] / "public" / "docs"
        if not docs_dir.exists():
            print(f"[SKIP] {site}: no existe {docs_dir} (¿repo no clonado?)")
            continue
        for fname in list_pages(site):
            target = docs_dir / fname
            html = render(site, fname)
            current = target.read_text(encoding="utf-8") if target.exists() else None
            if current == html:
                continue
            changed.append((site, fname))
            if args.check:
                print(f"[DIFF] {site}/{fname}")
            else:
                target.write_text(html, encoding="utf-8")
                written += 1

    if args.check:
        if changed:
            print(f"\n{len(changed)} pagina(s) desactualizada(s)")
            return 1
        print("Las 82 paginas ya coinciden con lo generado.")
        return 0

    print(f"[OK] {written} pagina(s) escritas, {sum(len(list_pages(s)) for s in PAGES) - written} sin cambios")
    return 0


if __name__ == "__main__":
    sys.exit(main())
