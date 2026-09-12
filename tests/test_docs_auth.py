"""Tests para libra_web_kit.docs_auth.build_docs_login_app -- extraído
2026-07-26 de las 5 landings de la familia Libra, donde `auth/app.py` era
>85% idéntico. Ver wiki/analyses/auditoria-duplicacion-familia-libra.md."""
import httpx
import pytest
from fastapi.testclient import TestClient

from libra_web_kit.docs_auth import DocsLoginTheme, build_docs_login_app


@pytest.fixture(autouse=True)
def _default_secret_key(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "autoused-test-secret")


def _make_app(**overrides):
    kwargs = dict(
        product_name="Acme",
        apex_domain_default="acme.com.ar",
        secret_key_env="SECRET_KEY",
        secret_key_default="acme-docs-secret-change-me",
        verify_path="/api/auth/verify",
        slug_placeholder="tu-empresa",
        theme=DocsLoginTheme(accent="#2563eb", accent_hover="#1d4ed8"),
    )
    kwargs.update(overrides)
    return build_docs_login_app(**kwargs)


def _client(app):
    return TestClient(app, base_url="https://testserver")


def _mock_upstream(monkeypatch, handler):
    """Reemplaza el httpx.AsyncClient interno (la llamada server-to-server
    a /auth/verify de la instancia real) por uno con MockTransport --
    distinto del transport del TestClient, que habla con la app FastAPI
    en sí."""
    real_async_client = httpx.AsyncClient

    def fake_async_client(*args, **kwargs):
        kwargs["transport"] = httpx.MockTransport(handler)
        return real_async_client(*args, **kwargs)

    monkeypatch.setattr("libra_web_kit.docs_auth.httpx.AsyncClient", fake_async_client)


# ── Render / branding ───────────────────────────────────────────────────

def test_login_form_renders_product_branding():
    client = _client(_make_app())
    r = client.get("/login-docs")
    assert r.status_code == 200
    assert "Acme" in r.text
    assert "tu-empresa" in r.text
    assert "#2563eb" in r.text
    assert ".acme.com.ar" in r.text


def test_login_form_uses_theme_colors_not_hardcoded():
    theme = DocsLoginTheme(accent="#7c3aed", accent_hover="#6d28d9", bg="#fbf9f6")
    client = _client(_make_app(theme=theme))
    r = client.get("/login-docs")
    assert "#7c3aed" in r.text
    assert "#6d28d9" in r.text
    assert "#fbf9f6" in r.text


def test_invalid_slug_returns_400():
    client = _client(_make_app())
    r = client.post("/login-docs", data={"slug": "Not Valid!", "username": "u", "password": "p"})
    assert r.status_code == 400
    assert "inválido" in r.text.lower()


# ── Login submit: verify_path parametrizado ─────────────────────────────

def test_login_posts_to_configured_verify_path(monkeypatch):
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        return httpx.Response(200, json={"valid": True})

    _mock_upstream(monkeypatch, handler)
    client = _client(_make_app(verify_path="/api/auth/verify"))
    r = client.post(
        "/login-docs", data={"slug": "demo", "username": "u", "password": "p"}, follow_redirects=False,
    )
    assert r.status_code == 303
    assert captured["url"] == "https://demo.acme.com.ar/api/auth/verify"


def test_login_posts_to_alternate_verify_path(monkeypatch):
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        return httpx.Response(200, json={"valid": True})

    _mock_upstream(monkeypatch, handler)
    client = _client(_make_app(verify_path="/auth/verify"))
    r = client.post(
        "/login-docs", data={"slug": "demo", "username": "u", "password": "p"}, follow_redirects=False,
    )
    assert r.status_code == 303
    assert captured["url"] == "https://demo.acme.com.ar/auth/verify"


def test_login_success_sets_cookie_and_redirects(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"valid": True})

    _mock_upstream(monkeypatch, handler)
    client = _client(_make_app())
    r = client.post(
        "/login-docs", data={"slug": "demo", "username": "u", "password": "p"}, follow_redirects=False,
    )
    assert r.status_code == 303
    assert r.headers["location"] == "/docs/"
    assert "docs_session" in r.cookies


def test_login_invalid_credentials_returns_401(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"valid": False})

    _mock_upstream(monkeypatch, handler)
    client = _client(_make_app())
    r = client.post("/login-docs", data={"slug": "demo", "username": "u", "password": "wrong"})
    assert r.status_code == 401


