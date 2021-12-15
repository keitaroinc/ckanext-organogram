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
import six

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.plugins import DefaultTranslation
from ckanext.organogram import auth
import ckanext.organogram.views.organogram as organogram_blueprint
import ckanext.organogram.views.admin as admin_blueprint


class OrganogramPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer),
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IBlueprint)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'organogram')

    def update_config_schema(self, schema):

        ignore_missing = toolkit.get_validator('ignore_missing')

        schema.update({
            'ckanext.organogram.file_url': [ignore_missing, six.text_type],
        })
        return schema

    # IBlueprint

    def get_blueprint(self):
        return organogram_blueprint.get_blueprints() + \
               admin_blueprint.get_blueprints()

    # IAuthFunctions

    def get_auth_functions(self):
        return {
            'config_option_show': auth.config_option_show,
        }
