from ckan.controllers.admin import AdminController
from ckan.plugins import toolkit
import ckan.lib.uploader as uploader
import cgi


class AdminController(AdminController):
    def organogram_admin(self):
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