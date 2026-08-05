"""Configuración de Sphinx para la documentación de Fierro Harness."""

import os
from pathlib import Path

project = "Fierro Harness"
copyright = "2026, Lambda SRL"
author = "Lambda SRL"
language = "es"
version = "main"
release = version

extensions = ["myst_parser", "sphinx.ext.intersphinx", "sphinx_design", "sphinxcontrib.mermaid"]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

myst_enable_extensions = ["colon_fence", "deflist", "linkify"]
myst_heading_anchors = 3
myst_url_schemes = {
    "http": None,
    "https": None,
    "gh": {
        "url": "https://github.com/radiocutfm/harness/blob/main/{{path}}",
        "title": "",
        "classes": ["github"],
    },
}

docs_dir = Path(__file__).parent
fierro_inventory = os.environ.get("INTERSPHINX_FIERRO_INVENTORY", docs_dir / "_intersphinx" / "fierro.inv")
intersphinx_mapping = {"fierro": ("https://docs.fierro.com.ar/", str(fierro_inventory))}

html_theme = "sphinx_book_theme"
html_title = project
html_theme_options = {
    "repository_url": "https://github.com/radiocutfm/harness",
    "use_repository_button": True,
    "use_issues_button": True,
    "home_page_in_toc": True,
}
