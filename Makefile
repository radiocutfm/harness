.PHONY: release

release:
	@test -n "$(VERSION)" || (echo "Uso: make release VERSION=0.1.0"; exit 1)
	@git diff --quiet
	@git diff --cached --quiet
	@git tag "$(VERSION)"
	@git push origin "$(VERSION)"
	@gh release create "$(VERSION)" --generate-notes
