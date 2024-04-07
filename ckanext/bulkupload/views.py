from flask import Blueprint
from flask.views import MethodView


import ckan.model as model
import ckan.logic as logic
import ckan.plugins.toolkit as tk
import ckan.lib.base as base

from ckan.common import g, request
from ckan.logic.action import get, update

bulkupload = Blueprint("bulkupload", __name__)


class BulkResourceUpload(MethodView):

    def get(self, pkg_name):
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
    
    def post(self, pkg_name):
        return tk.render("package/upload_bulk_sucess.html")


bulkupload.add_url_rule("/dataset/<pkg_name>/resource/new/bulkupload",
                        view_func=BulkResourceUpload.as_view(str("bulk_upload")),
                        methods=("GET", "POST"))
