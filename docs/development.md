# Desarrollo

El proyecto usa Python 3.14 y `uv`.

```sh
make install
prek install
make qa
make docs
```

`make install` sincroniza todos los grupos de dependencias. `prek install`
habilita los hooks locales; `make qa` ejecuta Ruff, Ty y pytest con cobertura
obligatoria del 100% sobre `src/fierro_harness`.

Los cambios de código deben mantener el conjunto amplio de reglas Ruff definido
en `pyproject.toml`, pasar Ty y agregar tests para cada rama nueva. Para la
referencia general de desarrollo de Fierro, consultá la
[documentación de desarrollo](https://docs.fierro.com.ar/desarrollo-local.html)
y la [documentación federada](https://docs.fierro.com.ar/sobre-la-doc.html#documentacion-federada).

Las releases se publican únicamente con `make release` desde `main`, con el
árbol limpio y la versión ya mergeada.
