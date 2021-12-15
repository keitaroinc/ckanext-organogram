from flask import Blueprint

from ckan.plugins import toolkit


organogram = Blueprint(u'organogram_blueprint', __name__)


def index():
    return toolkit.render(
        'organogram/index.html'
    )


organogram.add_url_rule(u'/organogram',
                        view_func=index)


def get_blueprints():
    return [organogram]
