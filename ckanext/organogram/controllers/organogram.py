from ckan.lib.base import BaseController
from ckan.plugins import toolkit


class OrganogramController(BaseController):
    def organogram_index(self):
        return toolkit.render(
            'organogram/index.html'
        )