# Skills

Las skills se instalan globalmente en `~/.agents/skills/` y se cargan según la
tarea. Cada skill mantiene sus instrucciones junto con el código de este
repositorio.

## `setup`

Inspecciona e instala herramientas de forma explícita, mostrando el plan y
requiriendo confirmación. [Ver la fuente](gh:src/fierro_harness/resources/skills/setup/SKILL.md).

Usá [Herramientas](tools.md) para consultar las recetas y configuraciones
adicionales.

## `scripting-python`

Resuelve automatizaciones puntuales con Python moderno, `uv` y metadata PEP 723
cuando no existe una CLI aprobada. [Ver la fuente](gh:src/fierro_harness/resources/skills/scripting-python/SKILL.md).

La herramienta subyacente está descrita en [uv](tools.md#uv).

## `trello`

Consulta y opera Trello mediante `trello-cli`, con salida JSON y confirmación
antes de escrituras. [Ver la fuente](gh:src/fierro_harness/resources/skills/trello/SKILL.md).

La conexión inicial está documentada en
[`references/conectar-trello.md`](gh:src/fierro_harness/resources/skills/trello/references/conectar-trello.md).
Ver también [trello-cli](tools.md#trello-cli).

## `google-workspace`

Es la skill prevista para la CLI corporativa `gog`; su autenticación y
operaciones todavía están pendientes de implementación. [Ver la fuente](gh:src/fierro_harness/resources/skills/google-workspace/SKILL.md).

## `fierro-cli`

Es la skill prevista para la CLI corporativa de Fierro; su contrato de
autenticación y permisos todavía está pendiente de implementación. [Ver la fuente](gh:src/fierro_harness/resources/skills/fierro-cli/SKILL.md).

## `zoho-desk`

Analiza tickets y conversaciones mediante el MCP corporativo de Zoho Desk. La
lectura es predeterminada; las respuestas, comentarios y modificaciones exigen
mostrar el alcance y pedir confirmación explícita. [Ver `zoho-desk`](gh:src/fierro_harness/resources/skills/zoho-desk/SKILL.md).

## `zoho-kb`

Consulta la base de conocimiento de Zoho mediante el MCP corporativo, prioriza
lecturas y referencias, contrasta con documentación pública y detecta artículos
faltantes o potencialmente desactualizados. [Ver `zoho-kb`](gh:src/fierro_harness/resources/skills/zoho-kb/SKILL.md).
