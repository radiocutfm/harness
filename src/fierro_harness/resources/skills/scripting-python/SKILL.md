---
name: scripting-python
description: Cortapluma general para resolver tareas automatizables con Python, uv y metadata PEP 723 cuando no existe una herramienta obvia.
compatibility: opencode
metadata:
  audience: employees
  owner: fierro
---

## Propósito

Esta skill es la cortapluma de uso general del harness. No hace falta que el usuario pida literalmente “hacé un script”. Activala cuando una tarea no tenga una CLI o herramienta obvia, pero pueda resolverse de forma clara, repetible y observable con Python. Esto incluye consultar, transformar, combinar, validar, generar o actualizar datos y archivos.

Preferí un único archivo Python ejecutado con `uv run script.py`, no un proyecto Python completo. Se pueden declarar dependencias en la metadata PEP 723 y `uv` debe resolverlas de forma reproducible.

## Cuándo no usarla

No reemplaces una CLI corporativa o una integración existente por Python. Usá primero la herramienta aprobada cuando exista, especialmente para autenticación y operaciones sobre sistemas externos. Si la tarea requiere una aplicación persistente, un servicio o una base de código grande, abrí una implementación específica.

## Reglas

- Requerí Python moderno, `argparse`, docstrings, tipos y funciones pequeñas.
- Usá metadata PEP 723 y dependencias reconocidas, actualizadas y mantenidas.
- Si hacen falta dependencias, declaralas en `# dependencies = [...]` y ejecutá el archivo con `uv run`; no pidas al usuario una instalación global de paquetes.
- Emití JSON o CSV; definí `--dry-run` para toda escritura.
- Usá variables de entorno o almacenes seguros para secretos; nunca los imprimas.
- Definí timeouts de red y manejá errores explícitamente.
- Si el usuario lo solicita, guardá scripts en `~/Documents/scripts/` (o equivalente ) y explicá su ubicación.

## Plantilla

```python
# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Describe qué automatiza el script."""
import argparse
import json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    print(json.dumps({"ok": True, "dry_run": args.dry_run}, ensure_ascii=False))


if __name__ == "__main__":
    main()
```

## Verificación

Comprobá que `uv run script.py --dry-run` funciona antes de cualquier escritura. Mostrá al usuario los destinos y cantidades afectadas y pedí confirmación antes de ejecutar una acción irreversible.
