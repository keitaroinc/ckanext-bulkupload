from flask import Blueprint
from flask.views import MethodView


import ckan.model as model
import ckan.logic as logic
import ckan.plugins.toolkit as tk
import ckan.lib.base as base

from ckan.common import g, request

bulkupload = Blueprint("bulkupload", __name__)


class BulkResourceUpload(MethodView):
    def _prepare(self):
        context = {
            "model": model,
            "session": model.Session,
            "user": g.user,
            "auth_user_obj": g.userobj,
        }
  
    def get(self, pkg_name):
        self._prepare()
        
        return base.render(
            u'package/snippets/resource_form_bulk.html', {
                u'pkg_name': pkg_name
            }
        )
    
    def post(self, pkg_name):
        return tk.render("package/snippets/resource_form_bulk.html")


bulkupload.add_url_rule("/dataset/<pkg_name>/resource/new/bulkupload",
                        view_func=BulkResourceUpload.as_view(str("bulk_upload")),
                        methods=("GET", "POST"))
