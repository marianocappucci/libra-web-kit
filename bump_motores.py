"""Abre, en el repo del consumidor donde se lo corre, un PR por cada motor de la
familia Libra cuyo tag publicado sea mas nuevo que el pin actual. Y, desde F0
(2026-09-05), tambien **cierra** los PR de bump que quedaron superados y
**mergea** los que ya estan en verde.

Es "lo que se hacia a mano con un worktree por producto", una vez por repo,
disparado por el reusable workflow `bump-motores.yml` de este mismo repo
(libra-web-kit) — cron diario mas boton manual. Vive aca, en un solo lugar: un
arreglo al bumpeo se propaga a los diez consumidores sin tocar sus repos.

Formatos de pin que entiende, que son los dos que usa la familia:

  pyproject.toml  "libracore[extras] @ git+https://github.com/OWNER/libracore.git@vX.Y.Z",
  package.json    "libra-ui": "github:OWNER/libra-ui#vX.Y.Z",

Para el pin de pyproject.toml, si el repo tiene `uv.lock` (F1), lo regenera con
`uv lock` en el mismo commit: el CI instala con `uv sync --locked` y un lock
viejo pondria rojo el PR de bump.

Para el pin de package.json ademas re-resuelve el `package-lock.json` con
`npm install`, porque el lock guarda el SHA del tag y no se mueve solo — es el
mismo pozo que aparecio al bumpear a mano (el lock decia la version nueva y
node_modules seguia en la vieja).

Las tres pasadas, en este orden:

1. **Abrir**: un PR por motor atrasado, en la rama `chore/bump-<motor>-<tag>`.
   Idempotente: si ya existe la rama o el PR para ese bump, lo deja como esta.
2. **Superar**: si el motor ya tiene un PR de bump abierto a una version MAS
   VIEJA que la que se acaba de abrir (o que ya estaba abierta), ese PR se
   cierra con un comentario que apunta al nuevo y se borra su rama. Antes de
   esto un motor que publicaba dos tags en dos dias dejaba dos PR abiertos por
   consumidor (medido el 2026-09-05: 6 repos con dos PR de libracore).
3. **Mergear**: un PR de bump abierto a la ULTIMA version del motor, con todos
   sus checks en verde (y al menos uno), mergeable, y cuyo salto no es de
   version mayor, se mergea con squash. El CI del consumidor es el gate — es
   el mismo criterio que se aplicaba a mano ("mergear solo si queda verde"),
   sin la persona en el medio. Un salto de mayor (X distinta) queda abierto
   para que lo mire alguien, verde o no: en semver eso declara ruptura.
   Los PR de `dependabot` del grupo `actions` reciben el mismo trato: son
   cambios de workflow que el propio CI del PR ya ejercito.

En `--dry-run` (el default) imprime lo que haria y no toca nada ni la red de
escritura. `--no-mergear` deja la pasada 3 apagada.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tomllib  # noqa: F401  (documenta que el script exige Python 3.11+)
import urllib.request  # noqa: F401

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
# --- rama de bump: chore/bump-<motor>-vX.Y.Z
_RAMA_BUMP = re.compile(r"^chore/bump-(?P<repo>libra[\w-]*)-(?P<ver>v\d+\.\d+\.\d+)$")
# --- rama de dependabot para el grupo de GitHub Actions
_RAMA_DEPENDABOT_ACTIONS = re.compile(r"^dependabot/github_actions/")

# Conclusiones de un check que cuentan como "verde". `SKIPPED` y `NEUTRAL`
# no ponen rojo (un job con `if:` que no aplico), pero tampoco alcanzan
# solos: hace falta al menos un SUCCESS de verdad --un cero esperado necesita
# un positivo--.
_VERDES = {"SUCCESS", "SKIPPED", "NEUTRAL"}
_ROJOS = {"FAILURE", "CANCELLED", "TIMED_OUT", "ACTION_REQUIRED", "ERROR", "STARTUP_FAILURE"}


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


def _refrescar_lock_py(repo_dir: str) -> str | None:
    """Si el repo tiene `uv.lock` (F1, 2026-09-05), un pin nuevo en pyproject
    lo deja desactualizado y el CI --que instala con `uv sync --locked`-- pone
    rojo el PR de bump. Se regenera aca, en el mismo commit que el pin, igual
    que el package-lock para los pines de npm."""
    if not os.path.isfile(os.path.join(repo_dir, "uv.lock")):
        return None
    _sh("uv", "lock", cwd=repo_dir)
    return "uv.lock"


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


# ---------------------------------------------------------------- pasadas 2 y 3

def _prs_abiertos(repo_dir: str) -> list[dict]:
    """Los PR abiertos del repo con lo que hace falta para decidir sobre ellos."""
    out = _sh("gh", "pr", "list", "--state", "open", "--limit", "100",
              "--json", "number,headRefName,baseRefName,mergeable,statusCheckRollup,author",
              cwd=repo_dir, check=False).strip()
    try:
        return json.loads(out or "[]")
    except json.JSONDecodeError:
        return []


def _bumps_abiertos(prs: list[dict]) -> list[dict]:
    """Solo los PR cuya rama es de bump, con `repo` y `ver` ya parseados."""
    res = []
    for pr in prs:
        m = _RAMA_BUMP.match(pr.get("headRefName") or "")
        if m and _semver(m["ver"]):
            res.append({**pr, "repo": m["repo"], "ver": m["ver"]})
    return res


def _superados(bumps: list[dict], repo: str, ultimo: str) -> list[dict]:
    """PR de bump de `repo` a una version mas vieja que `ultimo`: hay uno mas
    nuevo (abierto o por abrir) que los deja sin sentido."""
    return [b for b in bumps if b["repo"] == repo and _semver(b["ver"]) < _semver(ultimo)]


def _checks_en_verde(rollup: list[dict] | None) -> bool:
    """True solo si TODOS los checks terminaron sin rojo y hay al menos un
    SUCCESS. Sin checks (lista vacia) es False: un PR sin CI no se mergea."""
    if not rollup:
        return False
    hubo_exito = False
    for c in rollup:
        estado = (c.get("conclusion") or c.get("state") or "").upper()
        if estado in _ROJOS:
            return False
        if estado == "SUCCESS":
            hubo_exito = True
        elif estado not in _VERDES:
            # PENDING, IN_PROGRESS, QUEUED, EXPECTED, "" ... todavia no termino
            return False
    return hubo_exito


def _salto_es_mayor(actual: str, nueva: str) -> bool:
    """Cambio de version MAYOR (X distinta). En 0.x tambien puede haber
    ruptura, pero ahi el CI es el que decide; el salto de mayor se deja
    siempre a una persona porque en semver es una declaracion explicita."""
    a, n = _semver(actual), _semver(nueva)
    return bool(a and n) and a[0] != n[0]


def _mergeable(pr: dict) -> bool:
    # gh devuelve MERGEABLE / CONFLICTING / UNKNOWN; UNKNOWN es "todavia no lo
    # calculo", y no se mergea a ciegas.
    return (pr.get("mergeable") or "").upper() == "MERGEABLE"


def _cerrar_superado(repo_dir: str, pr: dict, motivo: str, dry_run: bool) -> None:
    print(f"      cierro #{pr['number']} ({pr['headRefName']}): {motivo}")
    if dry_run:
        return
    _sh("gh", "pr", "close", str(pr["number"]), "--delete-branch",
        "--comment", f"Superado: {motivo}. Lo cierra el workflow `bump-motores`.",
        cwd=repo_dir, check=False)


def _mergear(repo_dir: str, pr: dict, dry_run: bool) -> bool:
    print(f"      mergeo #{pr['number']} ({pr['headRefName']}): checks en verde")
    if dry_run:
        return True
    r = subprocess.run(
        ["gh", "pr", "merge", str(pr["number"]), "--squash", "--delete-branch"],
        cwd=repo_dir, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"      no se pudo mergear #{pr['number']}: {r.stderr.strip()[:300]}")
        return False
    return True


def superar_y_mergear(repo_dir: str, pines: dict, ultimos: dict, dry_run: bool,
                      mergear: bool = True) -> tuple[int, int]:
    """Pasadas 2 y 3 sobre los PR abiertos. Devuelve (cerrados, mergeados)."""
    prs = _prs_abiertos(repo_dir)
    bumps = _bumps_abiertos(prs)
    cerrados = mergeados = 0

    # 2. superar: por cada motor, los bumps a una version mas vieja que la ultima
    for repo, ultimo in sorted(ultimos.items()):
        if not ultimo:
            continue
        for viejo in _superados(bumps, repo, ultimo):
            _cerrar_superado(repo_dir, viejo, f"{repo} ya va por {ultimo}", dry_run)
            cerrados += 1

    if not mergear:
        return cerrados, mergeados

    # 3. mergear: bumps a la ultima version, en verde, sin salto de mayor
    for b in bumps:
        ultimo = ultimos.get(b["repo"])
        if not ultimo or b["ver"] != ultimo:
            continue
        actual = min((u["ver"] for u in pines.get(b["repo"], [])), key=_semver, default=None)
        if actual and _salto_es_mayor(actual, b["ver"]):
            print(f"      #{b['number']}: salto de mayor {actual} -> {b['ver']}, queda para una persona")
            continue
        if not _checks_en_verde(b.get("statusCheckRollup")):
            print(f"      #{b['number']}: checks no estan (todos) en verde todavia")
            continue
        if not _mergeable(b):
            print(f"      #{b['number']}: mergeable={b.get('mergeable')}, no se toca")
            continue
        if _mergear(repo_dir, b, dry_run):
            mergeados += 1

    # 3b. dependabot, grupo de GitHub Actions: mismo gate, mismo destino
    for pr in prs:
        if not _RAMA_DEPENDABOT_ACTIONS.match(pr.get("headRefName") or ""):
            continue
        if not _checks_en_verde(pr.get("statusCheckRollup")) or not _mergeable(pr):
            print(f"      #{pr['number']} ({pr['headRefName']}): dependabot sin verde o sin mergeable, queda")
            continue
        if _mergear(repo_dir, pr, dry_run):
            mergeados += 1
    return cerrados, mergeados


# ---------------------------------------------------------------- pasada 1

def procesar(repo_dir: str, dry_run: bool, mergear: bool = True) -> int:
    pines = _pines(repo_dir)
    if not pines:
        print("Este repo no pinea ningun motor de la familia.")
        return 0
    hechos = 0
    ultimos: dict = {}
    for repo, usos in sorted(pines.items()):
        actual = min((u["ver"] for u in usos), key=_semver)  # el mas atrasado de sus usos
        ultimo = _ultimo_tag(repo)
        ultimos[repo] = ultimo
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
            elif u["tipo"] == "py":
                lock = _refrescar_lock_py(repo_dir)
                if lock and lock not in tocados:
                    tocados.append(lock)
        _sh("git", "add", *tocados, cwd=repo_dir)
        cuerpo = (
            f"Bump automatico de **{repo}** de `{actual}` a `{ultimo}`.\n\n"
            f"Lo abre el workflow `bump-motores` (cron diario) al detectar que el tag "
            f"publicado del motor es mas nuevo que el pin de este repo. Es el mismo "
            f"cambio que antes se hacia a mano con un worktree por producto.\n\n"
            f"El CI de este PR es la verificacion: si queda verde y el salto no es de "
            f"version mayor, el mismo workflow lo mergea en su proxima corrida.\n\n"
            f"\U0001f916 Generated with [Claude Code](https://claude.com/claude-code)\n"
        )
        _sh("git", "commit", "-m",
            f"chore: el pin de {repo} pasa de {actual} a {ultimo}", cwd=repo_dir)
        _sh("git", "push", "-u", "origin", rama, cwd=repo_dir)
        _sh("gh", "pr", "create", "--base", "develop", "--head", rama,
            "--title", f"chore: el pin de {repo} pasa a {ultimo}",
            "--body", cuerpo, cwd=repo_dir)
        hechos += 1

    # volver a la rama base antes de tocar PRs ajenos: los merges no dependen
    # del checkout, pero un `gh pr close --delete-branch` de la rama actual si.
    if not dry_run:
        _sh("git", "checkout", "-q", "develop", cwd=repo_dir, check=False)
    cerrados, mergeados = superar_y_mergear(repo_dir, pines, ultimos, dry_run, mergear)
    print(f"  PR superados cerrados: {cerrados} | mergeados en verde: {mergeados}")
    return hechos


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-dir", default=".")
    ap.add_argument("--apply", action="store_true",
                    help="Abre, cierra y mergea los PR de verdad. Sin esto, dry-run.")
    ap.add_argument("--no-mergear", action="store_true",
                    help="No mergea los PR en verde (deja las pasadas 1 y 2).")
    args = ap.parse_args()
    n = procesar(os.path.abspath(args.repo_dir), dry_run=not args.apply,
                 mergear=not args.no_mergear)
    print(f"\n{'PRs abiertos' if args.apply else 'bumps que se abririan'}: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
