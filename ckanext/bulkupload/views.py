from flask import Blueprint
from ckan.common import config
import ckan.model as model
import ckan.logic as logic
import ckan.plugins.toolkit as tk
import ckan.lib.base as base
import logging
import os
from pathlib import Path

from ckan.common import g
from ckan.logic.action import get
import ckan.lib.navl.dictization_functions as dict_fns
import flask


log = logging.getLogger(__name__)

get_action = logic.get_action
parse_params = logic.parse_params
clean_dict = logic.clean_dict
tuplize_dict = logic.tuplize_dict
bulkupload = Blueprint("bulkupload", __name__)
try:
    storage_path = config.get('ckan.storage_path')
except:
    log.critical('''Please specify a ckan.storage_path in your config
                         for your uploads''')


def bulk_resource_upload(pkg_name):

    if flask.request.method == 'GET':
        context = {
            "model": model,
            "session": model.Session,
            "user": g.user,
            "auth_user_obj": g.userobj,
        }
        try:
            tk.check_access("bulk_resource_upload", context)
        except:
            return tk.abort(403)
        
        pkg_name_dict = {
            'id': pkg_name,
            }
        pkg_dict = get.package_show(context, pkg_name_dict)
        
        return base.render(
            'package/new_resource_not_draft_bulk.html', {
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
            tk.check_access("bulk_resource_upload", context)
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

        for f in uploaded_files:

            data_dict = {
                'package_id': pkg_name,
                'name': f.filename,
                'url': f.filename,
                'url_type': 'upload',
                'subject': form_data['subject'],
                'description': form_data['description'],
                'author': form_data['author'],
                'publisher': form_data['publisher'],
                'contributor': form_data['contributor'],
                'date': form_data['date'],
                'type': form_data['type'],
                'identifier': form_data['identifier'],
                'source': form_data['source'],
                'language': form_data['language'],
                'relation': form_data['relation'],
                'coverage': form_data['coverage'],
                'rights': form_data['rights'],
                'medium': form_data['medium'],
                'source_of_acquisition': form_data['source_of_acquisition'],
                'organization_description': form_data['organization_description'],
                'physical_technical': form_data['physical_technical'],
                'location': form_data['location'],
                'rules': form_data['rules'],
                'date_of_descriptions': form_data['date_of_descriptions'],
            }

            x = tk.get_action("resource_create")(context, data_dict)
            upload_path = storage_path + '/resources/' + x['id'][0:3] + "/" + x['id'][3:6]
            upload_filename = x['id'][6:]
            filepath = Path(os.path.join(upload_path, upload_filename))
            filepath.parent.mkdir(parents=True, exist_ok=True)
            f.save(os.path.join(upload_path, upload_filename))

        extra_vars= {
            'pkg_dict': pkg_dict
        }
        return base.render(
            'package/activity_bulk.html', extra_vars
        )


bulkupload.add_url_rule("/dataset/<pkg_name>/resource/new/bulkupload",
                        view_func=bulk_resource_upload,
                        methods=("GET", "POST"))
