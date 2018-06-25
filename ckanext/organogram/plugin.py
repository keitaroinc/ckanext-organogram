import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.plugins import DefaultTranslation


class OrganogramPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer),
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.ITranslation)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'organogram')

    def update_config_schema(self, schema):

        ignore_missing = toolkit.get_validator('ignore_missing')

        schema.update({
            'ckanext.organogram.file_url': [ignore_missing, unicode],
        })
        return schema

    # IRoutes

    def before_map(self, map):
        map.connect(
            'organogram_admin',
            '/ckan-admin/organogram',
            controller='ckanext.organogram.controllers.admin:AdminController',
            action='organogram_admin')
        map.connect(
            'organogram_index',
            '/organogram',
            controller='ckanext.organogram.controllers.organogram:OrganogramController',
            action='organogram_index')
        return map
