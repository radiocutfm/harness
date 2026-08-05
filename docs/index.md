# Fierro Harness

Fierro Harness instala las skills y herramientas aprobadas para trabajar con
OpenCode en Lambda. El sitio integrado se publica junto con la documentación
de Fierro; las fuentes se mantienen en este repositorio y se validan también de
manera independiente.

## Objetivos

- instalar una base reproducible para OpenCode
- distribuir skills corporativas sin sobrescribir configuración personal
- ofrecer herramientas aprobadas con instalación explícita y verificable
- mantener documentación navegable para personas y agentes

## Instalación rápida

```{tab-set}

```{tab-item} Windows

```powershell
irm https://github.com/radiocutfm/harness/releases/latest/download/install.ps1 | iex
```

```

```{tab-item} Linux

```sh
curl -fsSL https://github.com/radiocutfm/harness/releases/latest/download/install.sh | sh
```

```

```{tab-item} macOS

```sh
curl -fsSL https://github.com/radiocutfm/harness/releases/latest/download/install.sh | sh
```

```

```

El instalador se puede ejecutar nuevamente para reparar o reconciliar el
entorno. Para detalles de herramientas, autenticación y configuración inicial,
seguí [Herramientas](tools.md).

```{toctree}
:maxdepth: 2
:caption: Uso

skills.md
tools.md
secretos.md
```

```{toctree}
:maxdepth: 2
:caption: Desarrollo

development.md
```
