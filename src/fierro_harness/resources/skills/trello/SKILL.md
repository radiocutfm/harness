---
name: trello
description: Consulta y opera Trello mediante trello-cli.
compatibility: opencode
---

## Autenticación

Antes de la primera operación, seguí `references/conectar-trello.md`.

## Consultas

Usá `-o json` para salida estructurada.

- Identidad y tableros: `trello-cli auth whoami -o json` y `trello-cli member boards me --fields name,url -o json`.
- Tablero y listas: `trello-cli board get <id-del-tablero> -o json` y `trello-cli board lists <id-del-tablero> -o json`.
- Tarjetas de una lista: `trello-cli list cards <id-de-la-lista> -o json`.
- Búsqueda: `trello-cli search run --query <texto> -o json`.
- Actividad reciente: `trello-cli board actions <id-del-tablero> --since <fecha-iso> --limit 50 -o json`.

## Escrituras

Antes de escribir, mostrá el tablero, la lista, los elementos afectados y el resultado esperado; pedí confirmación explícita inmediatamente antes de ejecutar.

- Crear tarjeta: `trello-cli card create --idList <id-de-la-lista> --name <título>`.
- Actualizar tarjeta, incluyendo vencimiento: `trello-cli card update <id-de-la-tarjeta> --due <fecha-iso>`.
- Comentar: `trello-cli card comment <id-de-la-tarjeta> --text <comentario>`.
- Adjuntar un archivo: `trello-cli card attach <id-de-la-tarjeta> --file <ruta-del-archivo>`.
- Usá `--dry-run` cuando esté disponible. No hagas escrituras masivas ni acciones destructivas sin una confirmación reforzada.

Ante un error de autorización o límite, explicá qué pasó sin mostrar claves, tokens, rutas de credenciales ni datos de otra cuenta.
