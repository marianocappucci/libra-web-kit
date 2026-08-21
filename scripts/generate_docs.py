#!/usr/bin/env python3
"""Regenera `public/docs/*.html` en los repos hermanos de landings a partir de
`libra_web_kit.docs_gen` -- fuente de verdad unica para el shell
(navbar/sidebar/footer) de la documentacion. El contenido de cada pagina
sigue viviendo en `libra_web_kit/docs_content/<sitio>/<archivo>.html`
(fragmento HTML, se edita ahi -- no en el HTML final generado).

Uso: correr desde cualquier lado con el venv de libra-web-kit activo.
    .venv/bin/python scripts/generate_docs.py            # escribe todas las paginas
    .venv/bin/python scripts/generate_docs.py --check     # solo verifica, no escribe (exit 1 si difiere)
"""
import argparse
import sys
from pathlib import Path

from libra_web_kit.docs_gen import list_pages, render
from libra_web_kit.docs_pages import PAGES

#: 🔴 Mismo riesgo que en `generate_css.py`: un sitio de `PAGES` que falte aca
#: hace que `REPO_DIR_BY_SITE[site]` reviente con `KeyError` en el medio del
#: recorrido, dejando escritos los sitios anteriores. El test
#: `test_todos_los_sitios_tienen_repo_destino` lo agarra antes.
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
                        help="No escribe nada; falla (exit 1) si alguna pagina quedaria distinta.")
    parser.add_argument("--proyectos-dir", default=str(Path(__file__).resolve().parents[2]),
                        help="Directorio que contiene los repos hermanos (default: el padre de libra-web-kit).")
    parser.add_argument("--forzar-divergentes", action="store_true",
                        help="Escribe tambien en los sitios que divergieron del kit. "
                             "PISA lo que tengan de mas. Solo despues de traer esas "
                             "paginas a docs_content/.")
    args = parser.parse_args()

    proyectos_dir = Path(args.proyectos_dir)
    changed = []
    written = 0
    total = sum(len(list_pages(s)) for s in PAGES)
    for site in PAGES:
        docs_dir = proyectos_dir / REPO_DIR_BY_SITE[site] / "public" / "docs"
        if not docs_dir.exists():
            print(f"[SKIP] {site}: no existe {docs_dir} (¿repo no clonado?)")
            continue

        # 🔴 **Un sitio que tiene paginas que el kit no conoce se saltea.**
        #
        # No es una precaucion teorica: `libradesk_web` esta asi desde el
        # 2026-08-20 —21 archivos en `public/docs/` contra 15 en `PAGES`—
        # porque alguien escribio `recorrido.html`, `agenda.html`, `stock.html`
        # y companía **en el repo generado** en vez de en `docs_content/`.
        #
        # Sin esta guarda, correr el generador por cualquier otro motivo
        # —agregar un sitio nuevo, por ejemplo— reescribe las 15 paginas que SI
        # conoce con un sidebar que no menciona a las otras 6. Las 6 quedan
        # vivas en el disco y **sin ningun link que lleve a ellas**: no hay
        # error, no hay 404, y el unico sintoma es documentacion publicada que
        # el cliente ya no puede encontrar. Paso dos veces en la misma sesion
        # antes de que existiera esto.
        #
        # La salida NO es borrar las paginas de mas: es traerlas a
        # `docs_content/<sitio>/` y registrarlas, que es donde tendrian que
        # haber nacido.
        de_mas = sorted(
            p.name for p in docs_dir.iterdir()
            if p.suffix == ".html" and p.name not in PAGES[site]
        )
        if de_mas and not args.forzar_divergentes:
            print(f"[SALTEADO] {site}: el repo tiene {len(de_mas)} pagina(s) que el kit "
                  f"no conoce, asi que regenerar dejaria huerfanas: {de_mas}")
            print(f"            Traelas a docs_content/{site}/ y registralas en "
                  f"docs_pages/docs_sidebars, o pasa --forzar-divergentes para pisarlas.")
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
        print(f"Las {total} paginas ya coinciden con lo generado.")
        return 0

    print(f"[OK] {written} pagina(s) escritas, {sum(len(list_pages(s)) for s in PAGES) - written} sin cambios")
    return 0


if __name__ == "__main__":
    sys.exit(main())
