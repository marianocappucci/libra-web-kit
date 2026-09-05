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
