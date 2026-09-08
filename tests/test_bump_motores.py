"""Las pasadas 2 y 3 de `bump_motores.py` (superar y mergear), sobre datos con
la forma que devuelve `gh pr list --json`. Sin red: `_prs_abiertos` y los
comandos de escritura se reemplazan, y se asertan los comandos que se
habrian corrido."""
from __future__ import annotations

import importlib.util
import pathlib
import subprocess

import pytest

_RAIZ = pathlib.Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("bump_motores", _RAIZ / "bump_motores.py")
bm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bm)


def _pr(num, rama, checks=("SUCCESS", "SUCCESS"), mergeable="MERGEABLE"):
    return {
        "number": num, "headRefName": rama, "baseRefName": "develop",
        "mergeable": mergeable,
        "statusCheckRollup": [{"conclusion": c} for c in checks],
        "author": {"login": "app/libra-bump"},
    }


# ---------------------------------------------------------------- puras

def test_bumps_abiertos_parsea_solo_las_ramas_de_bump():
    prs = [_pr(1, "chore/bump-libracore-v1.83.0"), _pr(2, "feature/otra"),
           _pr(3, "chore/bump-libra-ui-v0.59.0"), _pr(4, "chore/bump-libracore-nope")]
    b = bm._bumps_abiertos(prs)
    assert [(x["number"], x["repo"], x["ver"]) for x in b] == [
        (1, "libracore", "v1.83.0"), (3, "libra-ui", "v0.59.0")]


def test_superados_son_los_de_version_mas_vieja_del_mismo_motor():
    b = bm._bumps_abiertos([
        _pr(1, "chore/bump-libracore-v1.80.0"), _pr(2, "chore/bump-libracore-v1.83.0"),
        _pr(3, "chore/bump-libragenda-v0.9.1")])
    assert [x["number"] for x in bm._superados(b, "libracore", "v1.83.0")] == [1]
    assert bm._superados(b, "libragenda", "v0.9.1") == []


@pytest.mark.parametrize("rollup, esperado", [
    ([{"conclusion": "SUCCESS"}, {"conclusion": "SUCCESS"}], True),
    ([{"conclusion": "SUCCESS"}, {"conclusion": "SKIPPED"}], True),
    ([{"conclusion": "SUCCESS"}, {"conclusion": "FAILURE"}], False),
    ([{"conclusion": "SUCCESS"}, {"state": "PENDING"}], False),
    ([{"conclusion": None, "state": "IN_PROGRESS"}], False),
    ([{"conclusion": "SKIPPED"}], False),   # sin ningun positivo no alcanza
    ([], False),                            # sin checks no se mergea
    (None, False),
    ([{"state": "SUCCESS"}], True),         # statuses viejos usan `state`
])
def test_checks_en_verde(rollup, esperado):
    assert bm._checks_en_verde(rollup) is esperado


@pytest.mark.parametrize("a, n, mayor", [
    ("v1.80.0", "v1.83.0", False), ("v0.9.1", "v0.10.0", False),
    ("v1.83.0", "v2.0.0", True), ("v0.35.0", "v1.0.0", True),
])
def test_salto_es_mayor(a, n, mayor):
    assert bm._salto_es_mayor(a, n) is mayor


# ---------------------------------------------------------------- pasadas

@pytest.fixture
def comandos(monkeypatch):
    """Captura todo lo que el script quiere ejecutar, sin ejecutarlo."""
    corridos: list[list[str]] = []

    def falso_sh(*args, cwd=None, check=True):
        corridos.append(list(args))
        return ""

    def falso_run(args, cwd=None, capture_output=True, text=True):
        corridos.append(list(args))
        return subprocess.CompletedProcess(args, 0, "", "")

    monkeypatch.setattr(bm, "_sh", falso_sh)
    monkeypatch.setattr(bm.subprocess, "run", falso_run)
    return corridos


def _escenario(monkeypatch, prs):
    monkeypatch.setattr(bm, "_prs_abiertos", lambda repo_dir: prs)


def test_cierra_el_superado_y_mergea_el_ultimo_en_verde(monkeypatch, comandos):
    _escenario(monkeypatch, [
        _pr(162, "chore/bump-libracore-v1.80.0"),
        _pr(163, "chore/bump-libracore-v1.83.0"),
    ])
    pines = {"libracore": [{"ver": "v1.75.0"}]}
    cerrados, mergeados = bm.superar_y_mergear(".", pines, {"libracore": "v1.83.0"}, dry_run=False)
    assert (cerrados, mergeados) == (1, 1)
    assert ["gh", "pr", "close", "162"] == comandos[0][:4]
    assert "--delete-branch" in comandos[0]
    assert ["gh", "pr", "merge", "163", "--squash", "--delete-branch"] == comandos[1]


