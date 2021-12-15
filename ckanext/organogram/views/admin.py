from flask import Blueprint

from ckan.plugins import toolkit
import ckan.lib.uploader as uploader
import cgi
from ckan.views.admin import before_request as admin_before_request


organogram_admin_blueprint = Blueprint(u'organogram_admin_blueprint', __name__, url_prefix=u'/ckan-admin')


@organogram_admin_blueprint.before_request
def before_request():
    return admin_before_request()


def admin():
    if toolkit.request.method == 'POST':
        data = dict(toolkit.request.POST)

        if isinstance(data.get('organogram_file_upload'), cgi.FieldStorage):
            upload = uploader.get_uploader('organogram', data['organogram_file_url'])
            upload.update_data_dict(data, 'organogram_file_url', 'organogram_file_upload', 'clear_upload')
            upload.upload(uploader.get_max_image_size())
            organogram_file_url = upload.filename
        else:
            organogram_file_url = data.get('organogram_file_url')

        toolkit.get_action('config_option_update')({}, {
            'ckanext.organogram.file_url': organogram_file_url
        })

    organogram_file_url = toolkit.get_action('config_option_show')({}, {
        'key': 'ckanext.organogram.file_url'
    })

    extra_vars = {
        'data': {
            'organogram_file_url': organogram_file_url
        },
        'errors': {}
    }
    return toolkit.render('admin/organogram_config.html', extra_vars)


organogram_admin_blueprint.add_url_rule(u'/organogram',
                                        view_func=admin,
                                        methods=[u'GET', u'POST'])


def get_blueprints():
    return [organogram_admin_blueprint]
