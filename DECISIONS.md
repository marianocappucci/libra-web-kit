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

## ADR-008 — La identidad de cada producto (color + ícono) vive en el kit y la marca de la landing es el ícono

- Estado: aceptada
- Fecha: 2026-10-07
- Contexto: la marca del navbar y del pie de las landings era un cuadrado con
  `background: var(--brand)` y la **inicial** del producto; no había favicon. El
  humano decidió que cada producto tiene un color y un ícono (tabla en
  `wiki/analyses/identidad-de-producto-diseno.md`) y que el ícono blanco sobre el
  cuadrado del color reemplaza a la inicial y es el favicon.
- Decisión:
  - `identidad.IDENTIDAD` es la copia, para las landings, de esa tabla (la otra copia es
    `libra-ui/src/identidad.ts`, con el nombre del ícono de lucide). `tests/test_identidad.py`
    la hardcodea y la compara con el `--brand`, `--brand-dark` y `--brand-light` de
    `site_css_tokens.SITES`: si una copia diverge, el test falla.
  - Las páginas que el kit genera (`/docs/` y `/legal/`) toman el ícono de `IDENTIDAD`
    (`marca_icono_html`), ya no la inicial; el footer de Restolibra, que tiene el cuadrado
    inline, lleva el marcador `@@marca_icono@@`. La home de cada landing sigue siendo **a mano**:
    `scripts/generate_favicon.py --check` la mira (favicon enlazado y `.logo-icon` con el
    ícono correcto) para que un cambio de ícono no la deje atrás sin aviso.
  - `favicon_gen.favicon_svg(sitio)` produce el ícono plano (cuadrado de 64 con `rx=14`
    ~22 %, ícono blanco al 60 % y centrado) y `scripts/generate_favicon.py` lo escribe en
    `public/img/favicon.svg` de cada landing.
  - Los trazos de los ocho íconos están en `iconos_bootstrap.py`, copiados de Bootstrap
    Icons 1.11.3 (MIT, aviso en el docstring): el favicon es un SVG suelto y no puede usar la
    fuente que cargan las landings desde el CDN. Para cambiar el ícono de un producto: bajar
    la versión `npm pack bootstrap-icons@1.11.3`, copiar los `<path>` de
    `icons/<nombre>.svg` a `TRAZOS` y cambiar `icono_bootstrap` en `IDENTIDAD` y en el
    documento del wiki.
  - **Sólo SVG, sin PNG.** Rasterizar exigiría Pillow o cairosvg, que el kit no tiene y que
    las landings instalarían sin necesitarlos. Los navegadores de escritorio toman el SVG;
    queda afuera el ícono de «agregar a inicio» de iOS (`apple-touch-icon`).
- Consecuencias: el cuadrado de la marca pasa a `font-size: 1.1rem` en el navbar y `1rem` en
  el pie, porque ahora lleva un glifo y no una letra; cambian los dos `*_style.css.golden`.
  Llega a cada landing al regenerar y commitear el resultado (`generate_css.py`,
  `generate_docs.py`, `generate_legal.py`, `generate_favicon.py`) más la edición a mano de su
  `index.html`; el pin del paquete en `auth/requirements.txt` no cambia nada de eso, porque lo
  generado ya está commiteado en la landing. Versión del kit: tag `v0.5.0` (minor, módulos
  nuevos; el tag lo corta quien mergea, la versión sale de `hatch-vcs`).

## ADR-009 — La marca de la landing es el dibujo de libra-ui, copiado; reemplaza al favicon en Python de ADR-008

- Estado: aceptada
- Fecha: 2026-10-07
- Contexto: ADR-008 puso en la marca del navbar y del pie un glifo de Bootstrap Icons
  sobre un cuadrado con `background: var(--brand)` y generó el favicon dibujándolo en
  Python (`favicon_gen`, con los trazos de `iconos_bootstrap`). El mismo día libra-ui
  v0.124.0 (ADR-034) dio a cada producto una **marca dibujada propia** (dos piezas, un
  filo que las separa, detalles calados) con una variante `favicon` reducida para 16-32 px,
  y publicó los ocho dibujos como archivos (`marcas/<p>.svg`, `marcas/<p>-favicon.svg`,
  lienzo de 120) justamente para que las landings no tengan que redibujarlos.
