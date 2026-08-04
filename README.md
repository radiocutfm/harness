# Fierro Agents Harness

Repositorio interno de Lambda/Fierro para versionar e instalar skills y herramientas que utilizarán agentes de OpenCode.

## Alcance actual

Este repositorio contiene el boilerplate inicial:

- `install.py`: script Python ejecutado con `uv run`.
- `install.sh`: bootstrap para Linux.
- `install.ps1`: bootstrap para Windows PowerShell.
- `skills/`: skills globales compatibles con OpenCode.
- `.github/workflows/release.yml`: publicación de los artefactos de instalación.

La implementación se realizará progresivamente mediante los issues del repositorio.

## Instalación

Linux:

```sh
curl -fsSL https://github.com/radiocutfm/harness/releases/latest/download/install.sh | sh
```

Windows PowerShell:

```powershell
irm https://github.com/radiocutfm/harness/releases/latest/download/install.ps1 | iex
```

Volver a ejecutar el instalador equivale a volver a instalar o reconciliar el entorno.

## Skills

Las skills iniciales son:

- `trello`
- `google-workspace`
- `fierro-cli`
- `zoho-desk`
- `zoko-kb`
- `scripting-python`

Las skills de integración todavía son contratos iniciales. Cada una deberá documentar sus herramientas requeridas, versiones mínimas, instalación, autenticación y operaciones soportadas antes de habilitarse.

## Seguridad

No versionar tokens, cookies, contraseñas ni configuración personal. Las integraciones deben preferir CLIs con salida JSON cuando exista una alternativa razonable y deben proteger las credenciales usando los mecanismos seguros de cada herramienta.
