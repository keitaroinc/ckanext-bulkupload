from flask import Blueprint
from flask.views import MethodView

import requests
import json
import ssl
import ckan.model as model
import ckan.logic as logic
import ckan.plugins.toolkit as tk
import ckan.lib.base as base

from ckan.common import g
from ckan.logic.action import get, create
import flask

get_action = logic.get_action
bulkupload = Blueprint("bulkupload", __name__)


def bulk_resource_upload(pkg_name):

    if flask.request.method == 'GET':
        context = {
            "model": model,
            "session": model.Session,
            "user": g.user,
        }
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

        tk.get_action("call_add_resouce_api")
        return base.render(
            'package/upload_bulk_sucess.html'

        )


bulkupload.add_url_rule("/dataset/<pkg_name>/resource/new/bulkupload",
                        view_func=bulk_resource_upload,
                        methods=("GET", "POST"))
