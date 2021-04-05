"""
Copyright (c) 2018 Keitaro AB

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

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