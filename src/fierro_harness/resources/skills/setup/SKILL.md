---
name: setup
description: Prepara el entorno instalando o verificando las herramientas requeridas por las skills habilitadas.
compatibility: opencode
metadata:
  audience: employees
  owner: fierro
---

## Propósito

Usá esta skill cuando el usuario quiera preparar el entorno completo o comprobar qué integraciones puede utilizar. Debe reunir las herramientas declaradas por las skills habilitadas y ejecutar su instalación o verificación mediante el instalador del harness.

## Reglas

- Mostrá antes de instalar la lista de herramientas, versiones, origen y motivo.
- Pedí confirmación antes de instalar o modificar componentes.
- No instales herramientas sólo porque una skill esté disponible; instalá las que el usuario seleccione o todas las habilitadas cuando lo pida explícitamente.
- Reutilizá los procedimientos de instalación definidos por cada skill.
- Verificá plataforma, versión, autenticación y salida JSON cuando corresponda.
- No solicites ni guardes tokens en archivos del repositorio.
- Si una herramienta no tiene instalador confiable, informá el bloqueo y no improvises una descarga.

## Resultado

Informá qué herramientas ya estaban instaladas, cuáles se instalaron, cuáles fallaron y qué acción manual queda pendiente. No informes secretos, rutas de credenciales ni contenido de cuentas.
