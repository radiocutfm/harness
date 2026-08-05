# Secretos

Los secretos no se guardan en el repositorio ni en `opencode.json`. Por ahora,
las credenciales corporativas se comparten manualmente mediante Passbolt y se
exponen sólo al proceso que las necesita.

Cuando una skill necesita un secreto:

1. pedilo a la persona usuaria indicando qué servicio y operación lo requieren
2. obtenelo desde el mecanismo corporativo aprobado
3. pasalo por variable de entorno o por el almacén seguro de la herramienta
4. no lo imprimas, no lo escribas en archivos del proyecto y no lo incluyas en
   logs, prompts persistentes, issues o PRs

Para Trello, la API key se obtiene desde [Power-Up
administration](https://trello.com/power-ups/admin) y se entrega a
`trello-cli auth login`; el CLI conserva sus credenciales según su mecanismo
oficial.

El token de DeepSeek todavía requiere configuración oficial de OpenCode. La
integración prevista con Passbolt se implementará en un issue separado.
