#!/bin/bash
# Compatibility wrapper: delegates to the script in the lawofmessiah_translations submodule.

set -euo pipefail

SCRIPT_PATH="./data/lawofmessiah_translations/update_translation_files.sh"

if [[ ! -f "${SCRIPT_PATH}" ]]; then
    echo "ERROR: ${SCRIPT_PATH} not found"
    exit 1
fi

bash "${SCRIPT_PATH}" "$@"
