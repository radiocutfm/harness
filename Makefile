.PHONY: install lint format test qa build bump release help

install: ## Install development dependencies
	@uv sync

lint: ## Run Ruff checks
	@uv run ruff check .

format: ## Format Python files
	@uv run ruff format .

test: ## Run tests
	@uv run pytest -q

qa: lint test ## Run local quality checks

build: ## Build the wheel
	@uv build

 bump: ## Bump the patch version in pyproject.toml
	@uv version --bump patch

release: ## Create a GitHub release using the pyproject.toml version
	@git diff --quiet
	@git diff --cached --quiet
	@version=$$(uv version --short); \
	test -n "$$version"; \
	git diff --quiet "$$(git rev-list -n 1 HEAD)" -- pyproject.toml; \
	git rev-parse "$$version" >/dev/null 2>&1 && { echo "El tag $$version ya existe" >&2; exit 1; } || true; \
	git tag "$$version"; \
	git push origin "$$version"; \
	gh release create "$$version" --generate-notes

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*## ' Makefile | sed 's/:.*## /\t/'
