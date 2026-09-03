"""
Backend de acceso a `/docs/` para las landings de la familia Libra.
Extraído 2026-07-26 de `auth/app.py` de Contalibra/Restolibra/Gestiolibra/
MedLibra/VentaLibra, donde era >85% idéntico salvo branding (colores,
nombre, placeholder del subdominio), el endpoint interno de verify (dos
convenciones: `/api/auth/verify` en Contalibra/Restolibra vs.
`/auth/verify` en las otras tres) y el nombre de la env var de
`SECRET_KEY` -- ver wiki/analyses/auditoria-duplicacion-familia-libra.md.

No guarda usuarios propios: cada login se valida en tiempo real contra la
instancia real del cliente (`POST https://{subdominio}.{apex_domain}
{verify_path}`), reutilizando el auth que ya existe en cada contenedor.
El usuario escribe directamente su subdominio en vez de elegirlo de un
`<select>`.

Incluye rate limiting por IP (5 intentos fallidos / 15 min, mismo patrón
que `AdminAuth` de `libracore.auth`) -- agregado el mismo día en P0 del
mismo plan de consolidación, nace incluido acá.
"""
import os
import re
import threading
import time
from dataclasses import dataclass

import httpx
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

COOKIE_NAME = "docs_session"
MAX_AGE = 86400 * 7  # 7 dias
SLUG_RE = re.compile(r"^[a-z0-9-]{1,63}$")

LOGIN_MAX_INTENTOS = 5
LOGIN_VENTANA_SEGUNDOS = 15 * 60


@dataclass(frozen=True)
class DocsLoginTheme:
    """Paleta de la pantalla de login -- únicos valores que difieren
    genuinamente por producto además del branding textual."""

    accent: str
    accent_hover: str
    bg: str = "#f8fafc"
    fg: str = "#1e293b"
    border: str = "#e2e8f0"
    muted_fg: str = "#64748b"
    muted_bg: str = "#f1f5f9"


def build_docs_login_app(
    *,
    product_name: str,
    apex_domain_default: str,
    secret_key_env: str,
    secret_key_default: str,
    verify_path: str,
    slug_placeholder: str,
    theme: DocsLoginTheme,
) -> FastAPI:
    """Construye la app FastAPI completa (login/logout/check) para el
    login gateado de `/docs/` de un producto. Cada landing la instancia
    una sola vez en su propio `auth/app.py` con sus valores de
    parametrización."""

    docs_auth_secret = os.environ.get("DOCS_AUTH_SECRET", "")
    secret_key = os.environ.get(secret_key_env, secret_key_default)
    apex_domain = os.environ.get("APEX_DOMAIN", apex_domain_default)

    signer = URLSafeTimedSerializer(secret_key)

    # Rate limiting de /login-docs en memoria del propio proceso -- mismo
    # patron que AdminAuth de libracore.auth. Alcanza porque cada landing
    # corre como un unico proceso; se resetea si el contenedor reinicia,
    # aceptable para este backend de bajo trafico.
    intentos_fallidos: dict[str, list] = {}
    intentos_lock = threading.Lock()

    def rate_limit_excedido(ip: str) -> bool:
        if not ip:
            return False
        ahora = time.time()
        with intentos_lock:
            vigentes = [t for t in intentos_fallidos.get(ip, []) if ahora - t < LOGIN_VENTANA_SEGUNDOS]
            intentos_fallidos[ip] = vigentes
            return len(vigentes) >= LOGIN_MAX_INTENTOS

    def registrar_intento_fallido(ip: str):
        if not ip:
            return
        with intentos_lock:
            intentos_fallidos.setdefault(ip, []).append(time.time())

    def render_login(error: str = "", slug: str = "", username: str = "") -> str:
        t = theme
        return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Acceso a Documentación · {product_name}</title>
