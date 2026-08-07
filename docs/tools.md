# Herramientas

La skill [`setup`](skills.md#setup) inspecciona las herramientas y sólo instala
las que la persona selecciona. Para ver el estado actual:

```sh
fierro-harness setup --json
```

Para mostrar una receta sin ejecutarla:

```sh
fierro-harness setup --install <herramienta>
```

Después de revisar el plan, confirmalo con `--yes`. En automatizaciones se puede
usar `FIERRO_HARNESS_ASSUME_YES=1`.

## OpenCode CLI

La CLI `opencode` ejecuta el agente y se instala desde la documentación oficial
con npm. Su autenticación se configura mediante el mecanismo oficial de
OpenCode; no se guardan tokens en este repositorio.

## OpenCode Desktop

OpenCode Desktop es independiente de la CLI. Harness detecta la aplicación en
Windows x64 y Linux, y descarga los paquetes oficiales `.exe`, `.deb` o `.rpm`
con SHA-256 fijado antes de instalarlos.

```sh
fierro-harness setup --install opencode-desktop
fierro-harness setup --install opencode-desktop --yes
```

En Linux se requiere `sudo`; una política corporativa puede exigir que la
instalación la realice el área administradora.

## uv

`uv` administra Python, entornos y scripts PEP 723. Se instala con el instalador
oficial de Astral y debe quedar disponible en `PATH`.

## jq

`jq` procesa JSON desde la shell. Harness descarga el binario correspondiente
a la plataforma y verifica su checksum antes de copiarlo al directorio local.

## trello-cli

[`trello-cli`](https://github.com/hammashamzah/trello-cli) permite consultar y
actualizar Trello desde comandos estructurados. Instalalo explícitamente:

```sh
fierro-harness setup --install trello-cli --yes
```

Para conectar una cuenta, creá una API key desde [Power-Up
administration](https://trello.com/power-ups/admin) y ejecutá:

```sh
trello-cli auth login --key <api-key>
trello-cli auth whoami -o json
```

No pegues la key en un issue, PR o archivo del repositorio.

## MCP de Zoho Desk

La skill `zoho-desk` usa el MCP corporativo disponible en el entorno de
OpenCode. `fierro-harness` no instala una CLI de Zoho ni guarda sus tokens.

Al comenzar una sesión, consultá las organizaciones disponibles con
`zoho_ZohoDesk_getOrganizations` y usá el `orgId` del portal correcto. Para
trabajar con tickets se consultan `getTicket`, `getThreads`, `getThread`,
`getTicketConversations`, `getTicketHistory` y `getTicketsMetrics`. Las búsquedas
y los artículos sugeridos se usan como fuentes adicionales, no como evidencia
automática de una resolución.

La lectura no requiere confirmación adicional. Antes de usar operaciones que
envíen respuestas, agreguen comentarios o modifiquen tickets, la skill debe
mostrar ticket, destinatario, canal, visibilidad, contenido y cambios previstos,
y pedir confirmación explícita. No se guardan tokens, `orgId` ni contenido de
tickets en el repositorio.

## MCP de Zoho Knowledge Base

La skill `zoho-kb` usa el mismo MCP corporativo de Zoho Desk para consultar la
base de conocimiento. No requiere una CLI, instalación, versión mínima ni
credenciales nuevas: `fierro-harness` no instala el MCP ni guarda sus tokens.

Las consultas comienzan identificando la organización con
`zoho_ZohoDesk_getOrganizations`. Para buscar y verificar artículos se usan
`searchSolutions`, `getArticle`, `getArticleTranslation`,
`getArticleTranslations`, `getAllKBRootCategories`,
`getKBRootCategoryTree` y `getArticles`. Las respuestas deben citar el título,
ID, categoría, idioma, estado, versión, fecha de modificación y enlace cuando
estén disponibles.

La skill distingue artículos públicos de contenido interno y no presenta
inferencias como documentación oficial. Crear, editar, eliminar, traducir,
publicar o reposicionar artículos requiere mostrar el alcance y pedir
confirmación explícita.

## Configuración adicional

- OpenCode usa `deepseek/deepseek-v4-flash` como modelo administrado si no hay
  una configuración personal en conflicto.
- Trello requiere una API key por cuenta; ver [Secretos](secretos.md).
