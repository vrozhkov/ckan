from time import time

from collections import defaultdict

import ckan.lib.base as base
import ckan.lib.helpers as h
import ckan.model as model
import ckan.plugins as plugins
import ckan.logic as logic

from ckan.common import _, request, c, response, g
# from ckanext.banner import db

# from ckanext.banner.plugin import BannerPlugin


check_access = logic.check_access


class BannerException(Exception):
    pass


class BannerNotFoundException(BannerException):
    pass


class BannerController(base.BaseController):

    def __before__(self, action, **env):
        super(BannerController, self).__before__(action, **env)

        try:
            self.context = {
                'model': model,
                'session': model.Session,
                'user': base.c.user or base.c.author,
                'auth_user_obj': base.c.userobj
            }

            check_access('admin_banner', self.context)

        except logic.NotAuthorized:
            base.abort(401, _('Only for sysadmin users.'))

    @staticmethod
    def _get_index_template(**extra_vars):
        context = {
            'banners': [],
            'errors': [],
            'banner': []
        }
        context.update(extra_vars)
        return plugins.toolkit.render(
            'banner/index.html', extra_vars=context)

    def index(self):
        return self._get_index_template()


def _redirect(action):
    base.redirect(h.url_for(
        action=action,
        controller=BannerPlugin.CONTROLLER
    ))


def _get_static_path():
    return plugins.toolkit.config['banner_static_folder']