<meta name="robots" content="noindex">
<style>
  body {{ font-family: 'Inter', system-ui, sans-serif; background:{t.bg}; color:{t.fg};
         display:flex; align-items:center; justify-content:center; min-height:100vh; margin:0; }}
  .card {{ background:#fff; border:1px solid {t.border}; border-radius:12px; padding:2rem;
           box-shadow:0 4px 24px rgba(0,0,0,.08); width:100%; max-width:380px; }}
  h1 {{ font-size:1.25rem; margin:0 0 1.25rem; }}
  label {{ display:block; font-size:.85rem; margin:.75rem 0 .25rem; color:{t.muted_fg}; }}
  .domain-row {{ display:flex; align-items:stretch; border:1px solid {t.border}; border-radius:8px; overflow:hidden; }}
  .domain-row input {{ border:none; flex:1; min-width:0; }}
  .domain-row span {{ background:{t.muted_bg}; color:{t.muted_fg}; padding:.6rem .6rem; font-size:.85rem;
                       white-space:nowrap; display:flex; align-items:center; }}
  input {{ width:100%; padding:.6rem .75rem; border:1px solid {t.border}; border-radius:8px;
                   font-size:1rem; box-sizing:border-box; }}
  button {{ width:100%; margin-top:1.25rem; padding:.7rem; background:{t.accent}; color:#fff;
            border:none; border-radius:8px; font-size:1rem; cursor:pointer; }}
  button:hover {{ background:{t.accent_hover}; }}
  .error {{ background:#fef2f2; color:#b91c1c; padding:.6rem .75rem; border-radius:8px;
            font-size:.85rem; margin-bottom:1rem; }}
  a {{ color:{t.accent}; text-decoration:none; font-size:.85rem; }}
</style>
</head>
<body>
  <div class="card">
    <h1>Documentación del sistema</h1>
    {'<div class="error">' + error + '</div>' if error else ''}
    <form method="post" action="/login-docs">
      <label for="slug">Tu subdominio</label>
      <div class="domain-row">
        <input type="text" name="slug" id="slug" required autocomplete="off"
               placeholder="{slug_placeholder}" value="{slug}">
        <span>.{apex_domain}</span>
      </div>
      <label for="username">Usuario</label>
      <input type="text" name="username" id="username" required autocomplete="username" value="{username}">
      <label for="password">Contraseña</label>
      <input type="password" name="password" id="password" required autocomplete="current-password">
      <button type="submit">Ingresar</button>
    </form>
    <p style="margin-top:1rem"><a href="/">&larr; Volver al sitio</a></p>
  </div>
</body>
</html>"""

    app = FastAPI(title=f"{product_name} Docs Auth", docs_url=None, redoc_url=None)

    @app.get("/login-docs", response_class=HTMLResponse)
    async def login_form():
        return render_login()

    @app.post("/login-docs", response_class=HTMLResponse)
    async def login_submit(request: Request, slug: str = Form(...), username: str = Form(...), password: str = Form(...)):
        slug = slug.strip().lower()
        if not SLUG_RE.match(slug):
            return HTMLResponse(render_login("Subdominio inválido.", slug, username), status_code=400)

        ip = request.client.host if request.client else ""
        if rate_limit_excedido(ip):
            return HTMLResponse(
                render_login("Demasiados intentos fallidos. Esperá unos minutos y volvé a intentar.", slug, username),
                status_code=429,
            )

        domain = f"{slug}.{apex_domain}"
        try:
            async with httpx.AsyncClient(timeout=8) as client:
                r = await client.post(
                    f"https://{domain}{verify_path}",
                    headers={"X-Internal-Auth": docs_auth_secret},
                    json={"username": username, "password": password},
                )
            data = r.json() if r.status_code == 200 else {"valid": False}
        except httpx.HTTPError:
            return HTMLResponse(
                render_login("No se pudo contactar a tu instancia. Revisá el subdominio e intentá de nuevo.", slug, username),
                status_code=502,
            )

        if not data.get("valid"):
            registrar_intento_fallido(ip)
            return HTMLResponse(render_login("Subdominio, usuario o contraseña incorrectos.", slug, username), status_code=401)

        token = signer.dumps({"slug": slug, "username": username})
        resp = RedirectResponse("/docs/", status_code=303)
        resp.set_cookie(COOKIE_NAME, token, httponly=True, samesite="lax", max_age=MAX_AGE)
        return resp

    @app.get("/logout-docs")
    async def logout():
        resp = RedirectResponse("/login-docs", status_code=303)
        resp.delete_cookie(COOKIE_NAME)
        return resp

    @app.get("/check", include_in_schema=False)
    async def check(request: Request):
        """Endpoint interno para el auth_request de nginx: 200 si la cookie es válida, 401 si no."""
        token = request.cookies.get(COOKIE_NAME)
        if not token:
            return Response(status_code=401)
        try:
            signer.loads(token, max_age=MAX_AGE)
        except (BadSignature, SignatureExpired):
            return Response(status_code=401)
        return Response(status_code=200)

    return app
