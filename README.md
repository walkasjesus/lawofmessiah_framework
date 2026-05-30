# lawofmessiah_framework

This repository contains the Law of Messiah website and supporting Python tools.

It is a digital presentation of the book series _The Law of Messiah - Torah from a New Covenant Perspective_ by Michael Rudolph and Daniel C. Juster.

## Main components

- `lawofmessiah_website/`: Django website project
- `bible_lib/`: library for Bible API access and verse retrieval helpers
- `import_tool/`: import utilities for commandments, lessons, and Law of Messiah data
- `translate_tool/`: translation helper package

## Quick start (website)

1. Install dependencies and create a virtual environment

   ```bash
   ./lawofmessiah_website/install.sh
   ```

2. Create local Django settings file

   ```bash
   cp ./lawofmessiah_website/lawofmessiah_website/settings.py.example ./lawofmessiah_website/lawofmessiah_website/settings.py
   ```

3. Apply migrations / initialize database

   ```bash
   ./lawofmessiah_website/update_database.sh
   ```

4. Import Law of Messiah content

   ```bash
   ./lawofmessiah_website/IMPORT.sh
   ```

5. (Optional) create admin user

   ```bash
   cp ./lawofmessiah_website/account_app/management/commands/import_users.py.example ./lawofmessiah_website/account_app/management/commands/import_users.py
   ./lawofmessiah_website/create_admin_user.sh
   ```

6. Run the server

   ```bash
   ./lawofmessiah_website/run_server.sh
   ```

Then open `http://localhost:8000`.

## Common website scripts

- `./lawofmessiah_website/make_migration.sh`: create Django migrations
- `./lawofmessiah_website/update_database.sh`: apply migrations
- `./lawofmessiah_website/run_tests.sh`: run Django tests
- `./lawofmessiah_website/update_translation_files.sh`: regenerate translation files
- `./lawofmessiah_website/cache_bible_translation.sh`: cache Bible API responses
- `./lawofmessiah_website/clear_all_caches.sh`: clear application caches

## Project layout details

- `lawofmessiah_website/lawofmessiah_website/`: Django settings, middleware, URL config, WSGI
- `lawofmessiah_website/lawofmessiah_app/`: main Law of Messiah app (views, templates, models)
- `lawofmessiah_website/account_app/`: account and auth-related app
- `lawofmessiah_website/commandments_app/`: commandments domain models
- `lawofmessiah_website/data/lawofmessiah/`: source/import data files

## Notes

- This repository includes helper scripts intended to be run from the repository root.
- Some data and tests may depend on external Bible API access.

## Related repositories

- Law of Messiah source data: https://github.com/walkasjesus/LawofMessiah
- Translation repository: https://github.com/walkasjesus/walkasjesus_translations
