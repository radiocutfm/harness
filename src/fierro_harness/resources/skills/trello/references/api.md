# Trello API

## Opción elegida

Se usa la API REST oficial de Trello mediante un script Python PEP 723 sin dependencias externas. La autenticación usa una API key y un token personal provistos en `TRELLO_API_KEY` y `TRELLO_API_TOKEN` sólo durante la ejecución. No se guardan ni se muestran.

La interfaz inicial es de sólo lectura:

- `GET /1/members/me/boards`
- `GET /1/boards/{id}`
- `GET /1/boards/{id}/lists`
- `GET /1/boards/{id}/cards`
- `GET /1/search`

Cada comando emite JSON y limita la cantidad de elementos devueltos localmente. No hay operaciones de escritura ni destructivas en esta versión.

## Seguridad y operación

Trello limita las solicitudes por API key y por token, y responde `429` al excederlos. El script reintenta `429` y errores `5xx` hasta tres veces, usando `Retry-After` cuando está disponible. Los errores redactan la URL para que no exponga los parámetros de autenticación.

No almacenar los secretos en repositorios, archivos de configuración ni estado del harness. Para automatizaciones persistentes, usar un proveedor de secretos aprobado antes de programar consultas.

## Fuentes

- https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/
- https://developer.atlassian.com/cloud/trello/guides/rest-api/authorization/
- https://developer.atlassian.com/cloud/trello/guides/rest-api/rate-limits/
- https://developer.atlassian.com/cloud/trello/rest/api-group-boards/
