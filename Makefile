.PHONY: install lint format test qa build release help

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

release: ## Create a GitHub release from pyproject.toml version
	@git diff --quiet
	@git diff --cached --quiet
	@version=$$(uv version --short); \
	git tag "$$version"; \
	git push origin "$$version"; \
	gh release create "$$version" --generate-notes

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*## ' Makefile | sed 's/:.*## /\t/'