def test_upstream_unreachable_returns_502(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("boom", request=request)

    _mock_upstream(monkeypatch, handler)
    client = _client(_make_app())
    r = client.post("/login-docs", data={"slug": "demo", "username": "u", "password": "p"})
    assert r.status_code == 502


def test_docs_auth_secret_header_uses_env_var(monkeypatch):
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["header"] = request.headers.get("X-Internal-Auth")
        return httpx.Response(200, json={"valid": True})

    monkeypatch.setenv("DOCS_AUTH_SECRET", "the-shared-secret")
    _mock_upstream(monkeypatch, handler)
    client = _client(_make_app())
    client.post("/login-docs", data={"slug": "demo", "username": "u", "password": "p"})
    assert captured["header"] == "the-shared-secret"


# ── Rate limiting ────────────────────────────────────────────────────────

def test_rate_limit_blocks_after_max_failed_attempts(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"valid": False})

    _mock_upstream(monkeypatch, handler)
    client = _client(_make_app())
    for _ in range(5):
        r = client.post("/login-docs", data={"slug": "demo", "username": "u", "password": "wrong"})
        assert r.status_code == 401
    r = client.post("/login-docs", data={"slug": "demo", "username": "u", "password": "wrong"})
    assert r.status_code == 429


def test_rate_limit_is_isolated_per_app_instance(monkeypatch):
    """Cada landing construye su propia app (su propio estado de rate
    limiting) -- confirma que no hay estado compartido accidental entre
    instancias."""
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"valid": False})

    _mock_upstream(monkeypatch, handler)

    client_a = _client(_make_app())
    for _ in range(5):
        client_a.post("/login-docs", data={"slug": "demo", "username": "u", "password": "wrong"})
    assert client_a.post(
        "/login-docs", data={"slug": "demo", "username": "u", "password": "wrong"},
    ).status_code == 429

    client_b = _client(_make_app())
    assert client_b.post(
        "/login-docs", data={"slug": "demo", "username": "u", "password": "wrong"},
    ).status_code == 401


# ── La IP del cliente detrás de los proxies (ADR-007) ────────────────────

#: El par directo que ve el backend en producción: el nginx de la landing, en
#: la red de Docker.
PAR_PROXY = ("172.18.0.9", 50000)


def _rechazar_todo(monkeypatch):
    _mock_upstream(monkeypatch, lambda request: httpx.Response(200, json={"valid": False}))


def _detras_del_proxy(app):
    return TestClient(app, base_url="https://testserver", client=PAR_PROXY)


def _fallar(client, xff):
    return client.post(
        "/login-docs",
        data={"slug": "demo", "username": "u", "password": "wrong"},
        headers={"X-Forwarded-For": xff},
    )


def test_un_cliente_bloqueado_no_bloquea_a_los_demas(monkeypatch):
    """🔴 El defecto: se contaba por `request.client.host`, que detrás de NPM y
    del nginx de la landing es siempre el mismo contenedor. Cinco fallos de
    cualquiera dejaban a TODOS afuera de `/docs/` durante 15 minutos."""
    _rechazar_todo(monkeypatch)
    client = _detras_del_proxy(_make_app())
    for _ in range(5):
        assert _fallar(client, "203.0.113.7").status_code == 401
    assert _fallar(client, "203.0.113.7").status_code == 429
    # Otro cliente, por el mismo proxy, sigue pudiendo intentar.
    assert _fallar(client, "198.51.100.9").status_code == 401


def test_rotar_la_izquierda_del_header_no_esquiva_el_bloqueo(monkeypatch):
    """Lo de la izquierda lo escribe el cliente; NPM agrega su par a la
    derecha. Leer desde la izquierda dejaría esquivar el bloqueo."""
    _rechazar_todo(monkeypatch)
    client = _detras_del_proxy(_make_app())
    for i in range(5):
        assert _fallar(client, f"192.0.2.{i}, 203.0.113.7").status_code == 401
    assert _fallar(client, "192.0.2.99, 203.0.113.7").status_code == 429


def test_el_salto_del_nginx_de_la_landing_se_saltea(monkeypatch):
    """Con el nginx agregando su propio salto (`$proxy_add_x_forwarded_for`),
    a la derecha queda una IP de Docker: se saltea y cuenta el cliente."""
    _rechazar_todo(monkeypatch)
    client = _detras_del_proxy(_make_app())
    for _ in range(5):
        assert _fallar(client, "203.0.113.7, 172.18.0.3").status_code == 401
    assert _fallar(client, "203.0.113.7").status_code == 429