- Decisión:
  - **ADR-008 queda reemplazado en el dibujo del favicon y de la marca**: se retiran
    `favicon_gen.py`, `iconos_bootstrap.py`, `identidad.nombre_icono` y
    `identidad.marca_icono_html`. Sigue vigente de ADR-008 lo demás: `IDENTIDAD` (los
    colores) y `tests/test_identidad.py`, que la compara con el documento del wiki y con
    `site_css_tokens.SITES`. `icono_bootstrap` queda como dato de la tabla del wiki
    (glifo de una línea), ya no es la marca.
  - Los 16 SVG viven en `libra_web_kit/marcas/`, **copiados byte a byte** (nada se edita ni
    se redibuja acá) con `scripts/sincronizar_marcas.py --tag <vX.Y.Z>`, que los lee con
    `git show <tag>:marcas/<archivo>` de un checkout de libra-ui (`--libra-ui` o
    `$LIBRA_UI_DIR`; `--desde-dir` para una rama sin tag; `--check` para verificar) y deja
    `marcas/ORIGEN.txt` con el tag, el commit y el comando. Origen actual: **libra-ui v0.124.0**
    (`e38c42e`). Al subir de versión: correr el script, cambiar `TAG_POR_DEFECTO`, correr los
    tests y volver a correr `generate_favicon.py` en las landings.
  - `tests/test_marcas.py` verifica que estén los 16, que cada uno empiece con `<svg`, sea de
    lienzo 120 y lleve el `color` de `IDENTIDAD[p]` (en el cuadrado de fondo), y que el kit
    coincida con el tag declarado si hay un checkout de libra-ui (si no, se saltea).
  - `scripts/generate_favicon.py` copia `marcas/<p>-favicon.svg` a `public/img/favicon.svg` y
    `marcas/<p>.svg` a `public/img/marca.svg` de cada landing, como bytes. Su `--check` exige
    igualdad de bytes y que la home (a mano) tenga el `<link rel="icon">`, **dos**
    `<img src="/img/marca.svg" ... width height>` (navbar y pie) y ningún `<div class="logo-icon">`
    de la marca anterior.
  - La marca de las páginas que genera el kit (docs y legales) y del pie de Restolibra es
    `<img src="/img/marca.svg" alt="" class="logo-icon" width="32|28" height="32|28">`. El SVG ya
    trae el cuadrado de color y el redondeo, así que `.logo-icon` pierde `background`,
    `border-radius`, `color` y `font-size` en `style.css.template` y `.f-logo` (VentaLibra) queda
    sólo con tamaño: con un `background` el color asomaría en las esquinas redondeadas. `alt=""`
    porque el nombre del producto está escrito al lado.
  - Sigue sin PNG (razón de ADR-008): quedan afuera el `apple-touch-icon` y el ícono de «agregar
    a inicio» de iOS.
- Consecuencias: cambian los dos `*_style.css.golden`, las páginas de `/docs/` y `/legal/` de
  las ocho landings y sus `style.css`. Cada landing recibe además `public/img/marca.svg` y
  edita a mano su `index.html`. Los 16 SVG viajan dentro del paquete (hatchling incluye todo
  el árbol de `libra_web_kit/`); las landings que instalan el kit por `docs_auth` cargan
  ~16 KB más. Sin tag nuevo todavía: lo corta quien mergea (minor).

## ADR-010 — El pulido de VentaLibra pasa a ser la línea común de las ocho landings

- Estado: aceptada
- Fecha: 2026-10-09
- Contexto: VentaLibra recibió en octubre un pulido propio: hero más alto, franja de
  puntos fuertes, rubros como tarjetas, pasos unidos por una línea, planes de igual
  altura, sección «Así se ve» con capturas de la demo, pie en cuatro columnas y
  preguntas frecuentes (libra-web-kit#66 a #71). Todo vivía en el slot `hero_extra`
  del bloque `ventalibra`, con los colores ámbar escritos a mano, así que ningún otro
  sitio podía usarlo. El humano pidió llevar las otras siete a la misma línea, «cada
  una con sus particularidades».
- Decisión:
  - El CSS pasa a `templates/pulido.css` y el template lo inserta en el slot nuevo
    `@@pulido@@`, justo donde estaba el `hero_extra` de VentaLibra, para que la cascada
    no cambie. Lo reciben los ocho sitios.
  - `pulido.css` no lleva colores de marca fijos. Usa `var(--brand*)` y las variables
    `--p-*`, que `css_gen` emite por sitio desde `site_css_tokens.PULIDO_VARS`: acento del
    hero, acento sobre fondo oscuro, fondos oscuros de la sección de capturas y del pie,
    grises del pie, borde de tarjetas y los `r,g,b` para las sombras.
  - El `hero_extra` de VentaLibra queda vacío. Los otros `hero_extra` siguen siendo
    lo propio de cada sitio, como el login de ContaLibra.
- Consecuencias:
  - VentaLibra se renderiza igual: la captura de página completa antes y después del
    cambio coincide píxel a píxel en escritorio, y en celular sólo difiere el
    antialiasing de un ícono.
  - Los golden de `contalibra` y `restolibra` se regeneraron, porque ahora incluyen el pulido.
  - Una página que no use las clases nuevas (`highlights`, `rubro`, `showcase`,
    `site-footer`, `faq-*`) igual recibe el hero más alto, la tipografía nueva y las
    tarjetas de igual altura.
