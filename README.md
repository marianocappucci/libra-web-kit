# libra-web-kit

Backend de login gateado de `/docs/` compartido por las landings de la
familia Libra: [Contalibra](https://github.com/marianocappucci/contalibra_web),
[Restolibra](https://github.com/marianocappucci/restolibra_web),
[Gestiolibra](https://github.com/marianocappucci/gestiolibra_web),
[MedLibra](https://github.com/marianocappucci/medlibra_web) y
[VentaLibra](https://github.com/marianocappucci/ventalibra_web).

Extraído el 2026-07-26 tras confirmar en una auditoría de duplicación que
`auth/app.py` era >85% idéntico entre las cinco landings, salvo branding
(colores, nombre de producto, placeholder del subdominio), el endpoint
interno de verify (dos convenciones: `/api/auth/verify` en
Contalibra/Restolibra, `/auth/verify` en las otras tres) y el nombre de
la env var de `SECRET_KEY`. Ver
`wiki/analyses/auditoria-duplicacion-familia-libra.md` en el repo de la
wiki para el detalle completo del audit y el plan (P3).

## Uso

```python
# auth/app.py de cada landing
from libra_web_kit.docs_auth import build_docs_login_app, DocsLoginTheme

app = build_docs_login_app(
    product_name="Gestiolibra",
    apex_domain_default="gestiolibra.com.ar",
    secret_key_env="DOCS_SESSION_SECRET",
    secret_key_default="gestiolibra-docs-secret-change-me",
    verify_path="/auth/verify",
    slug_placeholder="tu-negocio",
    theme=DocsLoginTheme(accent="#7c3aed", accent_hover="#6d28d9"),
)
```

## Cómo se distribuye

Igual que libracore/libragenda/libracommerce/libraedge/libra-ui: repo
privado, instalado por cada consumidor como dependencia git pineada a un
tag exacto (nunca un rango), nunca publicado a un registro.

En `auth/requirements.txt` de cada consumidor:

```
libra-web-kit @ git+https://github.com/marianocappucci/libra-web-kit.git@v0.1.0
```

`git+https://` para que funcione también en desarrollo local sin
identidad SSH propia contra GitHub. El build en el VPS reescribe la URL a
`git+ssh://` vía un alias de `Host` dedicado + deploy key de solo
lectura, mismo patrón que los demás paquetes Python de la familia.

## Qué incluye

- `libra_web_kit.docs_auth.build_docs_login_app(...)`: construye la app
  FastAPI completa (`GET`/`POST /login-docs`, `GET /logout-docs`,
  `GET /check` para `auth_request` de nginx).
- `libra_web_kit.docs_auth.DocsLoginTheme`: paleta de colores de la
  pantalla de login (los únicos valores visuales que difieren realmente
  entre productos, además del texto de branding).
- Rate limiting por IP incluido (5 intentos fallidos / 15 min, mismo
  patrón que `AdminAuth` de `libracore.auth`) — agregado el mismo día en
  P0 del mismo plan de consolidación.

## Qué NO incluye

`nginx.conf`, `docker-compose.yml` y el CI workflow de cada landing
siguen siendo archivos propios de cada repo (son infraestructura, no
código runtime instalable) — quedan fuera del alcance de este paquete.
