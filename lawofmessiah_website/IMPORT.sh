#!/bin/bash
#
# This script imports Law of Messiah and Maimonides data into the database.

if [[ -f ./venv/Scripts/activate ]]; then
	source ./venv/Scripts/activate
elif [[ -f ./venv/bin/activate ]]; then 
	source ./venv/bin/activate
else
	echo "WARNING: cannot find environment binary, using system python"
fi

# If Linux based servers. This is the preferred Operating System.
if which tee > /dev/null 2>&1 && which date > /dev/null 2>&1; then
	DELETE_DATABASE=false
	QUIET=false
	lom_source=data/lawofmessiah/filter_output/collected_ids_titles.yaml
	today=$(date +%Y%m%d)
	start=$(date '+%Y-%m-%d %H:%M:%S')
	log=log/commandments.${today}.log
	mkdir -p log
	cur=$(dirname "$(realpath $0)")
	database=jcdatabase
	rsakey=/home/jesuscommandments/.ssh/id_rsa

	# Parse some options
	while getopts 'dq' OPTION; do
	case "$OPTION" in
		d)
		DELETE_DATABASE=true
		;;
		q)
		QUIET=true
		;;
		*)
		echo "Script usage: $(basename $0) [-d] [-q]" >&2
		echo "   -d will DELETE app data from the current database and re-import source data!"
		echo "   -q will run this script quiet, without warnings!"
		exit 1
		;;
	esac
	done
	if [[ $(echo ${DELETE_DATABASE}) == "true" ]]; then
		echo "You are about to DELETE app data from the current database and re-import source data"
	else
		echo "WARNING: You will not delete current database records, so stale/duplicate items can remain"
	fi
	if [[ $(echo ${QUIET}) == "false" ]]; then
		read -p "Are you sure? " -n 1 -r
		echo ""
		if [[ ! $REPLY =~ ^[Yy]$ ]]
		then
			exit 1
		fi
	fi

	# Setup SSH agent to connect to Github
	# eval $(ssh-agent)
	# ssh-add ${rsakey}

	cd "${cur}"
	if [[ $(echo $DELETE_DATABASE) == "true" ]]; then
		if mysqldump $database > /root/mysqldump_$database_$today.sql | tee -a ${log}; then
			echo "INFO: Succesfully backuped $database to /root/mysqldump_${database}_${today}.sql" | tee -a ${log}
			TABLES=$(mysql jcdatabase -e "show tables;" | grep lawofmessiah_app)
			echo "Now deleting data from lawofmessiah_app tables" | tee -a ${log}
			IFS=$'\n'
			for table in ${TABLES}; do
				mysql $database -e "SET FOREIGN_KEY_CHECKS = 0; DELETE FROM $table; SET FOREIGN_KEY_CHECKS = 1"
			done
		else
			echo "ERROR: Mysqldump was not successful. Please investigate why. Now exiting." | tee -a ${log}
			exit 1
		fi
	fi

	# Import active datasets
	cd "${cur}"
	echo "INFO: ${start} - Start importing Law of Messiah" | tee -a ${log}
	python3 manage.py import_law_of_messiah --source "${lom_source}" | tee -a ${log}
	echo "INFO: ${start} - Start importing Law of Messiah drawings" | tee -a ${log}
	python3 manage.py import_law_of_messiah_drawings --filename-prefix jv_waj_lom_ | tee -a ${log}
	end=$(date '+%Y-%m-%d %H:%M:%S')
	echo "INFO: ${end} - Ended importing Law of Messiah drawings" | tee -a ${log}
	echo "INFO: ${start} - Start importing Maimonides commandments" | tee -a ${log}
	python3 manage.py import_maimonides | tee -a ${log}
	end=$(date '+%Y-%m-%d %H:%M:%S')
	echo "INFO: ${end} - Ended importing Maimonides commandments" | tee -a ${log}
	end=$(date '+%Y-%m-%d %H:%M:%S')
	echo "INFO: ${end} - Ended importing Law of Messiah" | tee -a ${log}

# Other Operating Systems like Windows
else
	lom_source=data/lawofmessiah/filter_output/collected_ids_titles.yaml
	echo "INFO: Start importing Law of Messiah"
	python3 manage.py import_law_of_messiah --source "${lom_source}"
	echo "INFO: Start importing Law of Messiah drawings"
	python3 manage.py import_law_of_messiah_drawings --filename-prefix jv_waj_lom_
	echo "INFO: Ended importing Law of Messiah drawings"
	echo "INFO: Start importing Maimonides commandments"
	python3 manage.py import_maimonides
	echo "INFO: Ended importing Maimonides commandments"
	echo "INFO: Ended importing Law of Messiah"

fi