def test_sin_pasar_por_un_proxy_el_header_no_se_cree(monkeypatch):
    """Quien llega con un par que no es de confianza no elige su IP: cuenta
    su par, cambie lo que cambie el header."""
    _rechazar_todo(monkeypatch)
    client = TestClient(_make_app(), base_url="https://testserver", client=("203.0.113.50", 1))
    for i in range(5):
        assert _fallar(client, f"198.51.100.{i}").status_code == 401
    assert _fallar(client, "198.51.100.99").status_code == 429


#: Casos para la guarda de divergencia: (par directo, X-Forwarded-For, redes
#: extra del entorno). Cubren cada rama de la regla.
CASOS_IP = [
    (PAR_PROXY, None, ""),
    (PAR_PROXY, "203.0.113.7", ""),
    (PAR_PROXY, "192.0.2.1, 203.0.113.7", ""),
    (PAR_PROXY, "203.0.113.7, 172.18.0.3", ""),
    (PAR_PROXY, "10.0.0.5, 172.18.0.3", ""),
    (PAR_PROXY, " , ", ""),
    (("203.0.113.50", 1), "198.51.100.1", ""),
    (("testclient", 1), "198.51.100.1", ""),
    (("::ffff:172.18.0.9", 1), "203.0.113.7", ""),
    (("198.51.100.200", 1), "203.0.113.7", "198.51.100.0/24"),
    (PAR_PROXY, "198.51.100.200, 203.0.113.7", "203.0.113.0/24"),
    (PAR_PROXY, "203.0.113.7", "no-es-una-red"),
    (None, "203.0.113.7", ""),
]


@pytest.mark.parametrize("cliente,xff,extra", CASOS_IP)
def test_la_copia_de_ip_del_request_da_lo_mismo_que_libraauth(monkeypatch, cliente, xff, extra):
    """🔑 `docs_auth.ip_del_request` es una copia de la de libraauth (no se
    importa para no arrastrarle SQLAlchemy a las landings). Esta guarda las
    corre a las dos contra los mismos casos: si libraauth cambia la regla, esto
    se pone rojo. El import va sin `importorskip` a propósito: si libraauth no
    está instalado, la guarda tiene que fallar, no saltearse en verde."""
    from starlette.requests import Request

    from libraauth.auth_events import ip_del_request as de_libraauth
    from libra_web_kit.docs_auth import ip_del_request as de_la_copia

    monkeypatch.setenv("LIBRAAUTH_PROXIES_DE_CONFIANZA", extra)
    headers = [] if xff is None else [(b"x-forwarded-for", xff.encode())]
    request = Request({"type": "http", "headers": headers, "client": cliente})
    assert de_la_copia(request) == de_libraauth(request)


# ── Logout / check ───────────────────────────────────────────────────────

def test_logout_clears_cookie(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"valid": True})

    _mock_upstream(monkeypatch, handler)
    client = _client(_make_app())
    client.post("/login-docs", data={"slug": "demo", "username": "u", "password": "p"})
    assert client.get("/check").status_code == 200
    client.get("/logout-docs")
    assert client.get("/check").status_code == 401


def test_check_without_cookie_returns_401():
    client = _client(_make_app())
    assert client.get("/check").status_code == 401


def test_check_with_tampered_cookie_returns_401(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"valid": True})

    _mock_upstream(monkeypatch, handler)
    client = _client(_make_app())
    client.post("/login-docs", data={"slug": "demo", "username": "u", "password": "p"})
    client.cookies.set("docs_session", client.cookies.get("docs_session") + "tampered")
    assert client.get("/check").status_code == 401


# ── SECRET_KEY env var parametrizable ────────────────────────────────────

def test_secret_key_env_var_name_is_configurable(monkeypatch):
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.setenv("DOCS_SESSION_SECRET", "custom-env-secret")

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"valid": True})

    _mock_upstream(monkeypatch, handler)
    app = _make_app(secret_key_env="DOCS_SESSION_SECRET", secret_key_default="fallback-not-used")
    client = _client(app)
    r = client.post(
        "/login-docs", data={"slug": "demo", "username": "u", "password": "p"}, follow_redirects=False,
    )
    assert r.status_code == 303
    assert "docs_session" in r.cookies
