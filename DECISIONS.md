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

## ADR-007 — El bloqueo de `/login-docs` cuenta por la IP del cliente, no por la del proxy

- Estado: aceptada
- Fecha: 2026-09-12
- Contexto: la cadena es cliente → NPM → nginx de la landing → `docs_auth`.
  `docs_auth` contaba los fallidos por `request.client.host`, que es siempre el
  nginx de la landing, y el `limit_req` del nginx contaba por `$remote_addr`, que
  es siempre NPM. Los dos bloqueos eran globales: cinco fallos de cualquiera
  dejaban a todos afuera de `/docs/` durante 15 minutos, y el `limit_req` daba 5
  pedidos por minuto entre todos los usuarios. Además, los puertos de las landings
  están publicados en el host, así que se puede llegar al nginx sin pasar por NPM.
- Decisión:
  - `docs_auth.ip_del_request` aplica la regla del ADR-013 de libraauth: recorre
    `X-Forwarded-For` desde la derecha salteando las redes de Docker y loopback, y
    lo lee sólo si el par directo es una de ellas.
  - Es una **copia**, no un import: libraauth les arrastraría SQLAlchemy a las
    landings. Un test la corre junto a la de libraauth (que está en el extra
    `dev`) contra los mismos casos, así que no puede divergir en silencio.
  - Usa la misma variable de entorno para agregar un salto,
    `LIBRAAUTH_PROXIES_DE_CONFIANZA`.
  - La plantilla nginx usa `real_ip` con las mismas redes, así que `limit_req`
    cuenta por cliente, y en `/login-docs` agrega su salto con
    `$proxy_add_x_forwarded_for`. Quien entra por el puerto publicado queda con su
    IP real a la derecha, en vez de elegirla.
- Consecuencias: los dos bloqueos pasan a ser por cliente. Detrás de un proxy que
  no esté en la lista (un CDN delante de NPM), todos los clientes volverían a
  verse con la misma IP; el salto se declara en `LIBRAAUTH_PROXIES_DE_CONFIANZA`
  y en el `set_real_ip_from` de la plantilla. Llega a las landings recién cuando
  suben el pin del paquete y el tag de la imagen `libra-nginx-web`.
