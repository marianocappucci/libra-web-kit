# Arquitectura — libra-web-kit

## Propósito y límites

libra-web-kit es el **kit web compartido** de la familia Libra: la
infraestructura común de las *landings* de marketing (`contalibra_web`,
`restolibra_web`, `gestiolibra_web`, `medlibra_web`, `ventalibra_web` y las que
sigan) y la automatización transversal que no pertenece a ningún producto. Se
extrajo el 2026-07-26 tras una auditoría de duplicación entre las landings.

A diferencia de los otros motores, **sus consumidores no son los ocho productos
verticales** —de ahí que no aparezca importado en su código— sino los repos
`*_web` de las landings, más el CI de los diez repos que consumen motores. Reúne
cuatro cosas que comparten esos repos: el login gateado de `/docs/`, la
generación de CSS/docs/legales, la imagen nginx común y el bumpeo automático de
motores.

## Componentes

### Paquete `libra_web_kit/` — generación y login de las landings

- **`docs_auth.py`** (`build_docs_login_app`, `DocsLoginTheme`): el backend de
  login que **gatea `/docs/`** en cada landing. Una sola implementación para
  todas: cada landing la monta con su tema.
- **`css_gen.py`** (`render`, `render_all`) + **`site_css_tokens.py`**:
  generación del CSS compartido a partir de tokens, para que las landings no
  diverjan en estilos.
- **`docs_gen.py`** (`list_pages`, `render`, `render_all`), **`docs_pages.py`**,
  **`docs_sidebars.py`**: generación del sitio de documentación.
- **`legal_gen.py`** (`render`, `markdown_publicado`, `render_all`, `sitios`):
  generación de las páginas legales (términos, privacidad) publicadas por sitio.

### `bump_motores.py` + `.github/workflows/bump-motores.yml` — bumpeo de motores

La automatización transversal más importante del kit. `bump_motores.py`, corrido
**en el repo del consumidor**, abre un PR por cada motor de la familia cuyo tag
publicado sea más nuevo que el pin actual. Entiende los dos formatos de pin de la
familia:

- `pyproject.toml`: `"<motor>[extras] @ git+https://github.com/OWNER/<repo>.git@vX.Y.Z"`
- `package.json`: `"<motor>": "github:OWNER/<repo>#vX.Y.Z"` — y además
  re-resuelve el `package-lock.json` con `npm install`, porque el lock guarda el
  SHA del tag y no se mueve solo (el pozo conocido: el lock decía la versión
  nueva y `node_modules` seguía en la vieja).

Vive en un solo lugar a propósito: un arreglo al bumpeo se propaga a los diez
consumidores sin tocar sus repos. El reusable workflow `bump-motores.yml`
(`workflow_call`, cron diario + botón manual) lo dispara usando la GitHub App
`libra-bump` para abrir los PRs con una identidad que **sí** dispara el CI del
consumidor (un PR abierto por `GITHUB_TOKEN` no lo haría); si el secreto de la
App falta, degrada a un `::warning::` en vez de fallar. Ver la entidad `libra-bump`
del wiki.

### Imagen nginx compartida — `nginx/`, `publish-nginx-image.yml`

La imagen nginx común de las landings, publicada por su propio workflow
(`publish-nginx-image.yml`), y el `deploy-vps.yml` de despliegue. Es la otra
pieza de infraestructura que las landings no deben duplicar.

## Diseño: un solo lugar para lo compartido

El principio del kit es el mismo que motivó su extracción: **lo que comparten N
landings vive una vez.** El login de `/docs/`, el CSS, las páginas legales y la
imagen nginx eran copias divergentes antes de julio de 2026; el bumpeo de motores
era un worktree a mano por producto. Todo eso se centralizó acá, de modo que un
arreglo se hace en un lugar y alcanza a todos los consumidores.

## Distribución

Paquete `libra_web_kit` (build `hatchling`), versión pineada al tag (`v0.3.0` al
2026-09), consumido por las landings; el `bump_motores.py` y los workflows se
consumen como reusable workflow / script, no como import.

## Referencias

- `README.md` — origen de la extracción y lista de landings consumidoras.
- Wiki: entidades `libra-web-kit` y `libra-bump`, y la auditoría
  `auditoria-estructural-familia-libra-2026-09`.
