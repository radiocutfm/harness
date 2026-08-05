# Conectar Trello

La primera vez, la persona sólo tiene que aprobar el acceso en Trello. No tiene que crear variables de entorno ni copiar contraseñas en archivos.

1. Confirmá que `trello-cli` está instalado con `fierro-harness setup --install trello-cli`.
2. Pedí permiso para abrir la ventana de conexión y ejecutá `trello-cli auth login --key <clave-de-integración>`.
3. Si el harness todavía no tiene una clave de integración de la empresa, no pidas que la persona cree una aplicación ni un Power-Up. Explicá que falta habilitar la integración corporativa y derivala al responsable indicado.
4. Cuando se abra Trello, la persona inicia sesión si hace falta y elige **Permitir**. Al terminar, puede cerrar la pestaña y volver a la conversación.
5. Verificá la conexión con `trello-cli auth whoami -o json`.

La CLI guarda el acceso en su configuración local. Para desconectarlo, solicitá confirmación y ejecutá `trello-cli auth logout`.

# Consultas

Usá `trello-cli` y pedí formato JSON con `-o json`.

- Tableros: `member boards me --fields name,url -o json`
- Listas: `board lists <id-del-tablero> -o json`
- Tarjetas: `list cards <id-de-la-lista> -o json`
- Búsqueda: `search run --query <texto> -o json`

Antes de crear, editar, mover, cerrar, comentar o adjuntar algo, mostrale a la persona el tablero, los elementos afectados y el resultado esperado. Recién ejecutá la acción después de una confirmación explícita. Usá `--dry-run` cuando la operación lo admita.
