# Autenticación de Trello

La integración usa `trello-cli`.

1. Instalá la herramienta: `fierro-harness setup --install trello-cli --yes`.
2. Iniciá sesión en Trello y abrí https://trello.com/power-ups/admin.
3. Creá un Power-Up, abrí la pestaña **API key** y generá una clave.
4. Ejecutá `trello-cli auth login --key <api-key>`.
5. En la ventana de Trello, elegí **Permitir**.
6. Verificá la cuenta conectada: `trello-cli auth whoami -o json`.

Para desconectar la cuenta, ejecutá `trello-cli auth logout`.
