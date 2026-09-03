"""Abre, en el repo del consumidor donde se lo corre, un PR por cada motor de la
familia Libra cuyo tag publicado sea mas nuevo que el pin actual.

Es "lo que se hacia a mano con un worktree por producto", una vez por repo,
disparado por el reusable workflow `bump-motores.yml` de este mismo repo
(libra-web-kit) — cron diario mas boton manual. Vive aca, en un solo lugar: un
arreglo al bumpeo se propaga a los diez consumidores sin tocar sus repos.

Formatos de pin que entiende, que son los dos que usa la familia:

  pyproject.toml  "libracore[extras] @ git+https://github.com/OWNER/libracore.git@vX.Y.Z",
  package.json    "libra-ui": "github:OWNER/libra-ui#vX.Y.Z",

Para el pin de package.json ademas re-resuelve el `package-lock.json` con
`npm install`, porque el lock guarda el SHA del tag y no se mueve solo — es el
mismo pozo que aparecio al bumpear a mano (el lock decia la version nueva y
node_modules seguia en la vieja).

No hace nada si el pin ya esta al dia, y es idempotente: si ya existe la rama o
el PR para ese bump, lo deja como esta. En `--dry-run` (el default) imprime lo
que haria y no toca nada ni la red de escritura.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tomllib
import urllib.request

OWNER = "marianocappucci"
# Los siete motores de la familia. El script solo actua sobre los que el repo
# realmente pinea; esta lista es para no confundir un `libracore` cualquiera en
# un comentario con una dependencia.
MOTORES = [
    "libracore", "libraauth", "libracommerce", "libragenda", "libraedge",
    "libra-ui", "libra-web-kit",
]

# --- pyproject: "<motor>[extras] @ git+.../<motor>.git@vX.Y.Z"
_PY = re.compile(
    r'(?P<full>"(?P<name>libra[\w-]*)(?P<extras>\[[^\]]*\])?\s*@\s*'
    r'git\+https://github\.com/' + re.escape(OWNER) +
    r'/(?P<repo>libra[\w-]*)\.git@)(?P<ver>v\d+\.\d+\.\d+)"'
)
# --- package.json: "<motor>": "github:OWNER/<repo>#vX.Y.Z"
_JS = re.compile(
    r'("(?P<name>libra[\w-]*)"\s*:\s*"github:' + re.escape(OWNER) +
    r'/(?P<repo>libra[\w-]*)#)(?P<ver>v\d+\.\d+\.\d+)"'
)


def _semver(tag: str) -> tuple[int, int, int] | None:
    m = re.fullmatch(r"v(\d+)\.(\d+)\.(\d+)", tag)
    return (int(m[1]), int(m[2]), int(m[3])) if m else None


def _sh(*args: str, cwd: str | None = None, check: bool = True) -> str:
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"{' '.join(args)} -> {r.returncode}\n{r.stderr}")
    return r.stdout


def _ultimo_tag(repo: str) -> str | None:
    """El tag semver mas alto del motor. Repos publicos: sin credencial."""
    out = _sh("git", "ls-remote", "--tags",
              f"https://github.com/{OWNER}/{repo}.git", check=False)
    tags = []
    for line in out.splitlines():
        m = re.search(r"refs/tags/(v\d+\.\d+\.\d+)$", line)  # ignora ^{} y no-semver
        if m and _semver(m[1]):
            tags.append(m[1])
    return max(tags, key=_semver) if tags else None


def _pines(repo_dir: str) -> dict:
    """{repo_motor: [(archivo, name, ver, tipo), ...]} — un motor puede estar en
    pyproject y en package.json a la vez (no pasa hoy, pero no se asume)."""
    encontrados: dict = {}
    for rel, rx, tipo in [
        ("pyproject.toml", _PY, "py"),
        ("frontend/package.json", _JS, "js"),
        ("package.json", _JS, "js"),
    ]:
        path = os.path.join(repo_dir, rel)
        if not os.path.isfile(path):
            continue
        txt = open(path, encoding="utf-8").read()
        for m in rx.finditer(txt):
            repo = m.group("repo")
            if repo not in MOTORES:
                continue
            encontrados.setdefault(repo, []).append(
                {"archivo": rel, "name": m.group("name"), "ver": m.group("ver"),
                 "tipo": tipo})
    return encontrados


def _cambiar_pin(repo_dir: str, rel: str, tipo: str, repo: str, nueva: str) -> None:
    path = os.path.join(repo_dir, rel)
    txt = open(path, encoding="utf-8").read()
    rx = _PY if tipo == "py" else _JS

    def repl(m: re.Match) -> str:
        if m.group("repo") != repo:
            return m.group(0)
        # reconstruye conservando prefijo (name/extras/url) y cambiando solo la version
        return m.group(0)[: m.start("ver") - m.start(0)] + nueva + m.group(0)[m.end("ver") - m.start(0):]

    nuevo = rx.sub(repl, txt)
    if nuevo == txt:
        raise RuntimeError(f"no se cambio nada en {rel} para {repo}")
    open(path, "w", encoding="utf-8", newline="\n" if not txt.endswith("\r\n") else "\r\n").write(nuevo)


def _refrescar_lock(repo_dir: str, rel_pkg: str, repo: str, nueva: str) -> str | None:
    """Re-resuelve el lock del dep de git: npm deja node_modules en la version
    vieja aunque el lock ya declare la nueva, hasta forzar la re-instalacion."""
    fe = os.path.dirname(os.path.join(repo_dir, rel_pkg))
    if not os.path.isfile(os.path.join(fe, "package-lock.json")):
        return None
    _sh("npm", "install", f"{repo}@github:{OWNER}/{repo}#{nueva}",
        "--no-audit", "--no-fund", cwd=fe)
    return os.path.relpath(os.path.join(fe, "package-lock.json"), repo_dir)


def _rama_o_pr_existe(repo_dir: str, rama: str) -> bool:
    remoto = _sh("git", "ls-remote", "--heads", "origin", rama,
                 cwd=repo_dir, check=False).strip()
    if remoto:
        return True
    pr = _sh("gh", "pr", "list", "--head", rama, "--state", "all",
             "--json", "number", cwd=repo_dir, check=False).strip()
    try:
        return bool(json.loads(pr or "[]"))
    except json.JSONDecodeError:
        return False


def procesar(repo_dir: str, dry_run: bool) -> int:
    pines = _pines(repo_dir)
    if not pines:
        print("Este repo no pinea ningun motor de la familia.")
        return 0
    hechos = 0
    for repo, usos in sorted(pines.items()):
        actual = min((u["ver"] for u in usos), key=_semver)  # el mas atrasado de sus usos
        ultimo = _ultimo_tag(repo)
        if ultimo is None:
            print(f"  {repo}: no pude leer los tags, salteo")
            continue
        if _semver(ultimo) <= _semver(actual):
            print(f"  {repo}: al dia ({actual})")
            continue
        rama = f"chore/bump-{repo}-{ultimo}"
        print(f"  {repo}: {actual} -> {ultimo}  (rama {rama})")
        if dry_run:
            for u in usos:
                print(f"      cambiaria {u['archivo']} ({u['tipo']})")
            hechos += 1
            continue
        if _rama_o_pr_existe(repo_dir, rama):
            print("      ya hay rama o PR para este bump, salteo")
            continue
        _sh("git", "checkout", "-B", rama, cwd=repo_dir)
        tocados = []
        for u in usos:
            _cambiar_pin(repo_dir, u["archivo"], u["tipo"], repo, ultimo)
            tocados.append(u["archivo"])
            if u["tipo"] == "js":
                lock = _refrescar_lock(repo_dir, u["archivo"], repo, ultimo)
                if lock:
                    tocados.append(lock)
        _sh("git", "add", *tocados, cwd=repo_dir)
        cuerpo = (
            f"Bump automatico de **{repo}** de `{actual}` a `{ultimo}`.\n\n"
            f"Lo abre el workflow `bump-motores` (cron diario) al detectar que el tag "
            f"publicado del motor es mas nuevo que el pin de este repo. Es el mismo "
            f"cambio que antes se hacia a mano con un worktree por producto.\n\n"
            f"El CI de este PR es la verificacion: mergear solo si queda verde.\n\n"
            f"\U0001f916 Generated with [Claude Code](https://claude.com/claude-code)\n"
        )
        _sh("git", "commit", "-m",
            f"chore: el pin de {repo} pasa de {actual} a {ultimo}", cwd=repo_dir)
        _sh("git", "push", "-u", "origin", rama, cwd=repo_dir)
        _sh("gh", "pr", "create", "--base", "develop", "--head", rama,
            "--title", f"chore: el pin de {repo} pasa a {ultimo}",
            "--body", cuerpo, cwd=repo_dir)
        hechos += 1
    return hechos


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-dir", default=".")
    ap.add_argument("--apply", action="store_true",
                    help="Abre los PR de verdad. Sin esto, dry-run.")
    args = ap.parse_args()
    n = procesar(os.path.abspath(args.repo_dir), dry_run=not args.apply)
    print(f"\n{'PRs abiertos' if args.apply else 'bumps que se abririan'}: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
