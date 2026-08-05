.PHONY: install lint format type test qa build bump release docs help

install: ## Instala las dependencias y los hooks locales
	@uv sync --all-groups
	@if command -v prek >/dev/null 2>&1; then prek install; else echo "Instalá prek con: uv tool install prek"; fi

lint: ## Ejecuta Ruff
	@uv run --group lint ruff check .

format: ## Formatea el código con Ruff
	@uv run --group lint ruff format .

type: ## Ejecuta el chequeo de tipos con Ty
	@uv run --group qa ty check

test: ## Ejecuta pytest con 100% de cobertura
	@uv run --group test pytest

qa: lint type test ## Ejecuta todos los controles de calidad

build: ## Construye el wheel
	@uv build

bump: ## Incrementa la versión menor del paquete
	@uv version --bump minor

release: ## Crea y publica una release desde main
	@test "$$(git branch --show-current)" = "main" || { echo "La release debe salir desde main" >&2; exit 1; }
	@git diff --quiet && git diff --cached --quiet || { echo "El árbol de trabajo debe estar limpio" >&2; exit 1; }
	@version=$$(uv version --short); \
	test -n "$$version"; \
	git rev-parse "$$version" >/dev/null 2>&1 && { echo "El tag $$version ya existe" >&2; exit 1; } || true; \
	git tag -a "$$version" -m "Release $$version"; \
	git push origin "$$version"; \
	gh release create "$$version" --generate-notes

docs: ## Compila la documentación Sphinx
	@uv run --group docs sphinx-build -d docs/_build/doctrees docs docs/_build/html -b html -W

help: ## Muestra los objetivos disponibles
	@grep -E '^[a-zA-Z_-]+:.*## ' Makefile | sed 's/:.*## /\t/'

.DEFAULT_GOAL := help
