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

## Configuración adicional

- OpenCode usa `deepseek/deepseek-v4-flash` como modelo administrado si no hay
  una configuración personal en conflicto.
- Trello requiere una API key por cuenta; ver [Secretos](secretos.md).
- Las skills pendientes de implementación deben informar su bloqueo y no
  improvisar otra CLI.
