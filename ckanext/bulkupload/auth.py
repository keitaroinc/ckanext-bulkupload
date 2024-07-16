import ckan.plugins.toolkit as toolkit


def bulk_resource_upload(context, data_dict):
    userobj = context.get('auth_user_obj')
    if not userobj:
        raise toolkit.NotAuthorized
    return {'success': False}


def package_busoperator(context, data_dict):
    userobj = context.get('auth_user_obj')
    if not userobj:
        raise toolkit.NotAuthorized
    return {'success': False}