def test_en_dry_run_no_corre_nada(monkeypatch, comandos):
    _escenario(monkeypatch, [
        _pr(162, "chore/bump-libracore-v1.80.0"),
        _pr(163, "chore/bump-libracore-v1.83.0"),
    ])
    cerrados, mergeados = bm.superar_y_mergear(
        ".", {"libracore": [{"ver": "v1.75.0"}]}, {"libracore": "v1.83.0"}, dry_run=True)
    assert (cerrados, mergeados) == (1, 1)
    assert comandos == []


def test_no_mergea_con_un_check_en_rojo_ni_pendiente(monkeypatch, comandos):
    _escenario(monkeypatch, [
        _pr(10, "chore/bump-libragenda-v0.10.0", checks=("SUCCESS", "FAILURE")),
        _pr(11, "chore/bump-libra-ui-v0.59.0", checks=("SUCCESS", "PENDING")),
    ])
    pines = {"libragenda": [{"ver": "v0.9.1"}], "libra-ui": [{"ver": "v0.58.0"}]}
    r = bm.superar_y_mergear(".", pines, {"libragenda": "v0.10.0", "libra-ui": "v0.59.0"}, dry_run=False)
    assert r == (0, 0)
    assert comandos == []


def test_un_salto_de_mayor_queda_abierto_aunque_este_verde(monkeypatch, comandos):
    _escenario(monkeypatch, [_pr(5, "chore/bump-libraauth-v1.0.0")])
    r = bm.superar_y_mergear(".", {"libraauth": [{"ver": "v0.35.0"}]}, {"libraauth": "v1.0.0"}, dry_run=False)
    assert r == (0, 0)
    assert comandos == []


def test_un_bump_a_una_version_que_ya_no_es_la_ultima_no_se_mergea(monkeypatch, comandos):
    # el viejo se cierra (pasada 2); aunque estuviera verde no entra en la 3
    _escenario(monkeypatch, [_pr(7, "chore/bump-libracore-v1.80.0")])
    r = bm.superar_y_mergear(".", {"libracore": [{"ver": "v1.75.0"}]}, {"libracore": "v1.83.0"}, dry_run=False)
    assert r == (1, 0)
    assert comandos[0][:3] == ["gh", "pr", "close"]


def test_sin_mergeable_no_se_toca(monkeypatch, comandos):
    _escenario(monkeypatch, [_pr(8, "chore/bump-libracore-v1.83.0", mergeable="UNKNOWN")])
    r = bm.superar_y_mergear(".", {"libracore": [{"ver": "v1.80.0"}]}, {"libracore": "v1.83.0"}, dry_run=False)
    assert r == (0, 0)
    assert comandos == []


def test_no_mergear_apaga_solo_la_pasada_3(monkeypatch, comandos):
    _escenario(monkeypatch, [
        _pr(1, "chore/bump-libracore-v1.80.0"), _pr(2, "chore/bump-libracore-v1.83.0")])
    r = bm.superar_y_mergear(".", {"libracore": [{"ver": "v1.75.0"}]}, {"libracore": "v1.83.0"},
                             dry_run=False, mergear=False)
    assert r == (1, 0)
    assert [c[:3] for c in comandos] == [["gh", "pr", "close"]]


def test_dependabot_actions_en_verde_se_mergea_y_npm_no(monkeypatch, comandos):
    _escenario(monkeypatch, [
        _pr(20, "dependabot/github_actions/actions-abc"),
        _pr(21, "dependabot/npm_and_yarn/frontend/npm-def"),
        _pr(22, "dependabot/github_actions/actions-xyz", checks=("FAILURE",)),
    ])
    r = bm.superar_y_mergear(".", {}, {}, dry_run=False)
    assert r == (0, 1)
    assert comandos == [["gh", "pr", "merge", "20", "--squash", "--delete-branch"]]


def test_un_merge_que_falla_no_cuenta(monkeypatch, comandos):
    _escenario(monkeypatch, [_pr(9, "chore/bump-libracore-v1.83.0")])

    def run_fallido(args, cwd=None, capture_output=True, text=True):
        return subprocess.CompletedProcess(args, 1, "", "Pull request is not mergeable")

    monkeypatch.setattr(bm.subprocess, "run", run_fallido)
    r = bm.superar_y_mergear(".", {"libracore": [{"ver": "v1.80.0"}]}, {"libracore": "v1.83.0"}, dry_run=False)
    assert r == (0, 0)


# ---------------------------------------------------------------- uv.lock (F1)

def test_sin_uv_lock_no_regenera_nada(tmp_path, comandos):
    assert bm._refrescar_lock_py(str(tmp_path)) is None
    assert comandos == []


def test_con_uv_lock_corre_uv_lock_y_lo_devuelve_para_commitear(tmp_path, comandos):
    (tmp_path / "uv.lock").write_text("version = 1")
    assert bm._refrescar_lock_py(str(tmp_path)) == "uv.lock"
    assert comandos == [["uv", "lock"]]


# ------------------------------------------------- pasada 1: aislar el fallo


