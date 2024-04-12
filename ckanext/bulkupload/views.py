from flask import Blueprint
from flask import request
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
import flask


log = logging.getLogger(__name__)

get_action = logic.get_action
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
        
        pkg_name_dict = {
            'id': pkg_name,
            }
        pkg_dict = get.package_show(context, pkg_name_dict)
        uploaded_files = flask.request.files.getlist("file[]")
        for f in uploaded_files:

            data_dict = {
                'package_id': pkg_name,
                'name': f.filename,
                'url': f.filename,
                'url_type': 'upload',
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
