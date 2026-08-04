---
name: trello
description: Consulta Trello mediante su API REST oficial y un script Python seguro.
compatibility: opencode
---

## Decisión

Usá la API REST oficial de Trello a través de `scripts/trello.py`. No se adopta una CLI de terceros: la API tiene superficie, autenticación y límites publicados, mientras que el script conserva una interfaz intercambiable y ejecutable con `uv` en Linux y Windows.

## Uso

- Pedí que el usuario exponga `TRELLO_API_KEY` y `TRELLO_API_TOKEN` en su sesión; nunca los pongas en comandos, archivos, logs o JSON.
- Ejecutá `uv run scripts/trello.py boards`, `board <id>`, `lists <board-id>`, `cards <board-id>` o `search <texto>`.
- La salida es JSON. Aplicá `--limit` para acotar colecciones y `--timeout` cuando corresponda.
- Esta versión es sólo de lectura. Antes de proponer una futura escritura, mostrale al usuario el tablero, la lista, los registros afectados y el contenido completo, y pedí confirmación.

## Límites y errores

- El script reintenta respuestas transitorias y `429` con espera acotada. No implementes polling; para sincronizaciones futuras evaluá webhooks.
- Si recibe `401` o `403`, informá el problema de autorización sin revelar los valores usados.
- Consultá `references/api.md` antes de extender endpoints o autenticación.
