# Law of Messiah data translations

This directory is the canonical place for translations generated from the structured Law of Messiah data files in `data/lawofmessiah`.

Purpose:
- Store translations for textual content extracted from the Law of Messiah YAML data.
- Keep these separate from the website's static/template translations.
- This is the translation source for imported content and commandment-related data, not for the normal page templates.

Language scope:
- Dutch (`nl`) only.

Active usage:
- Used by Django via `LOCALE_PATHS` alongside the main project locale path.
- This directory should be updated with:
  `./update_lawofmessiah_data_translation_files.sh`

Included content:
- All translatable text extracted from `data/lawofmessiah/*.yaml`
- Commandment and data-source strings that come from the Law of Messiah dataset
- The author pages that belong to the Law of Messiah content set:
  - `lawofmessiah_app/templates/authors/daniel_juster.html`
  - `lawofmessiah_app/templates/authors/michael_rudolph.html`
  - `lawofmessiah_app/templates/pages/legalism.html`

Excluded content:
- The regular website templates and page content in `lawofmessiah_app/templates` that are not part of the Law of Messiah data set
- The auto-translated commentary content for Rudolph/Juster, which is kept separate and is not part of this locale workflow

Expected layout:
- `locale/nl/LC_MESSAGES/django.po`

Note:
- `translate_tool` is a translation helper package used to automate translations; it is not itself the active locale directory used by Django.
