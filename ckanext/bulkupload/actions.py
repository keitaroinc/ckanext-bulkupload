import ckan.plugins.toolkit as tk
import requests
import ssl

ssl.match_hostname = lambda cert, hostname: True


def call_add_resouce_api():
    
    print("============================1==========================")


def call_add_resouce_api1():
    
    print("============================1==========================")
    ssl.match_hostname = lambda cert, hostname: True
    url = "http://localhost:5000/api/3/action/resource_create"
    headers = {
        'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJhN1lVZWNldGxTQjlRLXNBbEg4NTRRbjhlVEUxQXhGQzEtNFZnZzZ4M18xa0NscnZZX0hheGk0bkNiVFJRZ24wdk1oQnBWUGpRVjd5TnktMyIsImlhdCI6MTcxMjIzMzAwMX0.NBvgZIicgkHIbd_2lTmck5GLv_oWSNOA0lb4UdnWC0Q',
    }
    print("====================2==================================")
    files = {
        'package_id': (None, 'cloudstorage-03'),
        'name': (None, '5MB'),
        'url': (None, 'upload'),
        'description': (None, ''),
        'upload': open('/home/blagoja/Downloads/sample_data/5MB', 'rb'),
    }
    print("===========================3===========================")
    response = requests.post(url, headers=headers, files=files, verify=False)
    print(response)
    print('====================4==================================')
    return response
