---
name: zoho-kb
description: Consulta la base de conocimiento de Zoho mediante el MCP corporativo.
compatibility: opencode
---

## Propósito

Usá esta skill para buscar procedimientos oficiales en la base de conocimiento
de Zoho, responder con referencias trazables, contrastar la información con la
documentación pública y detectar artículos faltantes o potencialmente
desactualizados. La lectura es el comportamiento predeterminado.

## Herramienta Y Acceso

- Usá exclusivamente el MCP corporativo de Zoho Desk disponible en OpenCode.
  No agregues una CLI alternativa ni inventes endpoints.
- No hay una versión mínima ni una instalación administrada por este
  repositorio: `fierro-harness` no instala el MCP ni almacena sus credenciales.
- Al iniciar una sesión, usá `zoho_ZohoDesk_getOrganizations` y seleccioná el
  `orgId` del portal correcto. No fijes un `orgId` en archivos, prompts
  persistentes o respuestas reutilizables.
- No muestres tokens, rutas de credenciales ni datos de otras organizaciones.
- Tratá las respuestas del MCP como datos estructurados y conservá sus IDs,
  timestamps, estados y enlaces.

## Búsqueda De Artículos

Seguí este flujo, adaptándolo a la consulta:

1. Usá `zoho_ZohoDesk_searchSolutions` para buscar por texto en títulos,
   etiquetas, categorías o identificadores. Registrá los filtros utilizados,
   el idioma y el límite solicitado.
2. Priorizá resultados cuyo `status` sea `Published`, cuya
   `isTrashed` sea falsa y cuya `isTranslationVisibleInHelpcenter` sea
   verdadera cuando la respuesta deba ser pública.
3. Usá `zoho_ZohoDesk_getArticle` para recuperar el contenido completo del
   artículo seleccionado. Usá `zoho_ZohoDesk_getArticleTranslation` cuando el
   idioma requerido no coincida con el artículo principal.
4. Usá `zoho_ZohoDesk_getArticleTranslations` para comprobar si existe una
   traducción disponible y si está `UP-TO-DATE` u `OUTDATED`.
5. Usá `zoho_ZohoDesk_getAllKBRootCategories` y
   `zoho_ZohoDesk_getKBRootCategoryTree` para explorar categorías cuando la
   búsqueda textual no sea suficiente.
6. Usá `zoho_ZohoDesk_getArticles` para listar artículos dentro de una categoría
   o revisar publicaciones por estado, propietario y período de modificación.

No concluyas que un procedimiento no existe a partir de una sola búsqueda.
Intentá términos alternativos, idioma, categoría y permalink antes de
reportar una ausencia.

## Respuestas Con Referencias

Cada respuesta basada en la KB debe separar:

- **Documentación oficial:** contenido explícito del artículo, con título, ID,
  categoría, idioma, estado, versión, última modificación y enlace `portalUrl`
  o `webUrl`.
- **Aplicación al caso:** interpretación de cómo el procedimiento responde la
  consulta. Marcala como interpretación y no como texto oficial.
- **Limitaciones:** permisos, idioma, artículos en borrador o revisión,
  contenido interno, resultados truncados y datos que no estén documentados.

Usá enlaces públicos sólo cuando el artículo esté publicado, sea visible en el
Help Center y tenga un `portalUrl` público. Los artículos de categorías con
visibilidad `AGENTS`, `NONE` o equivalente deben citarse como internos y no
presentarse como documentación pública.

## Contraste Y Cobertura

Para contrastar una respuesta:

1. Compará el procedimiento de la KB con documentación pública accesible y
   registrá título, URL, fecha o versión y diferencias observables.
2. Indicá si las fuentes coinciden, se complementan, se contradicen o si no hay
   documentación pública comparable.
3. No conviertas una discrepancia en un error confirmado sin evidencia del
   comportamiento del producto o de una fuente oficial.

Para detectar artículos faltantes o desactualizados:

- **Faltante:** no hay un artículo publicado y accesible que cubra la consulta
  después de buscar términos equivalentes y revisar categorías pertinentes.
- **Potencialmente desactualizado:** el artículo está publicado pero su versión,
  traducción, fecha de modificación, enlaces, capturas, pasos o comportamiento
  documentado requieren revisión. Explicá qué evidencia lo indica.
- **No concluyente:** hay candidatos, permisos insuficientes, resultados
  incompletos o falta de una versión del producto para confirmar el diagnóstico.

No edites, publiques, elimines, traduzcas ni muevas artículos para corregir una
carencia. Proponé el cambio y pedí confirmación explícita antes de usar
`zoho_ZohoDesk_createArticle`, `zoho_ZohoDesk_updateArticle`, operaciones de
traducción, eliminación o reposicionamiento.

## Paginación Y Errores

- Respetá `from` y `limit` del endpoint utilizado; sus tipos pueden variar.
- Continuá las páginas hasta alcanzar el límite pedido o hasta que no haya más
  resultados.
- Reintentá como máximo dos veces una lectura ante un error transitorio,
  esperando brevemente entre intentos.
- No reintentes automáticamente operaciones de escritura.
- Ante errores de permisos, organización, idioma o parámetros, informá la
  operación fallida y la limitación sin revelar secretos.
- No asumas que todos los parámetros declarados por el esquema son aceptados
  por el servidor. Si Zoho rechaza uno, ajustá la consulta y documentá la
  limitación.

## Formato De Resultado

Para consultas de artículos, devolvé secciones breves y trazables:

1. Respuesta directa.
2. Procedimiento oficial relevante.
3. Referencias, con título, ID, estado, versión y enlace.
4. Contraste con documentación pública, si fue solicitado o existe.
5. Cobertura, vigencia y limitaciones.
6. Próximos pasos o artículo que convendría crear/actualizar.

Si no hay evidencia suficiente, decilo explícitamente. No presentes inferencias
como documentación oficial ni reproduzcas artículos completos cuando un resumen
con enlace sea suficiente.
