import os
from time import time

import ckan.model as model
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as helpers

from ckanext.slider import db


class SliderPlugin(plugins.SingletonPlugin):

    STATIC_FOLDER = 'slider-images'
    CONTROLLER = 'ckanext.slider.controller:SliderController'

    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IAuthFunctions)

    plugins.implements(plugins.ITemplateHelpers, inherit=True)
    plugins.implements(plugins.IConfigurable, inherit=True)

    def configure(self, config):
        if model.repo.are_tables_created() and \
                not db.slider_table.exists():
            db.slider_table.create()

        slider_static_path = os.path.join(
            config['pylons.paths']['static_files'],
            SliderPlugin.STATIC_FOLDER
        )

        if not os.path.exists(slider_static_path):
            os.mkdir(slider_static_path)

        config['slider_static_folder'] = slider_static_path

    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_public_directory(config, 'public')
        toolkit.add_resource('fanstatic', 'slider')
        toolkit.add_ckan_admin_tab(config, 'slider_admin', {
            'title': 'Slider',
            'icon': 'film'
        })

    def before_map(self, route):
        route.connect(
            'slider_admin',
            '/ckan-admin/slider',
            controller=self.CONTROLLER,
            action='index'
        )

        route.connect(
            'slider_admin_delete',
            '/ckan-admin/slider/{id_slider}/delete',
            controller=self.CONTROLLER,
            action='delete'
        )

        route.connect(
            'slider_admin_edit',
            '/ckan-admin/slider/{id_slider}/edit',
            controller=self.CONTROLLER,
            action='edit'
        )

        route.connect(
            'slider_admin_add',
            '/ckan-admin/slider/add',
            controller=self.CONTROLLER,
            action='add'
        )

        return route

    @staticmethod
    def get_helpers():
        return {
            'get_slider': _get_slider,
            'get_slider_url': _get_slider_url,
            'get_slider_static_url': lambda: SliderPlugin.STATIC_FOLDER
        }

    @staticmethod
    def get_auth_functions():
        return {
            'admin_slider': _admin_slider
        }


def _get_slider_url(action, id_slider):
    kwargs = {}
    if action not in ['add', 'index']:
        kwargs['id_slider'] = id_slider
    return helpers.url_for(
        action=action,
        controller=SliderPlugin.CONTROLLER,
        **kwargs
    )


def _get_slider():
    context = {}
    slides = db.Slider.find(is_active=True)
    if slides:
        context['slides'] = slides.all()
    else:
        context['slides'] = []

    return plugins.toolkit.render('slider/slider.html', extra_vars=context)


def _admin_slider(context, data_dict=None):
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
