---
name: zoho-desk
description: Analiza tickets y conversaciones de Zoho Desk mediante el MCP corporativo.
compatibility: opencode
---

## Propósito

Usá esta skill para consultar, analizar y, con confirmación explícita, responder
tickets de Zoho Desk. La lectura es el comportamiento predeterminado. La skill
cubre resúmenes, cronologías, clasificación, separación entre hechos e
hipótesis, próximos pasos, respuestas propuestas, detección de casos repetidos y
análisis de temas frecuentes.

## Herramienta Y Acceso

- Usá el MCP de Zoho Desk disponible en el entorno de OpenCode. No agregues una
  CLI alternativa ni inventes endpoints.
- No hay una instalación ni una versión mínima administrada por este
  repositorio: la disponibilidad, versión y autenticación del MCP son
  responsabilidad del entorno que ejecuta OpenCode. `fierro-harness` no instala
  ni almacena sus credenciales.
- Al iniciar una sesión, usá `zoho_ZohoDesk_getOrganizations` para identificar
  las organizaciones disponibles y seleccioná el `orgId` del portal correcto.
- No fijes un `orgId` en archivos, prompts persistentes o respuestas reutilizables.
- No muestres tokens, rutas de credenciales ni datos de otras organizaciones.
- Las respuestas del MCP ya son datos estructurados. Conservá IDs, timestamps,
  estados y enlaces al presentar resultados; no conviertas la respuesta en texto
  libre si la persona pidió JSON.

## Lectura De Tickets

Para un ticket, segui este orden:

1. Usá `zoho_ZohoDesk_getTicket` para obtener asunto, estado, contacto,
   departamento, canal, etiquetas y metadatos básicos.
2. Usá `zoho_ZohoDesk_getThreads` para enumerar las conversaciones y
   `zoho_ZohoDesk_getThread` para obtener el contenido completo de un thread.
   Pedí `include: plainText` cuando necesites analizar texto sin HTML.
3. Usá `zoho_ZohoDesk_getTicketConversations` cuando necesites una vista única
   de threads y comentarios.
4. Usá `zoho_ZohoDesk_getTicketHistory` para reconstruir cambios de estado,
   asignaciones, comentarios, notificaciones y eventos del ticket.
5. Usá `zoho_ZohoDesk_getTicketsMetrics` para tiempos de respuesta, resolución,
   reaperturas y agentes involucrados.
6. Usá `zoho_ZohoDesk_suggestArticlesForTicket` para consultar artículos que
   Zoho considera relacionados.

Para buscar tickets relacionados, usá `zoho_ZohoDesk_doSearch` o las operaciones
de búsqueda específicas disponibles. No asumas que todos los parámetros
declarados por el esquema son aceptados por el servidor: si una operación
rechaza un parámetro, ajustá la consulta y explicá la limitación.

## Análisis

### Resumen

Incluí el ID y número del ticket, el problema informado, el contexto técnico,
las acciones ya realizadas y el estado actual. Diferenciá claramente lo que
surge del ticket de cualquier interpretación.

### Cronología

Ordená los eventos por timestamp e indicá fecha, actor, tipo de evento y efecto.
Usá threads, comentarios e historial; no reconstruyas una secuencia únicamente
a partir del asunto o del último mensaje.

### Hechos E Hipótesis

- **Hechos:** datos explícitos del ticket, sus threads, comentarios, historial,
  adjuntos o métricas.
- **Hipótesis:** explicaciones o causas posibles que todavía no están probadas.
- **Pendientes:** información necesaria para confirmar o descartar una hipótesis.

Cada conclusión relevante debe citar el ID del ticket o thread y, cuando sea
posible, su timestamp. No presentes inferencias como información oficial.

### Repetidos Y Tendencias

Para casos repetidos, buscá candidatos y compará asunto, descripción, contacto,
producto, error, canal y período. Informá coincidencias y diferencias; no
fusiones, cierres ni cambios de estado automáticos.

Para temas frecuentes o necesidades de capacitación, indicá el intervalo de
tiempo, los filtros, el tamaño de la muestra y las limitaciones de los datos.
No generalices a partir de un único ticket.

## Paginación Y Errores

- Respetá `from` y `limit` del endpoint utilizado. Sus tipos pueden variar entre
  operaciones.
- Continuá las páginas hasta que no haya más resultados o hasta alcanzar el
  límite solicitado por la persona.
- Reintentá como máximo dos veces una lectura ante un error transitorio,
  esperando brevemente entre intentos.
- No reintentes automáticamente operaciones de escritura: podrías duplicar un
  comentario o una respuesta.
- Ante un error de permisos, organización o parámetros, informá la operación
  que falló y qué dato falta, sin revelar secretos.

## Respuestas Y Escrituras

Redactá inicialmente la respuesta en la conversación de OpenCode, sin escribir
en Zoho Desk. Antes de usar cualquiera de estas operaciones:

- `zoho_ZohoDesk_draftsReply`
- `zoho_ZohoDesk_sendReply`
- `zoho_ZohoDesk_createTicketComment`
- `zoho_ZohoDesk_updateTicketComment`
- `zoho_ZohoDesk_updateTicket`

mostrá y pedí confirmación explícita inmediatamente antes de ejecutar. El
resumen previo debe incluir:

- número e ID del ticket;
- destinatario y canal;
- visibilidad pública o privada;
- contenido completo propuesto;
- cambio de estado, si corresponde;
- adjuntos, si los hubiera.

No hagas escrituras masivas, cierres, eliminaciones, fusiones ni cambios de
asignación sin una confirmación reforzada que indique el alcance exacto.

## Formato De Resultado

Para análisis, devolvé secciones breves y trazables:

1. Identificación del ticket.
2. Resumen.
3. Hechos comprobados.
4. Cronología.
5. Hipótesis y pendientes.
6. Próximos pasos.
7. Fuentes consultadas.

Si no hay evidencia suficiente, decilo explícitamente. No descargues ni
reproduzcas adjuntos salvo que sean necesarios para la solicitud y la persona lo
indique.
