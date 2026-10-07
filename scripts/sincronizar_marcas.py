#!/usr/bin/env python3
"""Copia las marcas dibujadas de libra-ui a `libra_web_kit/marcas/`, byte a byte.

Las ocho marcas (`marcas/<p>.svg`, la marca completa, y `marcas/<p>-favicon.svg`, la
reducida para 16-32 px) las dibuja `libra-ui/src/marcas.ts` (libra-ui ADR-034) y viven
en el repo de libra-ui. El kit NO las redibuja: las copia, y `libra_web_kit.marcas_gen`
las sirve a `scripts/generate_favicon.py`. Acá está el camino de la copia.

Uso, con el venv del kit:
    .venv/bin/python scripts/sincronizar_marcas.py                         # tag TAG_POR_DEFECTO de ../libra-ui
    .venv/bin/python scripts/sincronizar_marcas.py --tag v0.125.0          # otra versión
    .venv/bin/python scripts/sincronizar_marcas.py --desde-dir ~/proyectos/libra-ui/marcas
    .venv/bin/python scripts/sincronizar_marcas.py --check                 # no escribe; exit 1 si difieren

Con `--tag` lee con `git show <tag>:marcas/<archivo>` (no toca el árbol de trabajo de
libra-ui ni exige tenerlo en ese tag). Con `--desde-dir` lee el directorio tal cual (una
rama sin tag, para probar). Deja `libra_web_kit/marcas/ORIGEN.txt` con de dónde salieron.

Al subir de versión: correr el script, correr los tests (`tests/test_marcas.py` verifica
que estén los 16 y el color de `IDENTIDAD`), cambiar `TAG_POR_DEFECTO` y volver a correr
`scripts/generate_favicon.py` contra cada landing.
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

from libra_web_kit.identidad import IDENTIDAD

#: La versión de libra-ui de la que salen las marcas del kit.
TAG_POR_DEFECTO = "v0.124.0"

DESTINO = Path(__file__).resolve().parents[1] / "libra_web_kit" / "marcas"
#: `LIBRA_UI_DIR` lo cambia (p. ej. desde un worktree del kit, donde el hermano no está).
LIBRA_UI_POR_DEFECTO = Path(os.environ.get("LIBRA_UI_DIR") or Path(__file__).resolve().parents[2] / "libra-ui")


def nombres_de_archivo() -> list[str]:
    """Los 16 archivos que tiene que haber: la marca y el favicon de cada producto."""
    return [f"{sitio}{variante}.svg" for sitio in sorted(IDENTIDAD) for variante in ("", "-favicon")]


def leer_de_tag(repo: Path, tag: str) -> tuple[dict[str, bytes], str]:
    """{archivo: bytes} de `marcas/` en `tag` de `repo`, y el commit al que apunta el tag."""

    def git(*args: str) -> bytes:
        return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True).stdout

    commit = git("rev-parse", f"{tag}^{{commit}}").decode().strip()
    return {n: git("show", f"{tag}:marcas/{n}") for n in nombres_de_archivo()}, commit


def leer_de_directorio(directorio: Path) -> dict[str, bytes]:
    return {n: (directorio / n).read_bytes() for n in nombres_de_archivo()}


def origen_txt(origen: str, comando: str) -> str:
    return (
        "Marcas dibujadas de la familia Libra: copia byte a byte de libra-ui (ADR-034).\n"
        "No se editan a mano ni se redibujan: se vuelven a copiar con\n"
        "scripts/sincronizar_marcas.py y se cambia TAG_POR_DEFECTO ahi.\n"
        "\n"
        f"origen:  {origen}\n"
        f"comando: {comando}\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--libra-ui", default=str(LIBRA_UI_POR_DEFECTO), help="Checkout de libra-ui (default: $LIBRA_UI_DIR o ../libra-ui, el hermano del kit).")
    parser.add_argument("--tag", default=TAG_POR_DEFECTO, help=f"Tag de libra-ui (default: {TAG_POR_DEFECTO}).")
    parser.add_argument("--desde-dir", help="Leer de este directorio en vez de un tag (no deja versión en ORIGEN.txt).")
    parser.add_argument("--destino", default=str(DESTINO), help="Dónde escribir (default: libra_web_kit/marcas/).")
    parser.add_argument("--check", action="store_true", help="No escribe; exit 1 si el destino difiere del origen.")
    args = parser.parse_args()

    destino = Path(args.destino)
    if args.desde_dir:
        marcas = leer_de_directorio(Path(args.desde_dir))
        origen = f"directorio {Path(args.desde_dir).resolve()} (sin versión)"
        comando = f"python scripts/sincronizar_marcas.py --desde-dir {args.desde_dir}"
    else:
        try:
            marcas, commit = leer_de_tag(Path(args.libra_ui), args.tag)
        except subprocess.CalledProcessError as e:
            print(f"No pude leer {args.tag} de {args.libra_ui} (¿--libra-ui apunta a un checkout con ese tag?):\n"
                  f"{e.stderr.decode(errors='replace')}", file=sys.stderr)
            return 2
        origen = f"libra-ui {args.tag} ({commit})"
        comando = f"python scripts/sincronizar_marcas.py --tag {args.tag}"

    distintos = [n for n, b in marcas.items() if not (destino / n).exists() or (destino / n).read_bytes() != b]
    if args.check:
        for n in distintos:
            print(f"[DIFF] {n}")
        print(f"{len(distintos)} archivo(s) distintos de {origen}")
        return 1 if distintos else 0

    destino.mkdir(parents=True, exist_ok=True)
    for n, b in marcas.items():
        (destino / n).write_bytes(b)
    (destino / "ORIGEN.txt").write_text(origen_txt(origen, comando), encoding="utf-8", newline="")
    print(f"[WRITE] {len(marcas)} marcas en {destino} ({len(distintos)} cambiadas) desde {origen}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
