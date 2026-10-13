# Action `e2e-ci`: tests de navegador de los productos Libra

Levanta un producto entero en el runner y corre Playwright (Chromium) contra él. Es el armado que el smoke de navegador copiaba en
los ocho productos (120 líneas de workflow cada uno), más lo que piden los tests de dominio: semilla, un usuario por rol, caché de
Chromium y un resumen que **no deja pasar un flake en silencio**.

```yaml
- uses: actions/checkout@v7
- name: Acceso SSH a los motores privados      # el del producto: sus deploy keys, sus motores
  run: …
- uses: marianocappucci/libra-web-kit/.github/actions/e2e-ci@e2e-ci-v1
  with:
    variante: debian
    base: ventalibra
    usuario: ventalibra
    clave: ventalibra-ci
    proyecto: e2e
    nocturno: ${{ github.event_name == 'schedule' }}
    env: |
      ENV=development
      DATA_DIR=${{ github.workspace }}/e2e-data
      VENTALIBRA_DATABASE_URL=postgresql+psycopg://ventalibra:ventalibra-ci@localhost:5432/ventalibra
      E2E_ADMIN_USUARIO=admin
      E2E_ADMIN_CLAVE=…
    semilla: |
      python -m scripts.e2e_usuarios terminos
      python -m scripts.seed_demo --url "$E2E_BASE_URL" --usuario "$E2E_ADMIN_USUARIO" --password "$E2E_ADMIN_CLAVE"
    usuarios-por-rol: python -m scripts.e2e_usuarios usuarios
```

Ejemplo completo y vivo: `ventalibra/.github/workflows/e2e.yml` (tests de dominio) y `smoke-navegador.yml` (sólo `proyecto: smoke`).

## Qué hace, en orden

1. **PostgreSQL** con [`postgres-ci`](../postgres-ci/action.yml) (`@postgres-ci-v1`: espejo de ECR con reintentos y espejos de respaldo). **Sin docker compose**:
   Docker Hub tiene tope de descargas anónimas y ya trabó el CI de toda la familia (`reglas/ci.md`).
2. **Variables de entorno** (`env`) a `GITHUB_ENV`, más `TZ`, `E2E_BASE_URL` y, de noche, `NOCTURNO=1`.
3. Python + **uv** y `uv sync` desde el lock; Node, `npm ci` y `npm run build` del frontend.
4. **Migraciones: las que declara `scripts/panel_admin.py`**, en su orden (el camino real del deploy), y **uvicorn** sirviendo `frontend/dist`, esperando `/health`.
5. **`semilla`** y **`usuarios-por-rol`** (comandos del producto, desde la raíz del repo y con el venv en el PATH).
6. **Chromium**, cacheado en `~/.cache/ms-playwright` por la versión de `@playwright/test`, e `install-deps` (las librerías del sistema no se cachean).
7. **`playwright test`** con `--project=<proyecto>` (y `--repeat-each`, `<spec>` si se piden).
8. **Resumen**: `resumen.mjs` lee `test-results/resultado.json` (lo escribe `libra-ui/e2e`) y deja el cuadro en el resumen del job, un `::warning` por cada **flake** (pasó recién al reintento de la corrida de noche) y los outputs `flaky` y `fallos`.
9. **Artifacts si algo falla o hubo un flake**: trace, screenshots, reporte HTML y `uvicorn.log`.

## Inputs

| Input | Obligatorio | Defecto | |
|---|---|---|---|
| `variante` | sí | | PostgreSQL `debian` o `alpine` (como `postgres-ci`) |
| `base`, `usuario`, `clave` | sí | | `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` |
| `tz` | | `America/Argentina/Buenos_Aires` | TZ del contenedor y del job |
| `modulo-app` | | `app.asgi:app` | módulo ASGI de uvicorn |
| `puerto` | | `8000` | puerto de la app; los tests usan `http://localhost:<puerto>` |
| `env` | | | `CLAVE=valor` por línea; la app y los tests las ven |
| `semilla` | | | comando(s) de shell que siembran la instancia |
| `usuarios-por-rol` | | | comando(s) de shell que crean un usuario por rol |
| `proyecto` | | `e2e` | `--project`: `smoke`, `e2e` o `smoke,e2e` (`setup` entra solo) |
| `spec` | | | archivo o patrón para acotar la corrida |
| `repetir` | | | `--repeat-each` (medir flakes de un spec nuevo) |
| `nocturno` | | `false` | `true` exporta `NOCTURNO=1`: `libra-ui/e2e` reintenta una vez y la Action avisa cada flake |
| `directorio-frontend` | | `frontend` | |
| `python-version`, `uv-version`, `uv-sync`, `node-version` | | `3.12`, `0.12.10`, `--locked`, `22` | |
| `espera-app` | | `60` | segundos de espera a `/health` |
| `artefactos` | | `e2e-playwright` | nombre del artifact |

Outputs: `flaky`, `fallos`.

## Lo que tiene que haber antes (y lo que trae el producto)

- `actions/checkout` y el **acceso SSH a los repos privados** (`libracore`, `libracommerce`, `libraauth`, `libra-ui`…): son secrets del repo y la lista de
  motores es de cada producto. Una Action compuesta no ve los secrets si no se los pasan, y pasar una deploy key multilínea por un input es más frágil que
  repetir el paso. (Si se repite en los ocho, la salida es una Action `ssh-privadas` aparte.)
- `scripts/panel_admin.py` con las migraciones, `frontend/` con `@playwright/test` y `libra-ui` (que trae `libra-ui/e2e`, ≥ la versión que lo publicó) y `/health`.
- Los tests: `frontend/playwright.config.ts` con `definirConfig()` de `libra-ui/e2e`, `e2e/auth.setup.ts` y los specs `*.e2e.ts` / `*.smoke.ts`.

## Por qué los pasos son así

- **Una Action compuesta y no un workflow reutilizable**: el job de cada producto es distinto (SSH, secrets, condiciones sobre el PR). Se versiona con un tag
  mayor móvil (`e2e-ci-v1`, que se mueve en cada versión compatible; un cambio incompatible es `e2e-ci-v2`) y uno exacto al lado.
- **`localhost` y no `127.0.0.1`**: la cookie de sesión de libraauth es `Secure` y Chromium sólo trata a `localhost` como contexto seguro sobre http.
- **Los Términos**: una instancia nueva los trae pendientes y el motor corta con 403 toda llamada gateada por rol. El smoke los atraviesa por la pantalla; los
  tests de dominio los aceptan por la API antes de sembrar.
- **Sin `waitForTimeout` ni `networkidle`** en los specs: se espera el hecho.

## Qué prueba este repo de la Action

`.github/workflows/accion-e2e-ci.yml`: que el YAML es compuesto y que `resumen.mjs` cuenta un reporte con un flake, un fallo y un salteado
(`prueba/resultado.json`). El armado completo se prueba en el producto piloto, que es quien tiene los motores privados.
