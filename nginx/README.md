# libra-nginx-web

Imagen base de nginx compartida por las 5 landings de la familia Libra.
Extraída 2026-07-26 (P3 del plan de consolidación, continuación) tras
confirmar que `nginx.conf` era idéntico entre Contalibra/Restolibra/
Gestiolibra/MedLibra/VentaLibra salvo el nombre del upstream de auth
(3 apariciones) -- ver
`wiki/analyses/auditoria-duplicacion-familia-libra.md`.

Publicada en GitHub Container Registry como
`ghcr.io/marianocappucci/libra-nginx-web` (imagen **pública** -- no
contiene nada sensible, solo un template de nginx, así que el VPS no
necesita autenticarse contra el registro para hacer `docker pull`).

## Uso

En el `Dockerfile` raíz de cada landing:

```dockerfile
FROM ghcr.io/marianocappucci/libra-nginx-web:v1
COPY public/ /usr/share/nginx/html/
EXPOSE 80
```

Y en `docker-compose.yml`, el servicio `web` necesita la env var:

```yaml
environment:
  - AUTH_UPSTREAM=gestiolibra-web-auth
```

(el nombre del servicio `auth` de ese mismo `docker-compose.yml`).

## Cómo funciona

Usa el soporte nativo de `envsubst` del `docker-entrypoint` oficial de
nginx: cualquier archivo en `/etc/nginx/templates/*.template` se procesa
con las variables de entorno definidas en el contenedor al arrancar, y el
resultado se escribe en `/etc/nginx/conf.d/`. El entrypoint solo sustituye
variables que existen como env var real del contenedor -- las variables
propias de nginx (`$host`, `$uri`, `$http_cookie`, etc.) no colisionan
porque no están en el entorno del proceso.
