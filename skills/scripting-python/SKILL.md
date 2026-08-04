---
name: scripting-python
description: Crea y ejecuta automatizaciones pequeñas como scripts Python portables con uv y metadata PEP 723.
compatibility: opencode
metadata:
  audience: employees
  owner: fierro
---

## Propósito

Usá esta skill para automatizaciones pequeñas y observables. Preferí un único archivo Python ejecutado con `uv run script.py`, no un proyecto Python completo.

## Reglas

- Requerí Python moderno, `argparse`, docstrings, tipos y funciones pequeñas.
- Usá metadata PEP 723 y dependencias reconocidas, actualizadas y mantenidas.
- Emití JSON o CSV; definí `--dry-run` para toda escritura.
- Usá variables de entorno o almacenes seguros para secretos; nunca los imprimas.
- Definí timeouts de red y manejá errores explícitamente.
- Si el usuario lo solicita, guardá scripts en `~/Documents/scripts/` y explicá su ubicación.

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

