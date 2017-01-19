import os
from time import time

import ckan.model as model
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as helpers

# from ckanext.banner import db


class BannerPlugin(plugins.SingletonPlugin):

    STATIC_FOLDER = 'banner-images'
    CONTROLLER = 'ckanext.banner.controller:BannerController'

    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IAuthFunctions)

    # plugins.implements(plugins.ITemplateHelpers, inherit=True)
    plugins.implements(plugins.IConfigurable, inherit=True)

    def configure(self, config):
        # if model.repo.are_tables_created() and \
        #         not db.banner_table.exists():
        #     db.banner_table.create()

        banner_static_path = os.path.join(
            config['pylons.paths']['static_files'],
            BannerPlugin.STATIC_FOLDER
        )

        if not os.path.exists(banner_static_path):
            os.mkdir(banner_static_path)

        config['banner_static_folder'] = banner_static_path

    def update_config(self, _config):
        toolkit.add_template_directory(_config, 'templates')
        toolkit.add_public_directory(_config, 'public')
        toolkit.add_resource('fanstatic', 'banner')
        toolkit.add_ckan_admin_tab(_config, 'banner_admin', {
            'title': 'Banner',
            'icon': 'th'
        })

    def before_map(self, route):
        route.connect(
            'banner_admin',
            '/ckan-admin/banner',
            controller=self.CONTROLLER,
            action='index'
        )

        # route.connect(
        #     'banner_admin_delete',
        #     '/banner/{id_banner}/delete',
        #     controller=self.CONTROLLER,
        #     action='delete'
        # )

        # route.connect(
        #     'banner_admin_edit',
        #     '/banner/{id_banner}/edit',
        #     controller=self.CONTROLLER,
        #     action='edit'
        # )

        # route.connect(
        #     'banner_admin_add',
        #     '/banner/add',
        #     controller=self.CONTROLLER,
        #     action='add'
        # )

        return route

#     # @staticmethod
#     # def get_helpers():
#     #     return {
#     #         'get_banner': _get_banner,
#     #         'get_banner_url': _get_banner_url,
#     #         'get_banner_static_url': lambda: BannerPlugin.STATIC_FOLDER
#     #     }

    @staticmethod
    def get_auth_functions():
        return {
            'admin_banner': _admin_banner
        }


# # def _get_banner_url(action, id_banner):
# #     kwargs = {}
# #     if action not in ['add', 'index']:
# #         kwargs['id_banner'] = id_banner
# #     return helpers.url_for(
# #         action=action,
# #         controller=BannerPlugin.CONTROLLER,
# #         **kwargs
# #     )


# # def _get_banner():
# #     context = {}
# #     banners = db.Banners.find(is_active=True)
# #     if banners:
# #         context['banner'] = banners.all()
# #     else:
# #         context['banner'] = []

# #     return plugins.toolkit.render('banner/banner.html', extra_vars=context)


def _admin_banner(context, data_dict=None):
    user = context.get('auth_user_obj')
    if not user or \
            not user.sysadmin:
        return {
            'success': False,
            'msg': 'Not allowed. Only for sysadmins.'
        }
    return {
        'success': True
    }
