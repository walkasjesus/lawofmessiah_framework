# Project translations

This directory is the canonical place for the website's regular Django/template translations.

Purpose:
- Store translations for the standard application UI and page templates.
- Keep these separate from structured Law of Messiah data translations stored in `data/lawofmessiah_translations`.
- This is the location for the normal website content and project-level text strings.

Language scope:
- Dutch (`nl`) only.

Active usage:
- Used by Django via `LOCALE_PATHS` for the main project translation files.
- This directory is updated with:
  `./update_translation_files.sh`

Included content:
- The main website templates and pages under `lawofmessiah_app/templates` that are not part of the Law of Messiah data set
- Other project-specific strings that are not extracted from `data/lawofmessiah/*.yaml`

Excluded content:
- The YAML-derived Law of Messiah content from `data/lawofmessiah`
- The data-backed author pages:
  - `lawofmessiah_app/templates/authors/daniel_juster.html`
  - `lawofmessiah_app/templates/authors/michael_rudolph.html`
  - `lawofmessiah_app/templates/pages/legalism.html`
- The auto-translated commentary content for Rudolph/Juster, which is kept separate from this project locale workflow

These three author pages are intentionally managed with the data-translation workflow, not with the main project translation workflow.

Expected layout:
- `locale/nl/LC_MESSAGES/django.po`

Workflow:
- Run `./update_translation_files.sh` for the project/page translations.
- Run `./update_lawofmessiah_data_translation_files.sh` for the data-derived translations.

This split keeps the normal website strings and the data-backed content clearly separated and easy to manage.
