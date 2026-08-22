#!/usr/bin/env python3
"""Escribe `public/legal/terminos.html` y el Markdown original en los ocho
repos de landings, a partir de `libra_web_kit.legal_gen`.

El texto sale de `libraauth.terminos`, que es de donde las ocho instancias
sacan el hash que exigen aceptar. Por eso no hay contenido que editar aca: para
cambiar el contrato se edita `libraauth/legal/terminos_v1.md`, se sube
`VERSION_VIGENTE`, se publica una version nueva del motor y recien despues se
corre esto.

Uso, con el venv del kit:
    .venv/bin/python scripts/generate_legal.py            # escribe
    .venv/bin/python scripts/generate_legal.py --check    # verifica, exit 1 si difiere
"""
import argparse
import sys
from pathlib import Path

from libra_web_kit.legal_gen import (
    RUTA_HTML, RUTA_MARKDOWN, markdown_publicado, render, sitios,
)

#: 🔴 Mismo riesgo que en `generate_docs.py` y `generate_css.py`: un sitio de
#: `SIDEBARS` que falte aca revienta con `KeyError` en el medio del recorrido y
#: deja escritos los anteriores. `test_todos_los_sitios_tienen_repo_destino_legal`
#: lo agarra antes.
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
                        help="No escribe nada; falla (exit 1) si algo quedaria distinto.")
    parser.add_argument("--proyectos-dir", default=str(Path(__file__).resolve().parents[2]),
                        help="Directorio con los repos hermanos (default: el padre de libra-web-kit).")
    args = parser.parse_args()

    proyectos_dir = Path(args.proyectos_dir)
    md = markdown_publicado()
    distintos: list[str] = []
    escritos = 0

    for site in sitios():
        raiz = proyectos_dir / REPO_DIR_BY_SITE[site] / "public"
        if not raiz.exists():
            print(f"[SKIP] {site}: no existe {raiz} (¿repo no clonado?)")
            continue

        for ruta, contenido in ((RUTA_HTML, render(site)), (RUTA_MARKDOWN, md)):
            destino = raiz / ruta
            actual = destino.read_text(encoding="utf-8") if destino.exists() else None
            if actual == contenido:
                continue
            distintos.append(f"{site}/{ruta}")
            if args.check:
                print(f"[DIFF] {site}/{ruta}")
            else:
                destino.parent.mkdir(parents=True, exist_ok=True)
                # `newline=""` con el contenido ya en LF: sin esto, corrido desde
                # Windows, Python traduce cada \n a \r\n al escribir y el
                # `sha256sum` del .md publicado deja de coincidir con el que la
                # pagina anuncia — que es justamente lo unico que ese archivo
                # existe para permitir verificar.
                with open(destino, "w", encoding="utf-8", newline="") as fh:
                    fh.write(contenido)
                escritos += 1

    if args.check:
        if distintos:
            print(f"\n{len(distintos)} archivo(s) desactualizado(s)")
            return 1
        print("Los ocho sitios ya tienen publicada la versión vigente.")
        return 0

    print(f"[OK] {escritos} archivo(s) escrito(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
