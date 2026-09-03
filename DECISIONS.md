# Decisiones arquitectónicas — libra-web-kit

Registro ADR. Las decisiones no se borran; si dejan de aplicar, se marcan como
reemplazadas. Fechas y motivos salen del código y de la historia registrada en el
wiki (entidades `libra-web-kit` y `libra-bump`).

## ADR-001 — Un kit compartido para las landings, tras auditoría de duplicación

- Estado: aceptada
- Fecha: 2026-07-26
- Contexto: las landings de marketing (`contalibra_web`, `restolibra_web`, …)
  tenían copias divergentes del login de `/docs/`, del CSS, de las páginas legales
  y de la imagen nginx.
- Decisión: extraer un kit compartido (`libra-web-kit`) con esas piezas; los
  consumidores son los repos `*_web`, no los productos verticales.
- Consecuencias: un arreglo se hace en un lugar y alcanza a todas las landings;
  el kit no aparece importado en el código de los productos porque no es suyo.

## ADR-002 — Login de `/docs/` compartido y parametrizable por tema

- Estado: aceptada
- Fecha: 2026-07-26
- Contexto: todas las landings gatean su documentación con el mismo mecanismo pero
  distinta marca.
- Decisión: `docs_auth.build_docs_login_app` construye el backend de login, con
  `DocsLoginTheme` para el aspecto por landing.
- Consecuencias: una sola implementación del gate; cada landing sólo aporta su
  tema.

## ADR-003 — Generación de CSS/docs/legales desde tokens, no a mano por sitio

- Estado: aceptada
- Fecha: 2026-07-26
- Contexto: mantener estilos, sidebars de docs y páginas legales copiados por
  landing garantiza que diverjan.
- Decisión: `css_gen`/`site_css_tokens`, `docs_gen`/`docs_pages`/`docs_sidebars` y
  `legal_gen` generan esas piezas desde una fuente común.
- Consecuencias: las landings no divergen en lo compartido; un cambio de estilo o
  de texto legal se propaga por regeneración.

## ADR-004 — La automatización de bump de motores vive en un solo lugar

- Estado: aceptada
- Fecha: 2026-09
- Contexto: actualizar el pin de un motor era "un worktree por producto a mano";
  al bumpear a mano aparecía el pozo del `package-lock.json` que no se movía solo.
- Decisión: `bump_motores.py`, corrido en el repo del consumidor, abre un PR por
  cada motor con tag más nuevo que el pin; entiende los dos formatos de pin de la
  familia (`pyproject.toml` y `package.json`), y para el segundo re-resuelve el
  lock con `npm install`. Vive en libra-web-kit, disparado por el reusable
  workflow `bump-motores.yml` (cron diario + botón manual).
- Consecuencias: un arreglo al bumpeo se propaga a los diez consumidores sin
  tocar sus repos.

## ADR-005 — El bump usa una GitHub App, no un PAT

- Estado: aceptada
- Fecha: 2026-09
- Contexto: un PR abierto por `GITHUB_TOKEN` **no** dispara el CI del consumidor
  (anti-loop de GitHub Actions), así que el bump quedaría sin verificar; y un PAT
  compartido vence y, al compartirse, tumba el CI de todos a la vez.
- Decisión: usar la GitHub App `libra-bump` (`create-github-app-token`) para abrir
  los PRs con una identidad que **sí** dispara el CI; si el secreto de la App
  falta, degradar a `::warning::` en vez de fallar.
- Consecuencias: el PR de bump se verifica solo; se evita el PAT. Ver la entidad
  `libra-bump` del wiki.

## ADR-006 — La imagen nginx común también vive en el kit

- Estado: aceptada
- Fecha: 2026-07
- Contexto: las landings comparten el proxy nginx y su despliegue; duplicarlo por
  sitio es la misma trampa que el CSS.
- Decisión: mantener la imagen nginx (`nginx/`) y sus workflows
  (`publish-nginx-image.yml`, `deploy-vps.yml`) en el kit.
- Consecuencias: una sola imagen y un solo pipeline de publicación/deploy para las
  landings.
