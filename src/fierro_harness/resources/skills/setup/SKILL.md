---
name: setup
description: Prepara el entorno instalando o verificando las herramientas requeridas por las skills habilitadas.
compatibility: opencode
metadata:
  audience: employees
  owner: fierro
---

## Propósito

Usá esta skill cuando el usuario quiera preparar el entorno completo o comprobar qué integraciones puede utilizar. Consultá `fierro-harness setup --json` para conocer el estado actual.

## Reglas

- Mostrá antes de instalar la lista de herramientas, versiones, origen y motivo.
- Pedí confirmación antes de instalar o modificar componentes.
- No instales herramientas sólo porque una skill esté disponible; instalá las que el usuario seleccione o todas las habilitadas cuando lo pida explícitamente.
- Reutilizá los procedimientos de instalación definidos por cada skill.
- Verificá plataforma, versión, autenticación y salida JSON cuando corresponda.
- No solicites ni guardes tokens en archivos del repositorio.
- Si una herramienta no tiene instalador confiable, informá el bloqueo y no improvises una descarga.

## Instalación explícita

- Mostrá primero el plan con `fierro-harness setup --install <herramienta>`.
- Sólo después de que el usuario confirme, ejecutá `fierro-harness setup --install <herramienta> --yes`.
- Para preparar todas las herramientas habilitadas, usá `--install all`; la misma confirmación aplica.
- Usá `--dry-run` junto con `--yes` para validar el plan sin modificar el equipo.
- El comando sólo instala herramientas seleccionadas explícitamente. No instala una integración al cargar esta skill.

## Resultado

Informá qué herramientas ya estaban instaladas, cuáles se instalaron, cuáles fallaron y qué acción manual queda pendiente. No informes secretos, rutas de credenciales ni contenido de cuentas.
