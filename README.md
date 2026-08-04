# Fierro Agents Harness

Repositorio interno para instalar, configurar y mantener el entorno corporativo de agentes de Lambda/Fierro.

<details>
<summary>Contexto y objetivos</summary>

El harness centraliza herramientas CLI, skills de OpenCode, políticas, diagnóstico, actualización y recuperación para personal administrativo, soporte, operaciones y otras áreas. Prioriza seguridad, recuperación, simplicidad, observabilidad, reproducibilidad y portabilidad.

La primera plataforma soportada es OpenCode, con OpenCode Desktop o `opencode web` como experiencia de uso. Las integraciones prefieren CLIs observables con salida JSON antes que MCP cuando existe una alternativa razonable.
</details>

## Instalación y actualización

Linux:

```sh
curl -fsSL https://github.com/radiocut/harness/releases/latest/download/install.sh | sh
```

Windows PowerShell:

```powershell
irm https://github.com/radiocut/harness/releases/latest/download/install.ps1 | iex
```

Ejecutar el instalador nuevamente debe reconciliar y reparar la instalación. La versión específica se fija con `FIERRO_AGENTS_VERSION=0.1.0` en Linux o `$env:FIERRO_AGENTS_VERSION = "0.1.0"` en PowerShell. Estos comandos quedarán activos cuando exista el primer release.

## Experiencias previstas

El launcher principal abrirá OpenCode Web localmente (`opencode web`), con el servidor limitado a `127.0.0.1` por defecto. También habrá launchers para diagnóstico, actualización y documentación.

Ejemplos de tareas esperadas:

- “Armá una planilla con los reportes de errores de Zoho y separá hechos de hipótesis.”
- “Creame un PDF con la lista de libros nuevos del usuario de Fierro.”
- “Buscá en la base de conocimiento el procedimiento oficial y citá el artículo.”
- “Convertí estos tickets repetidos en requerimientos de Trello, mostrame el resumen y pedime confirmación antes de crear cada tarjeta.”

## Estado

Este commit es el boilerplate inicial. Las implementaciones se desarrollarán en issues pequeñas y ordenadas por dependencia.

## Desarrollo

Requiere Python 3.14+ para ejecutar el script del instalador; `uv` es el único runtime recomendado. No hay un paquete Python: el instalador final es un único `install.py` con metadata PEP 723.

```sh
uv run --with pytest pytest
```

No se versionan tokens, cookies, contraseñas ni archivos de configuración personales.