def _procesar_con(monkeypatch, pines, ultimos, rotos=()):
    """Corre la pasada 1 sin red. `rotos` son los motores cuyo `_abrir_bump`
    revienta, que es como se comporta `npm install` cuando un peer no resuelve.
    Devuelve (resultado, motores efectivamente intentados)."""
    intentados: list[str] = []

    def falso_abrir(repo_dir, repo, usos, actual, ultimo, rama, base):
        intentados.append(repo)
        if repo in rotos:
            raise RuntimeError(f"npm install {repo} -> 1\nERESOLVE")

    monkeypatch.setattr(bm, "_pines", lambda repo_dir: pines)
    monkeypatch.setattr(bm, "_ultimo_tag", lambda repo: ultimos[repo])
    monkeypatch.setattr(bm, "_rama_o_pr_existe", lambda repo_dir, rama: False)
    monkeypatch.setattr(bm, "_abrir_bump", falso_abrir)
    monkeypatch.setattr(bm, "superar_y_mergear",
                        lambda *a, **k: (0, 0))
    return bm.procesar(".", dry_run=False), intentados


_PINES_DE_UN_BACKOFFICE = {
    # El orden del dict no importa: `procesar` los recorre ordenados, y asi
    # `libra-ui` cae ANTES que los dos de Python. Es el caso real.
    "libra-ui": [{"ver": "v0.59.0", "archivo": "frontend/package.json", "tipo": "js"}],
    "libraauth": [{"ver": "v0.36.0", "archivo": "backend/pyproject.toml", "tipo": "py"}],
    "libracore": [{"ver": "v1.77.0", "archivo": "backend/pyproject.toml", "tipo": "py"}],
}
_ULTIMOS = {"libra-ui": "v0.65.0", "libraauth": "v0.37.0", "libracore": "v1.89.0"}


def test_un_motor_que_no_se_puede_bumpear_no_tapa_a_los_otros(monkeypatch, comandos):
    """El caso que dejo a libra-panel y libra-backoffice ocho versiones atras."""
    (hechos, fallidos), intentados = _procesar_con(
        monkeypatch, _PINES_DE_UN_BACKOFFICE, _ULTIMOS, rotos={"libra-ui"})
    # Los tres se intentaron, aunque el primero de la lista se rompiera.
    assert intentados == ["libra-ui", "libraauth", "libracore"]
    assert hechos == 2
    assert fallidos == ["libra-ui"]


def test_el_fallo_de_un_motor_sale_en_rojo_igual(monkeypatch, comandos):
    """Aislar el fallo es para que los demas avancen, no para esconderlo."""
    monkeypatch.setattr(bm, "_pines", lambda repo_dir: _PINES_DE_UN_BACKOFFICE)
    monkeypatch.setattr(bm, "_ultimo_tag", lambda repo: _ULTIMOS[repo])
    monkeypatch.setattr(bm, "_rama_o_pr_existe", lambda repo_dir, rama: False)
    monkeypatch.setattr(bm, "superar_y_mergear", lambda *a, **k: (0, 0))

    def falso_abrir(repo_dir, repo, usos, actual, ultimo, rama, base):
        if repo == "libra-ui":
            raise RuntimeError("ERESOLVE")

    monkeypatch.setattr(bm, "_abrir_bump", falso_abrir)
    monkeypatch.setattr(bm.sys, "argv", ["bump_motores.py", "--apply"])
    assert bm.main() == 1

    # Control: sin ningun motor roto, el mismo camino sale en verde. Sin esto,
    # un `return 1` incondicional pasaria el assert de arriba.
    monkeypatch.setattr(bm, "_abrir_bump", lambda *a, **k: None)
    assert bm.main() == 0


def test_cada_bump_parte_del_commit_base_y_no_del_anterior(monkeypatch, comandos):
    """Si el segundo bump saliera de la rama del primero, su PR se llevaria
    adentro el cambio del primero y dejaria de ser revisable por separado."""
    monkeypatch.setattr(bm, "_pines", lambda repo_dir: _PINES_DE_UN_BACKOFFICE)
    monkeypatch.setattr(bm, "_ultimo_tag", lambda repo: _ULTIMOS[repo])
    monkeypatch.setattr(bm, "_rama_o_pr_existe", lambda repo_dir, rama: False)
    monkeypatch.setattr(bm, "superar_y_mergear", lambda *a, **k: (0, 0))
    monkeypatch.setattr(bm, "_cambiar_pin", lambda *a, **k: None)
    monkeypatch.setattr(bm, "_refrescar_lock", lambda *a, **k: None)
    monkeypatch.setattr(bm, "_refrescar_lock_py", lambda *a, **k: None)
    bm.procesar(".", dry_run=False)

    base = next(c for c in comandos if c[:3] == ["git", "rev-parse", "HEAD"])
    assert base  # se pidio el commit base una vez, al arrancar
    checkouts = [c for c in comandos if c[:3] == ["git", "checkout", "-B"]]
    assert len(checkouts) == 3
    # El cuarto argumento es el punto de partida, y es el MISMO en los tres.
    puntos = {c[4] for c in checkouts}
    assert len(puntos) == 1, f"cada bump partio de otro lado: {puntos}"
