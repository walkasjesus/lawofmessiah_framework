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
	'--ignore=static/*',
])
PY
	#python3 -m django makemessages -l fr --extension=html --ignore=venv --ignore=data/* --ignore=static/* | tee -a ${log}
	#python3 -m django makemessages -l de --extension=html --ignore=venv --ignore=data/* --ignore=static/* | tee -a ${log}

	echo "Auto translating new untranslated Dutch entries while keeping existing translations intact." | tee -a ${log}
	python3 manage.py auto_translate | tee -a ${log}

	echo "Compiling Dutch project .po files." | tee -a ${log}
	python3 -m django compilemessages -l nl -i venv -i data/lawofmessiah -i data/lawofmessiah_translations | tee -a ${log}

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