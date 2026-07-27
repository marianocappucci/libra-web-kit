# Imagen base de nginx compartida por las 5 landings de la familia Libra
# (Contalibra, Restolibra, Gestiolibra, MedLibra, VentaLibra) -- extraído
# 2026-07-26, nginx.conf era idéntico entre las cinco salvo el nombre del
# upstream de auth (3 apariciones). Ver
# wiki/analyses/auditoria-duplicacion-familia-libra.md (P3, continuación).
#
# Usa el soporte nativo de envsubst del docker-entrypoint oficial de
# nginx: cualquier archivo en /etc/nginx/templates/*.template se procesa
# con las variables de entorno definidas en el contenedor (no las
# variables propias de nginx como $host/$uri -- el entrypoint solo
# sustituye las que existen como env var real, así que no colisiona) y el
# resultado se escribe en /etc/nginx/conf.d/ al arrancar. Cada consumidor
# solo necesita setear AUTH_UPSTREAM.
FROM nginx:1.27-alpine
RUN rm -f /etc/nginx/conf.d/default.conf
COPY default.conf.template /etc/nginx/templates/default.conf.template
