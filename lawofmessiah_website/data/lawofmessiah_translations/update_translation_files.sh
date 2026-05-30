#!/bin/bash
#
# Update Dutch translations for Law of Messiah data translations repository.
#
# Scope:
# - Dutch only (nl)
# - Target file: locale/nl/LC_MESSAGES/django.po
# - Source extraction from website Dutch PO entries that reference data/lawofmessiah/*

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WEBSITE_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"

if [[ -f "${WEBSITE_DIR}/venv/Scripts/activate" ]]; then
    source "${WEBSITE_DIR}/venv/Scripts/activate"
elif [[ -f "${WEBSITE_DIR}/venv/bin/activate" ]]; then
    source "${WEBSITE_DIR}/venv/bin/activate"
elif [[ -f "${WEBSITE_DIR}/../venv/bin/activate" ]]; then
    source "${WEBSITE_DIR}/../venv/bin/activate"
else
    echo "ERROR: cannot find environment binary"
    exit 1
fi

mkdir -p "${WEBSITE_DIR}/log"

today=$(date +%Y%m%d)
start=$(date '+%Y-%m-%d %H:%M:%S')
log="${WEBSITE_DIR}/log/lawofmessiah-data-translation.${today}.log"

echo "INFO: ${start} - Start updating Law of Messiah data translations" | tee -a "${log}"

python3 - <<'PY' | tee -a "${log}"
from pathlib import Path

website_root = Path.cwd()
source_po = website_root / 'translations' / 'locale' / 'nl' / 'LC_MESSAGES' / 'django.po'
target_po = website_root / 'data' / 'lawofmessiah_translations' / 'locale' / 'nl' / 'LC_MESSAGES' / 'django.po'

target_po.parent.mkdir(parents=True, exist_ok=True)

if not target_po.exists():
    target_po.write_text(
        '# SOME DESCRIPTIVE TITLE.\n'
        '# Copyright (C) YEAR THE PACKAGE\'S COPYRIGHT HOLDER\n'
        '# This file is distributed under the same license as the PACKAGE package.\n'
        '# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.\n'
        '#\n'
        'msgid ""\n'
        'msgstr ""\n'
        '"Project-Id-Version: PACKAGE VERSION\\n"\n'
        '"Report-Msgid-Bugs-To: \\n"\n'
        '"POT-Creation-Date: 2026-01-01 00:00+0000\\n"\n'
        '"PO-Revision-Date: 2026-01-01 00:00+0000\\n"\n'
        '"Last-Translator: <>\\n"\n'
        '"Language-Team: LANGUAGE <LL@li.org>\\n"\n'
        '"Language: nl\\n"\n'
        '"MIME-Version: 1.0\\n"\n'
        '"Content-Type: text/plain; charset=UTF-8\\n"\n'
        '"Content-Transfer-Encoding: 8bit\\n"\n'
        '"Plural-Forms: nplurals=2; plural=(n != 1);\\n"\n',
        encoding='utf-8',
    )

lines = source_po.read_text(encoding='utf-8').splitlines()
entries = []
cur = []
has_msgid = False

for line in lines:
    if line.startswith('msgid ') and has_msgid:
        entries.append(cur)
        cur = []
        has_msgid = False
    cur.append(line)
    if line.startswith('msgid '):
        has_msgid = True

if cur:
    entries.append(cur)

header = None
selected = []

for entry in entries:
    text = '\n'.join(entry)
    if header is None and 'msgid ""' in text:
        header = entry
        continue
    refs = [ln for ln in entry if ln.startswith('#:')]
    if any('data/lawofmessiah/' in ref for ref in refs):
        selected.append(entry)

if header is None:
    raise SystemExit('ERROR: Could not find PO header in source file')

if selected:
    output = '\n\n'.join(['\n'.join(header).strip()] + ['\n'.join(e).strip() for e in selected]).rstrip() + '\n'
    target_po.write_text(output, encoding='utf-8')

print(f'source_entries_total={len(entries)-1}')
print(f'data_entries_selected={len(selected)}')
print(f'target={target_po}')
PY

echo "Compiling Dutch messages (including data translation locale path if configured)." | tee -a "${log}"
cd "${WEBSITE_DIR}"
python3 -m django compilemessages -l nl -i venv | tee -a "${log}"

end=$(date '+%Y-%m-%d %H:%M:%S')
echo "INFO: ${end} - Ended updating Law of Messiah data translations" | tee -a "${log}"
