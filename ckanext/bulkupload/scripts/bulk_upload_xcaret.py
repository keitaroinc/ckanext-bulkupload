#!/usr/bin/env python3
import requests
import ssl
from os import walk
import os
import configparser

ssl.match_hostname = lambda cert, hostname: True

imported_vars = configparser.RawConfigParser()
imported_vars.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

folder_path = imported_vars.get('my_vars', "FOLDER_PATH")
api_token = imported_vars.get('my_vars', "API_TOKEN")
dataset_name = imported_vars.get("my_vars", "DATASET_NAME")
description = imported_vars.get("my_vars", "DESCRIPTION")
subject = imported_vars.get("my_vars", "SUBJECT")
creator = imported_vars.get("my_vars", "CREATOR")
publisher = imported_vars.get("my_vars", "PUBLISHER")
contributor = imported_vars.get("my_vars", "CONTRIBUTOR")
date = imported_vars.get("my_vars", "DATE")
type_field = imported_vars.get("my_vars", "TYPE")
identifier = imported_vars.get("my_vars", "IDENTIFIER")
source = imported_vars.get("my_vars", "SOURCE")
language = imported_vars.get("my_vars", "LANGUAGE")
relation = imported_vars.get("my_vars", "RELATION")
coverage = imported_vars.get("my_vars", "COVERAGE")
rights = imported_vars.get("my_vars", "RIGHTS")
medium = imported_vars.get("my_vars", "MEDIUM")
source_of_acquisition = imported_vars.get("my_vars", "SOURCE_OF_ACQUISITION")
organizational_description = imported_vars.get("my_vars", "ORGANIZATIONAL_DESCRIPTION")
physical_technical = imported_vars.get("my_vars", "PHYSICAL_TECHNICAL")
location = imported_vars.get("my_vars", "LOCATION")
rules = imported_vars.get("my_vars", "RULES")
date_modified = imported_vars.get("my_vars", "DATE_MODIFIED")


mypath = folder_path
for (dirpath, dirnames, filenames) in walk(mypath):
    list_of_files = [x for x in filenames]
    break

url = "https://xtoria.grupoxcaret.com/api/3/action/resource_create"

headers = {
    'Authorization': api_token,
}

for y in list_of_files:
    files = {
        'package_id': (None, dataset_name),
        'name': (None, y),
        'url': (None, 'upload'),
        'subject': (None, subject),
        'description': (None, description),
        'author': (None, creator),
        'publisher': (None, publisher),
        'contributor': (None, contributor),
        'date': (None, date),
        'type': (None, type_field),
        'identifier': (None, identifier),
        'source': (None, source),
        'language': (None, language),
        'relation': (None, relation),
        'coverage': (None, coverage),
        'rights': (None, rights),
        'medium': (None, medium),
        'source_of_acquisition': (None, source_of_acquisition),
        'organization_description': (None, organizational_description),
        'physical_technical': (None, physical_technical),
        'location': (None, location),
        'rules': (None, rules),
        'date_of_descriptions': (None, date_modified),
        'upload': open(dirpath + "/" + y, 'rb'),
    }
    
    response = requests.post(url, headers=headers, files=files, verify=False)
    print(response)


