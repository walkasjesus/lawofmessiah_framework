#!/bin/bash
# Compatibility wrapper: delegates to the script in the Law of Messiah data translation repository.
#
# Scope:
# - Dutch only (nl)
# - Structured Law of Messiah YAML content from data/lawofmessiah
# - The Law of Messiah content pages in the author section and legalism page
# - Used for data-derived translations, not for the regular website templates
#
# This script should be used for the content that lives under:
#   data/lawofmessiah_translations/
#   and for the Law of Messiah data pages:
#   lawofmessiah_app/templates/authors/daniel_juster.html
#   lawofmessiah_app/templates/authors/michael_rudolph.html
#   lawofmessiah_app/templates/pages/legalism.html
#
# The auto-translated commentaries for Rudolph/Juster remain outside this workflow.
# The regular project pages remain under:
#   translations/
#
set -euo pipefail

SCRIPT_PATH="./data/lawofmessiah_translations/update_translation_files.sh"

if [[ ! -f "${SCRIPT_PATH}" ]]; then
    echo "ERROR: ${SCRIPT_PATH} not found"
    exit 1
fi

bash "${SCRIPT_PATH}" "$@"
