---
title: "Build the MegaDetector Docs Site (MkDocs)"
description: "How to build and deploy the MegaDetector MkDocs documentation site locally and to GitHub Pages."
tags:
  - MegaDetector
  - documentation
  - MkDocs
  - developer guide
---

# Building the MkDocs Site

To build the MegaDetector docs site locally, follow these steps.


## 1. Install System Dependencies

Install Python and pipx via Homebrew (one-time setup):

```bash
brew bundle
```

Then install MkDocs and its plugins globally:

```bash
pipx install mkdocs-material --include-deps
pipx inject mkdocs-material pymdown-extensions mkdocstrings mkdocstrings-python
pipx ensurepath
```

Open a new terminal after running `pipx ensurepath` so the `mkdocs` command is on your PATH.


## 2. Build the Site

```bash
mkdocs build
```

This generates the static site in the `site/` directory.


## 3. Preview Locally

```bash
mkdocs serve
```

The site is available at `http://127.0.0.1:8000/`.


## 4. Deploy to GitHub Pages

Push any change to `docs/**`, `mkdocs.yml`, or `requirements.txt` on the `main` branch, GitHub Actions deploys automatically.

To deploy manually:

```bash
mkdocs gh-deploy --force
```


## Notes

- The `site/` directory is auto-generated and excluded from version control via `.gitignore`
- Documentation source files live in `docs/`
- Site config is in `mkdocs.yml` at the repo root
