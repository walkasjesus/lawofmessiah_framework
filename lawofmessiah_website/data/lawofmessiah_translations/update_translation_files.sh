#!/bin/bash
#
# Update Dutch translations for Law of Messiah data translations repository.
#
# Scope:
# - Dutch only (nl)
# - Target file: locale/nl/LC_MESSAGES/django.po
# - Source extraction directly from data/lawofmessiah YAML files

set -euo pipefail

PROFILE="${1:-all}"
if [[ "${PROFILE}" != "all" && "${PROFILE}" != "quick" ]]; then
    echo "ERROR: unsupported profile '${PROFILE}'. Use 'all' or 'quick'."
    exit 1
fi

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
echo "INFO: extraction profile=${PROFILE}" | tee -a "${log}"

export WEBSITE_DIR
export LOM_TRANSLATION_PROFILE="${PROFILE}"

python3 - <<'PY' | tee -a "${log}"
import ast
import os
import re
from pathlib import Path

import yaml


def decode_po_string(raw_line):
    raw_line = raw_line.strip()
    if not raw_line.startswith('"'):
        return ''
    try:
        return ast.literal_eval(raw_line)
    except Exception:
        return ''


def parse_po(path):
    if not path.exists():
        return '', {}

    lines = path.read_text(encoding='utf-8').splitlines()
    lines.append('')

    entries = {}
    refs = []
    msgid_parts = []
    msgstr_parts = []
    state = None
    header_msgstr = ''

    def flush_entry():
        nonlocal refs, msgid_parts, msgstr_parts, state, header_msgstr
        if not msgid_parts and not msgstr_parts:
            refs = []
            state = None
            return

        msgid = ''.join(msgid_parts)
        msgstr = ''.join(msgstr_parts)
        if msgid == '':
            header_msgstr = msgstr
        else:
            entries[msgid] = {'msgstr': msgstr, 'refs': sorted(set(refs))}

        refs = []
        msgid_parts = []
        msgstr_parts = []
        state = None

    for line in lines:
        stripped = line.strip()

        if not stripped:
            flush_entry()
            continue

        if line.startswith('#:'):
            refs.extend(line[2:].strip().split())
            continue

        if line.startswith('msgid '):
            state = 'msgid'
            msgid_parts = [decode_po_string(line[line.find('"'):])]
            continue

        if line.startswith('msgstr '):
            state = 'msgstr'
            msgstr_parts = [decode_po_string(line[line.find('"'):])]
            continue

        if stripped.startswith('"'):
            if state == 'msgid':
                msgid_parts.append(decode_po_string(stripped))
            elif state == 'msgstr':
                msgstr_parts.append(decode_po_string(stripped))

    return header_msgstr, entries


def po_escape(value):
    return value.replace('\\', '\\\\').replace('"', '\\"')


def format_po_string(keyword, value):
    if value is None:
        value = ''
    if '\n' not in value:
        return [f'{keyword} "{po_escape(value)}"']

    out = [f'{keyword} ""']
    parts = value.split('\n')
    last = len(parts) - 1
    for i, part in enumerate(parts):
        suffix = '\\n' if i < last else ''
        out.append(f'"{po_escape(part)}{suffix}"')
    return out


def is_translatable(text):
    if not isinstance(text, str):
        return False
    stripped = text.strip()
    if not stripped:
        return False
    if stripped.lower() in {'none', 'null', 'n/a', '-'}:
        return False
    letter_count = len(re.findall(r'[A-Za-z]', stripped))
    return letter_count >= 2


website_root = Path(os.environ['WEBSITE_DIR'])
profile = os.environ.get('LOM_TRANSLATION_PROFILE', 'all').strip().lower() or 'all'
source_po = website_root / 'translations' / 'locale' / 'nl' / 'LC_MESSAGES' / 'django.po'
target_po = website_root / 'data' / 'lawofmessiah_translations' / 'locale' / 'nl' / 'LC_MESSAGES' / 'django.po'
data_files = [
    website_root / 'data' / 'lawofmessiah' / 'Law_of_Messiah_ot.yaml',
    website_root / 'data' / 'lawofmessiah' / 'Law_of_Messiah_nt.yaml',
]

target_po.parent.mkdir(parents=True, exist_ok=True)

target_header, target_entries = parse_po(target_po)
source_header, source_entries = parse_po(source_po)

