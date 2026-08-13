#!/bin/bash
#
# Generate and update project translation files.
#
# Scope:
# - Dutch only (nl)
# - Regular project/template strings only
# - Excludes data/lawofmessiah and data/lawofmessiah_translations
#
# This script is for the website's standard page translations,
# including the main Django templates and the author/legalism pages.
# It does not manage the Law of Messiah YAML-derived data strings.

APPROVE_FUZZY="false"
for arg in "$@"; do
    case "$arg" in
        --approve-fuzzy|--approve-fuzzy=yes|--approve-fuzzy=true)
            APPROVE_FUZZY="true"
            ;;
        --approve-fuzzy=no|--approve-fuzzy=false)
            APPROVE_FUZZY="false"
            ;;
    esac
done

export APPROVE_FUZZY

if [[ -f ./venv/Scripts/activate ]]; then
	source ./venv/Scripts/activate
elif [[ -f ./venv/bin/activate ]]; then 
	source ./venv/bin/activate
elif [[ -f ./.venv/bin/activate ]]; then
	source ./.venv/bin/activate
elif [[ -f ../venv/bin/activate ]]; then
	source ../venv/bin/activate
elif [[ -f ../.venv/bin/activate ]]; then
	source ../.venv/bin/activate
else
	echo "ERROR: cannot find environment binary"
	exit 1
fi

# If Linux based servers. This is the preferred Operating System.
if which tee > /dev/null 2>&1 && which date > /dev/null 2>&1; then
	today=$(date +%Y%m%d)
	start=$(date '+%Y-%m-%d %H:%M:%S')
	log=log/translation.${today}.log
	
	echo "INFO: ${start} - Start translating files" | tee -a ${log}
	echo "Adding new Dutch static-project texts to the .po files." | tee -a ${log}
	python3 - <<'PY' | tee -a ${log}
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lawofmessiah_website.settings')
from django.core.management.commands.makemessages import Command

cmd = Command()
cmd.run_from_argv([
	'manage.py',
	'makemessages',
	'-l', 'nl',
	'--extension=html,py',
	'--ignore=venv',
	'--ignore=data/lawofmessiah/*',
	'--ignore=data/lawofmessiah_translations/*',
	'--ignore=lawofmessiah_app/templates/authors/daniel_juster.html',
	'--ignore=lawofmessiah_app/templates/authors/michael_rudolph.html',
	'--ignore=lawofmessiah_app/templates/pages/legalism.html',
	'--ignore=static/*',
])
PY
	python3 - <<'PY' | tee -a ${log}
import os
from pathlib import Path
import polib

po_path = Path('translations/locale/nl/LC_MESSAGES/django.po')
if po_path.exists():
    po = polib.pofile(str(po_path))
    keep = []
    exclude = {
        'lawofmessiah_app/templates/authors/daniel_juster.html',
        'lawofmessiah_app/templates/authors/michael_rudolph.html',
        'lawofmessiah_app/templates/pages/legalism.html',
    }
    for entry in po:
        refs = [ref for ref, _line in entry.occurrences]
        if any(ref in exclude for ref in refs):
            continue
        if os.environ.get('APPROVE_FUZZY', 'false').lower() in {'1', 'true', 'yes'} and 'fuzzy' in entry.flags:
            entry.flags = [flag for flag in entry.flags if flag != 'fuzzy']
        keep.append(entry)
    po = polib.POFile()
    po.metadata = {
        'Project-Id-Version': 'Law of Messiah Website',
        'Language': 'nl',
        'MIME-Version': '1.0',
        'Content-Type': 'text/plain; charset=UTF-8',
        'Content-Transfer-Encoding': '8bit',
        'Plural-Forms': 'nplurals=2; plural=(n != 1);',
    }
    po.extend(keep)
    po.save(str(po_path))
PY
	#python3 -m django makemessages -l fr --extension=html --ignore=venv --ignore=data/* --ignore=static/* | tee -a ${log}
	#python3 -m django makemessages -l de --extension=html --ignore=venv --ignore=data/* --ignore=static/* | tee -a ${log}

	echo "Auto translating new untranslated Dutch entries while keeping existing translations intact." | tee -a ${log}
	if [[ "${APPROVE_FUZZY}" == "true" ]]; then
		python3 manage.py auto_translate --approve-fuzzy | tee -a ${log}
	else
		python3 manage.py auto_translate | tee -a ${log}
	fi

	echo "Compiling Dutch project .po files." | tee -a ${log}
	python3 -m django compilemessages -l nl -i venv -i data/lawofmessiah -i data/lawofmessiah_translations | tee -a ${log}

	python3 - <<'PY' | tee -a ${log}
import os
from pathlib import Path

po_path = Path('translations/locale/nl/LC_MESSAGES/django.po')
if po_path.exists() and os.environ.get('APPROVE_FUZZY', 'false').lower() in {'1', 'true', 'yes'}:
    import polib
    po = polib.pofile(str(po_path))
    for entry in po:
        if 'fuzzy' in entry.flags:
            entry.flags = [flag for flag in entry.flags if flag != 'fuzzy']
    po.save(str(po_path))
PY

	end=$(date '+%Y-%m-%d %H:%M:%S')
	echo "INFO: ${end} - Ended translating files" | tee -a ${log}

# Other Operating Systems like Windows
else
	echo "INFO: Start translating files"
	echo "Adding new Dutch static-project texts to the .po files."
	python3 - <<'PY'
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lawofmessiah_website.settings')
from django.core.management.commands.makemessages import Command

cmd = Command()
cmd.run_from_argv([
	'manage.py',
	'makemessages',
	'-l', 'nl',
	'--extension=html,py',
	'--ignore=venv',
	'--ignore=data/lawofmessiah/*',
	'--ignore=data/lawofmessiah_translations/*',
	'--ignore=lawofmessiah_app/templates/authors/daniel_juster.html',
	'--ignore=lawofmessiah_app/templates/authors/michael_rudolph.html',
	'--ignore=lawofmessiah_app/templates/pages/legalism.html',
	'--ignore=static/*',
])
PY
	#python3 -m django makemessages -l fr --extension=html --ignore=venv --ignore=data/* --ignore=static/*
	#python3 -m django makemessages -l de --extension=html --ignore=venv --ignore=data/* --ignore=static/*

	echo "Auto translating new untranslated Dutch entries while keeping existing translations intact."
	python3 manage.py auto_translate

	echo "Compiling Dutch project .po files."
	python3 -m django compilemessages -l nl -i venv -i data/lawofmessiah -i data/lawofmessiah_translations

	echo "INFO: Ended translating files"
fi