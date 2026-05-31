#!/bin/bash
#
# Auto-translate Law of Messiah data translations.
#
# Usage:
#   bash auto_translate_files.sh [quick|all] [run|count]
#
# Defaults:
#   profile=quick
#   mode=run

set -euo pipefail

PROFILE="${1:-quick}"
MODE="${2:-run}"

if [[ "${PROFILE}" != "quick" && "${PROFILE}" != "all" ]]; then
    echo "ERROR: unsupported profile '${PROFILE}'. Use 'quick' or 'all'."
    exit 1
fi

if [[ "${MODE}" != "run" && "${MODE}" != "count" ]]; then
    echo "ERROR: unsupported mode '${MODE}'. Use 'run' or 'count'."
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WEBSITE_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
TARGET_PO="${WEBSITE_DIR}/data/lawofmessiah_translations/locale/nl/LC_MESSAGES/django.po"

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
log="${WEBSITE_DIR}/log/lawofmessiah-data-autotranslate.${today}.log"

echo "INFO: ${start} - Start auto-translating Law of Messiah data translations" | tee -a "${log}"
echo "INFO: profile=${PROFILE}, mode=${MODE}" | tee -a "${log}"

# Refresh the PO entries from source YAML before counting/translating.
cd "${WEBSITE_DIR}"
bash "${SCRIPT_DIR}/update_translation_files.sh" "${PROFILE}" | tee -a "${log}"

if [[ "${MODE}" == "count" ]]; then
    python3 - <<'PY' | tee -a "${log}"
from pathlib import Path
import polib

po_path = Path('data/lawofmessiah_translations/locale/nl/LC_MESSAGES/django.po')
po = polib.pofile(str(po_path))
print(f"total_entries={len(po)}")
print(f"untranslated_entries={len(po.untranslated_entries())}")
print(f"fuzzy_entries={sum(1 for e in po if 'fuzzy' in e.flags)}")
PY
    end=$(date '+%Y-%m-%d %H:%M:%S')
    echo "INFO: ${end} - Count mode complete" | tee -a "${log}"
    exit 0
fi

python3 - <<'PY' | tee -a "${log}"
import os
import polib
from translate_tool import PoTranslator

po_file = os.path.join('data', 'lawofmessiah_translations', 'locale', 'nl', 'LC_MESSAGES', 'django.po')
po_before = polib.pofile(po_file)
untranslated_before = len(po_before.untranslated_entries())
print(f'untranslated_before={untranslated_before}')

translator = PoTranslator()
translator.translate(po_file, 'en', 'nl')

po_after = polib.pofile(po_file)
untranslated_after = len(po_after.untranslated_entries())
fuzzy_after = sum(1 for entry in po_after if 'fuzzy' in entry.flags)
print(f'untranslated_after={untranslated_after}')
print(f'fuzzy_after={fuzzy_after}')
PY

echo "Compiling Dutch messages for data translations." | tee -a "${log}"
python3 -m django compilemessages -l nl -i venv | tee -a "${log}"

end=$(date '+%Y-%m-%d %H:%M:%S')
echo "INFO: ${end} - Ended auto-translating Law of Messiah data translations" | tee -a "${log}"
