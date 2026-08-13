import os

from django.apps import apps
from django.core.management import BaseCommand
from translate_tool import PoTranslator

from lawofmessiah_website.settings import BASE_DIR, LANGUAGES, LOCALE_PATHS


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--approve-fuzzy',
            action='store_true',
            default=False,
            help='Remove fuzzy flags from translated entries after auto-translation.',
        )

    def handle(self, *args, **options):
        approve_fuzzy = options.get('approve_fuzzy', False)
        languages = [code for code, name in LANGUAGES]

        translator = PoTranslator()

        for language in languages:
            if language != 'en':
                for file_path in self._po_file_paths(language):
                    self.stdout.write(f'Auto-translating {file_path}')
                    translator.translate(file_path, 'en', language)
                    if approve_fuzzy:
                        self._approve_fuzzy(file_path)

    def _approve_fuzzy(self, file_path):
        try:
            import polib
        except ImportError:
            return

        po = polib.pofile(file_path)
        for entry in po:
            if 'fuzzy' in entry.flags:
                entry.flags = [flag for flag in entry.flags if flag != 'fuzzy']
        po.save(file_path)

    def _po_file_paths(self, language):
        seen = set()
        base_dir = os.path.abspath(BASE_DIR)
        roots = list(LOCALE_PATHS)
        roots.extend(os.path.join(app_config.path, 'locale') for app_config in apps.get_app_configs())

        for root in roots:
            file_path = os.path.join(root, language, 'LC_MESSAGES', 'django.po')
            normalized = os.path.abspath(file_path)
            if not normalized.startswith(base_dir + os.sep):
                continue
            if normalized in seen or not os.path.exists(normalized):
                continue
            seen.add(normalized)
            yield normalized
