from flask import Blueprint
from ckan.common import config
import ckan.model as model
import ckan.logic as logic
import ckan.plugins.toolkit as tk
import ckan.lib.base as base
import logging
import os
import re
from pathlib import Path
import boto3
from botocore.exceptions import ClientError
import uuid

from ckan.common import g
from ckan.logic.action import get
import ckan.lib.helpers as h
import ckan.lib.navl.dictization_functions as dict_fns
import flask
from flask import redirect


log = logging.getLogger(__name__)

get_action = logic.get_action
parse_params = logic.parse_params
clean_dict = logic.clean_dict
tuplize_dict = logic.tuplize_dict
bulkupload = Blueprint("bulkupload", __name__)
try:
    storage_path = config.get('ckan.storage_path')
    log.info("12333333333333333333333")
    log.info(storage_path)
except:
    log.critical('''Please specify a ckan.storage_path in your config
                         for your uploads''')
    
aws_access_key_id = os.getenv('CKANEXT__S3FILESTORE__AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('CKANEXT__S3FILESTORE__AWS_SECRET_ACCESS_KEY')
bucket = os.getenv('CKANEXT__S3FILESTORE__AWS_BUCKET_NAME')
aws_region = os.getenv('CKANEXT__S3FILESTORE__REGION_NAME')
session = boto3.session.Session()
s3_client = session.client(
    service_name='s3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    endpoint_url=os.getenv('CKANEXT__S3FILESTORE__HOST_NAME', None),
    region_name=aws_region
)


def package_busoperator(errors=None):
    
    if flask.request.method == 'GET':
        context = {
            "model": model,
            "session": model.Session,
            "user": g.user,
            "auth_user_obj": g.userobj,
        }

        user_dict = {
            'id': g.user,
            'permission':'create_dataset',
        }

        org_list = tk.get_action("organization_list_for_user")(context, user_dict)

        try:
            tk.check_access('package_create', context)
        except:
            return tk.abort(403)
        
        extra_var = {
           'org_list': org_list,
           'errors': errors,
        }

        return base.render('package/package_busoperator.html', extra_var)
    
    elif flask.request.method == 'POST':
        context = {
            "model": model,
            "session": model.Session,
            "user": g.user,
            "auth_user_obj": g.userobj,
        }
        try:
            tk.check_access('package_create', context)
        except:
            return tk.abort(403)
        
        form_data = clean_dict(
            dict_fns.unflatten(tuplize_dict(parse_params(tk.request.form)))
        )
        name_validated = form_data['title'].replace(' ', '-').lower()

        data_dict = {
            'name': name_validated,
            'title': form_data['title'],
            'private': False,
            'status': 'active',
            'owner_org': form_data['owner_org'],
            'dataset_start_date': form_data['date-start'],
            'dataset_end_date': form_data['date-end'],
        }
        try:
            x = tk.get_action("package_create")(context, data_dict)
            pckg_title = x['name']
            return h.redirect_to(f'/dataset/{pckg_title}/resource/new/bulkupload')
        
        except:
            # To Do: Find better way (CKAN way) to handle errors
            errors = 'Dataset name exists'
            return redirect(h.url_for('bulkupload.package_busoperator', errors=errors))



def bulk_resource_upload(pkg_name):

    if flask.request.method == 'GET':
        context = {
            "model": model,
            "session": model.Session,
            "user": g.user,
            "auth_user_obj": g.userobj,
        }
        try:
            tk.check_access('package_create', context)
        except:
            return tk.abort(403)
        
        pkg_name_dict = {
            'id': pkg_name,
            }
        pkg_dict = get.package_show(context, pkg_name_dict)
        
        return base.render(
            'package/resource_busoperator.html', {
                'pkg_name': pkg_name,
                'pkg_dict': pkg_dict,
            }
        )
    elif flask.request.method == 'POST':
        context = {
            "model": model,
            "session": model.Session,
            "user": g.user,
            "auth_user_obj": g.userobj,
        }
        try:
            tk.check_access('package_create', context)
        except:
            return tk.abort(403)
        
        form_data = clean_dict(
            dict_fns.unflatten(tuplize_dict(parse_params(tk.request.form)))
        )
        pkg_name_dict = {
            'id': pkg_name,
            }
        pkg_dict = get.package_show(context, pkg_name_dict)
        uploaded_files = flask.request.files.getlist("file[]")

        # For newly created datasets
        if pkg_dict['state'] != 'active':
            patch_package_data = {
                'id': pkg_name,
                'state': 'active',
            }
            tk.get_action("package_patch")(context, patch_package_data)

        #The for loop stays for future multi files upload posibility
        for f in uploaded_files:

            url_striped = re.sub(r"[)()]+", "", f.filename)
            data_dict = {
                'package_id': pkg_name,
                'name': f.filename,
                'url': url_striped,
                'url_type': 'upload',
            }

            x = tk.get_action("resource_create")(context, data_dict)
            unique_filename = str(uuid.uuid4())[:8] + str(f.filename)
            file_name = os.path.join(storage_path, unique_filename)
            log.info("FILE NAMEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
            log.info(file_name)
            f.save(file_name)

            object_name = '/resources/' + x['id'] + '/' + url_striped
            log.info("=========================")
            log.info(object_name)
            log.info(x)

            try:
                response = s3_client.upload_file(file_name, bucket, object_name)
                log.info("OBJECT NAME!!!!!")
                log.info(object_name)
                log.info("BUCKET!!!!!!!")
                log.info(bucket)
                log.info("RESPONSE!!!!!!!!!!")
                log.info(response)

            except ClientError as e:
                logging.error(e)
            
            os.remove(file_name)
            

        extra_vars= {
            'pkg_dict': pkg_dict
        }
        return base.render(
            'package/activity_bulk.html', extra_vars
        )


bulkupload.add_url_rule("/dataset/new/busoperator",
                        view_func=package_busoperator,
                        methods=("GET", "POST"))

bulkupload.add_url_rule("/dataset/<pkg_name>/resource/new/bulkupload",
                        view_func=bulk_resource_upload,
                        methods=("GET", "POST"))