default_header = (
    'Project-Id-Version: Lawofmessiah_Translations\n'
    'Report-Msgid-Bugs-To: \n'
    'POT-Creation-Date: 2026-01-01 00:00+0000\n'
    'PO-Revision-Date: 2026-01-01 00:00+0000\n'
    'Last-Translator: <>\n'
    'Language-Team: Dutch\n'
    'Language: nl\n'
    'MIME-Version: 1.0\n'
    'Content-Type: text/plain; charset=UTF-8\n'
    'Content-Transfer-Encoding: 8bit\n'
    'Plural-Forms: nplurals=2; plural=(n != 1);\n'
)
header_msgstr = source_header or default_header
header_msgstr = header_msgstr.replace('\\n', '\n')

header_lines = [line for line in header_msgstr.splitlines() if line.strip()]
header_lines = [line for line in header_lines if not line.startswith('Language:')]
header_lines.append('Language: nl')
header_msgstr = '\n'.join(header_lines) + '\n'

source_msgstr_map = {
    msgid: payload['msgstr']
    for msgid, payload in source_entries.items()
    if payload.get('msgstr', '').strip()
}
existing_msgstr_map = {
    msgid: payload['msgstr']
    for msgid, payload in target_entries.items()
    if payload.get('msgstr', '').strip()
}

extract_map = {}


def add_msgid(msgid, ref):
    if not is_translatable(msgid):
        return
    refs = extract_map.setdefault(msgid, set())
    refs.add(ref)


for data_file in data_files:
    if not data_file.exists():
        continue

    parsed = yaml.safe_load(data_file.read_text(encoding='utf-8')) or []
    if not isinstance(parsed, list):
        continue

    for index, item in enumerate(parsed, start=1):
        if not isinstance(item, dict):
            continue

        item_id = str(item.get('id', '')).strip() or f'item{index}'

        common_keys = (
            'title',
            'commandment',
            'category',
            'commandment_type',
            'commandment_form',
        )
        extended_keys = (
            'commentary_rudolph',
            'commentary_juster',
            'classical_commentators',
            'copyright',
        )
        selected_keys = common_keys if profile == 'quick' else common_keys + extended_keys

        for key in selected_keys:
            value = item.get(key)
            if isinstance(value, str):
                add_msgid(value, f'data/lawofmessiah/{data_file.name}:{item_id}.{key}')

        subtitles = item.get('commandment_subtitles') or []
        if isinstance(subtitles, list):
            for sub_index, value in enumerate(subtitles, start=1):
                if isinstance(value, str):
                    add_msgid(value, f'data/lawofmessiah/{data_file.name}:{item_id}.commandment_subtitles[{sub_index}]')

        for related_key in ('commandments_related_ot', 'commandments_related_nt'):
            related_items = item.get(related_key) or []
            if not isinstance(related_items, list):
                continue
            for rel_index, rel_item in enumerate(related_items, start=1):
                if isinstance(rel_item, dict):
                    title = rel_item.get('title')
                    if isinstance(title, str):
                        add_msgid(title, f'data/lawofmessiah/{data_file.name}:{item_id}.{related_key}[{rel_index}].title')

lines = []
lines.extend([
    '# SOME DESCRIPTIVE TITLE.',
    '# Copyright (C) YEAR THE PACKAGE\'S COPYRIGHT HOLDER',
    '# This file is distributed under the same license as the PACKAGE package.',
    '# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.',
    '#',
])
lines.extend(format_po_string('msgid', ''))
lines.extend(format_po_string('msgstr', header_msgstr))

written_entries = 0
for msgid in sorted(extract_map.keys()):
    refs = sorted(extract_map[msgid])
    msgstr = existing_msgstr_map.get(msgid, source_msgstr_map.get(msgid, ''))

    lines.append('')
    lines.append(f"#: {' '.join(refs)}")
    lines.extend(format_po_string('msgid', msgid))
    lines.extend(format_po_string('msgstr', msgstr))
    written_entries += 1

target_po.write_text('\n'.join(lines).rstrip() + '\n', encoding='utf-8')

pretranslated = sum(1 for msgid in extract_map.keys() if existing_msgstr_map.get(msgid, source_msgstr_map.get(msgid, '')).strip())
print(f'profile={profile}')
print(f'data_entries_extracted={len(extract_map)}')
print(f'data_entries_pretranslated={pretranslated}')
print(f'target_entries_written={written_entries}')
print(f'target={target_po}')
PY

echo "Compiling Dutch messages (including data translation locale path if configured)." | tee -a "${log}"
cd "${WEBSITE_DIR}"
python3 -m django compilemessages -l nl -i venv | tee -a "${log}"

end=$(date '+%Y-%m-%d %H:%M:%S')
echo "INFO: ${end} - Ended updating Law of Messiah data translations" | tee -a "${log}"
