import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckanext.bulkupload.actions as actions
import ckanext.bulkupload.auth as auth
from ckanext.bulkupload.views import bulkupload
from ckan.lib.plugins import DefaultTranslation


class BulkuploadPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.ITranslation)
    
    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'bulkupload')

    # IActions

    def get_actions(self):

        return {
            "call_add_resouce_api": actions.call_add_resouce_api,
            
        }

    # IAuthFunctions

    def get_auth_functions(self):
        return {
            "bulk_resource_upload": auth.bulk_resource_upload,
        }
    
    # IBlueprint

    def get_blueprint(self):
        
        return bulkupload
