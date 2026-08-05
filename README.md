# Fierro Agents Harness

Instalador corporativo de skills y configuración inicial para OpenCode. Los bootstraps de distribución viven en `bootstrap/`; los releases los publican como `install.sh` e `install.ps1`.

## Instalación

En Windows PowerShell:

```powershell
irm https://github.com/radiocutfm/harness/releases/latest/download/install.ps1 | iex
```

En Linux:

```sh
curl -fsSL https://github.com/radiocutfm/harness/releases/latest/download/install.sh | sh
```


El instalador se puede ejecutar nuevamente para reparar o reconciliar el entorno. Actualmente instala las skills globales y configura el modelo predeterminado de OpenCode.

## Qué se instala

Las skills quedan disponibles globalmente para OpenCode en:

```text
~/.agents/skills/
```

En esta versión se incluyen:

- `scripting-python`: herramienta general para resolver tareas automatizables con Python y `uv`.
- `setup`: prepara herramientas requeridas por las skills.
- `trello`, `google-workspace`, `fierro-cli`, `zoho-desk` y `zoko-kb`: skills iniciales de integración.

Las integraciones que todavía requieren configuración de sus herramientas se habilitan progresivamente. La skill `setup` puede preparar el conjunto completo cuando esas herramientas estén definidas.

## Modelo y autenticación

OpenCode queda configurado con DeepSeek V4 Flash como modelo predeterminado. El identificador configurado es `deepseek/deepseek-v4-flash`; se verificará contra el catálogo disponible del proveedor antes de fijar una release estable.

El token de DeepSeek no se guarda en este repositorio ni en `opencode.json`. La integración prevista es obtenerlo desde Passbolt y exponerlo sólo al proceso de OpenCode. Hasta que esa integración esté implementada, el usuario debe configurar su autenticación mediante el mecanismo oficial de OpenCode.

Si el usuario ya tiene otro modelo configurado, el instalador informa el conflicto y no reemplaza la configuración personal. Antes de modificar `opencode.json` crea un backup.

## Automatización web

La automatización web con Playwright Python está definida en el issue #22 y todavía no forma parte de la instalación estable.

## Trello

La integración usa [`trello-cli`](https://github.com/hammashamzah/trello-cli). Para instalarla de forma explícita, ejecutá:

```sh
fierro-harness setup --install trello-cli --yes
```

Para conectar una cuenta, iniciá sesión en Trello, abrí [Power-Up administration](https://trello.com/power-ups/admin), creá un Power-Up y generá una API key en su pestaña **API key**. Luego ejecutá:

```sh
trello-cli auth login --key <api-key>
```

La herramienta abre Trello para aprobar el acceso. Comprobá la cuenta conectada con `trello-cli auth whoami -o json`.

## Seguridad

No incluir tokens, cookies, contraseñas, prompts ni datos de clientes en este repositorio. Las acciones de escritura en servicios externos deben pedir confirmación y mostrar previamente el destino y el alcance.

## Estado

El flujo básico de instalación ya funciona. La instalación de herramientas, automatización web, OAuth de Google Workspace, Passbolt, Trello y las integraciones de Fierro se implementan en sus issues correspondientes.
