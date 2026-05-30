# walkasjesus_biblereferences
Repository for the Law of Messiah Framework where all the commandments with all their related Bible References are stored in a CSV. This CSV can be imported/exported with the [Law of Messiah Framework](https://github.com/walkasjesus/walkasjesus_framework) and the [Law of Messiah Server](https://github.com/walkasjesus/walkasjesus_server)

## Files

- **commandments.csv** — Contains all 77 Steps commandments with their related Bible references.
- **lessons.csv** — Contains lesson data related to the commandments.

## Usage

Import commandments into the database:
```bash
python manage.py import_commandments
```

Export commandments from the database:
```bash
python manage.py export_commandments
```

# Related projects and repositories
The following projects are related to this repository.

## lawofmessiah_framework
This repository is the heart of the application which will show all the different components of the Law of Messiah Application in a fancy Python Framework [Django](https://www.djangoproject.com/)

## lawofmessiah_server
This repository contains IT Automation tools for [Ansible](https://docs.ansible.com/ansible/latest/index.html) to install & configure all the server components which are required to serve the [Law of Messiah Framework](https://github.com/walkasjesus/walkasjesus_framework)

## walkasjesus_translations
This repository contains all translation files from English to other languages. We use Google translate to make a first automated translation. The next step for the translator is to review all translated items and acknowledge them through the admin panel of the website. 
