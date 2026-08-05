---
name: trello
description: Consulta y opera Trello mediante una CLI integrada, con conexión guiada y credenciales protegidas.
compatibility: opencode
---

## Conectar una cuenta

Antes de la primera consulta, seguí `references/conectar-trello.md`. Guiá a la persona paso a paso; no asumas que conoce términos técnicos ni le pidas configurar variables de entorno.

## Consultar y cambiar datos

- Usá `trello-cli` para cada operación de Trello y pedí salida JSON con `-o json`.
- Consultá antes de modificar. Para una escritura, mostrale a la persona el tablero, la lista, los elementos afectados y el resultado esperado.
- Pedí confirmación explícita inmediatamente antes de crear, editar, mover, cerrar, comentar o adjuntar.
- Usá `--dry-run` cuando esté disponible. No hagas operaciones destructivas masivas.
- Ante un error de autorización o límite, explicá qué pasó sin mostrar claves, tokens, rutas de credenciales ni datos de otra cuenta.
