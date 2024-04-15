#!/usr/bin/env python3
import requests
import ssl
from os import walk
from datetime import datetime
from variables import *

now = datetime.now()
now_date = str(now.date())
now_date = now_date.replace("-", "/")

f = []
mypath = FOLDER_PATH
for (dirpath, dirnames, filenames) in walk(mypath):
    list_of_files = [x for x in filenames]
    break


ssl.match_hostname = lambda cert, hostname: True

url = "http://localhost:5000/api/3/action/resource_create"

headers = {
    'Authorization': API_TOKEN,
}

for y in list_of_files:
    files = {
        'package_id': (None, DATASET_NAME),
        'name': (None, y),
        'url': (None, 'upload'),
        'subject': (None, SUBJECT),
        'description': (None, DESCRIPTION),
        'author': (None, CREATOR),
        'publisher': (None, PUBLISHER),
        'contributor': (None, CONTRIBUTOR),
        'date': (None, DATE),
        'type': (None, TYPE),
        'identifier': (None, IDENTIFIER),
        'source': (None, SOURCE),
        'language': (None, LANGUAGE),
        'relation': (None, RELATION),
        'coverage': (None, COVERAGE),
        'rights': (None, RIGHTS),
        'medium': (None, MEDIUM),
        'source_of_acquisition': (None, SOURCE_OF_ACQUISITION),
        'organization_description': (None, ORGANIZATIONAL_DESCRIPTION),
        'physical_technical': (None, PHYSICAL_TECHNICAL),
        'location': (None, LOCATION),
        'rules': (None, RULES),
        'date_of_descriptions': (None, now_date),
        'upload': open(dirpath + "/" + y, 'rb'),
    }

    response = requests.post(url, headers=headers, files=files, verify=False)
    print(response)


