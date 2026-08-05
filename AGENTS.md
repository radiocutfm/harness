# Fierro Harness

Repositorio: https://github.com/radiocutfm/harness

## Alcance

`fierro-harness` instala skills globales y configura el entorno inicial de
OpenCode. El código del paquete vive en `src/fierro_harness/`, los recursos
bundleados en `src/fierro_harness/resources/`, los tests en `tests/` y los
bootstrap de distribución en `bootstrap/`.

## Comandos

- `make install`: instala todas las dependencias y los hooks de `prek`.
- `make lint`, `make format`, `make type`, `make test`, `make qa` y `make build`:
  validaciones locales habituales.
- `make docs`: compila la documentación local con Sphinx.
- `make bump`: incrementa la versión menor.
- `make release`: único flujo para publicar una versión. Debe ejecutarse desde
  `main`, con el árbol limpio y luego de que el bump esté mergeado.

## Python

- Usar Python 3.14 y administrar dependencias con `uv`; modificar dependencias
  mediante `uv add` o `uv remove`.
- Mantener anotaciones explícitas con genéricos nativos y uniones `|`.
- Usar `pathlib` para rutas y preferir guard clauses y código plano.
- Ejecutar `make qa` después de cambios de código. Las pruebas deben mantener
  100% de cobertura de `src/fierro_harness` sin excluir código de producción.

## Documentación federada

- `docs/` se valida localmente y se publica dentro de https://docs.fierro.com.ar
  como una fuente externa de Fierro.
- Los enlaces a documentación central usan el namespace
  `{external+fierro:doc}` y se validan con `docs/_intersphinx/fierro.inv`.
- Los cambios mergeados en `main` que afectan documentación disparan la
  reconstrucción central mediante la GitHub App `cruz-lambda`.

## Git y GitHub

- Trabajar en una rama por cambio y usar `gh` para issues y PRs.
- No hacer commits, pushes ni abrir PRs sin pedido explícito.
- Los PRs deben resumir el cambio y las validaciones ejecutadas.
- El texto commitable y las interacciones con GitHub se escriben en español
  rioplatense simple.
