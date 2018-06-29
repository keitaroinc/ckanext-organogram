from ckan.plugins import toolkit


@toolkit.auth_allow_anonymous_access
def config_option_show(context, data_dict):
    return {'success': True}
