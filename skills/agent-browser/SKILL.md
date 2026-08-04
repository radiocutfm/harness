---
name: agent-browser
description: Automatiza navegación web con agent-browser usando snapshots, referencias y las skills oficiales servidas por su CLI.
compatibility: opencode
metadata:
  audience: employees
  owner: fierro
---

## Herramienta requerida

- `agent-browser`: la versión mínima debe definirse y fijarse en la issue de integración antes de una release estable.
- Node.js y npm para la instalación oficial.
- Chrome for Testing, instalado con `agent-browser install`.
- En Linux, las dependencias del navegador pueden requerir `agent-browser install --with-deps`.

Si falta la herramienta, ofrecé instalarla siguiendo el procedimiento oficial y pedí confirmación. No descargues binarios desde fuentes alternativas.

## Skills oficiales

Las instrucciones actualizadas se sirven desde la versión instalada de la CLI:

```sh
agent-browser skills list --json
agent-browser skills get core --full
```

Usá `core` para navegación, snapshots, formularios, screenshots, extracción, sesiones y autenticación. No copies manualmente su contenido dentro de esta skill: la documentación indica que puede quedar desactualizado. La skill del harness ya funciona como punto de descubrimiento; no hace falta instalar otra skill mediante `npx`.

```sh
agent-browser skills get core --full
```

## Flujo básico

1. Abrí la URL con `agent-browser open`.
2. Obtené un snapshot interactivo con `agent-browser snapshot -i`.
3. Usá las referencias del snapshot para hacer click o completar campos.
4. Tomá otro snapshot después de cada cambio de página.
5. Cerrá la sesión al terminar.

## Seguridad

- No navegues a sitios ni envíes datos sin autorización del usuario.
- Confirmá antes de enviar formularios, mensajes, emails, o cualquier cambio sensible.
- No expongas cookies, tokens, almacenamiento local ni screenshots con información sensible.
- Preferí sesiones aisladas y no reutilices perfiles personales sin confirmación explícita.
