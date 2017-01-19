import os
import shutil
from time import time

from collections import defaultdict

import ckan.lib.base as base
import ckan.lib.helpers as h
import ckan.model as model
import ckan.plugins as plugins
import ckan.logic as logic

from ckan.common import _, request, c, response, g
from ckanext.slider import db

from ckanext.slider.plugin import SliderPlugin


check_access = logic.check_access


class SliderException(Exception):
    pass


class SliderNotFoundException(SliderException):
    pass


class SliderController(base.BaseController):

    def __before__(self, action, **env):
        super(SliderController, self).__before__(action, **env)

        try:
            self.context = {
                'model': model,
                'session': model.Session,
                'user': base.c.user or base.c.author,
                'auth_user_obj': base.c.userobj
            }

            check_access('admin_slider', self.context)

        except logic.NotAuthorized:
            base.abort(401, _('Only for sysadmin users.'))

    @staticmethod
    def _get_index_template(**extra_vars):
        context = {
            'slides': db.Slider.find().all(),
            'errors': [],
            'slide': []
        }
        context.update(extra_vars)
        return plugins.toolkit.render(
            'slider/index.html', extra_vars=context)

    def index(self):
        return self._get_index_template()

    def add(self):
        """
        Add slide.
        """
        if not request.POST:
            _redirect('index')

        data, errors = _validate_data()
        if not errors:
            errors = _save_slide(data, self.context['session'])
            if not errors:
                h.flash_success(_('Slide successful create.'))
                _redirect('index')

        del data['image']
        h.flash_error(_('Slide was not created.'))
        return self._get_index_template(
            errors=errors,
            slide=data
        )

    def delete(self, id_slider):
        """
        Delete slide.
        """
        try:
            id_slider = int(id_slider)
            slide = db.Slider.get(id_slider=id_slider)
            if not slide:
                raise SliderNotFoundException()
            # Remove old image
            if slide.image:
                image_file_name = os.path.join(_get_static_path(), slide.image)
                if os.path.exists(image_file_name):
                    os.remove(image_file_name)
            # Remove slide
            self.context['session'].delete(slide)
            self.context['session'].commit()
        except (ValueError, TypeError):
            h.flash_error(_('Invalid request.'))
        except SliderNotFoundException:
            h.flash_error(_('Slide was not found.'))
        except Exception as e:
            h.flash_error(str(e))
        else:
            h.flash_success(_('Slide successful delete.'))
        finally:
            _redirect('index')

    def edit(self, id_slider):
        """
        Edit slide.
        """
        try:
            id_slider = int(id_slider)
            slide = db.Slider.get(id_slider=id_slider)
            if not slide:
                raise SliderNotFoundException()
        except (ValueError, TypeError):
            h.flash_error(_('Invalid request.'))
        except SliderNotFoundException:
            h.flash_error(_('Slide was not found.'))
        else:
            if not request.POST:
                return self._get_index_template(slide=slide)

            data, errors = _validate_data(old_slide=slide)
            if not errors:
                errors = _save_slide(data, self.context['session'], slide)
                if not errors:
                    h.flash_success(_('Slide successful edit.'))
                    _redirect('index')

            h.flash_error(_('Slide was not edit.'))

            return self._get_index_template(slide=data, errors=errors)


def _redirect(action):
    base.redirect(h.url_for(
        action=action,
        controller=SliderPlugin.CONTROLLER
    ))


def _save_slide(data, session, old_slide=None):
    errors = defaultdict(list)
    try:
        slider = (db.Slider() if not old_slide else old_slide)

        slider.h1 = data['h1']
        slider.p = data['p']
        slider.button_left_enabled = data['button_left_enabled']
        if slider.button_left_enabled:
            slider.button_left_link = data['button_left_link']
            slider.button_left_name = data['button_left_name']
        slider.button_right_enabled = data['button_right_enabled']
        if slider.button_right_enabled:
            slider.button_right_link = data['button_right_link']
            slider.button_right_name = data['button_right_name']

        slider.is_text_left = data['position'] == 'left'
        slider.ordering = data['ordering']
        slider.is_active = data['is_active']

        if data['image'] is not None and \
                str(data['image'].__class__) == 'cgi.FieldStorage':
            image_name = int(time())
            image_ext = data['image'].type.split('/')[-1]

            # Get unique image name
            prefix = ''
            i = 0
            while True:
                image_file_name = '{}{}.{}'.format(
                    image_name, prefix, image_ext)
                if not os.path.exists(image_file_name):
                    break
                i += 1
                prefix = '_{}'.format(i)

            image_file = data['image'].file
            image_path = os.path.join(_get_static_path(), image_file_name)

            # Store image file
            image_file.seek(0)
            with open(image_path, 'wb') as output_file:
                shutil.copyfileobj(image_file, output_file)

            # Remove old image
            if slider.image:
                old_image_path = os.path.join(_get_static_path(), slider.image)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

            # Save image file name
            slider.image = image_file_name

        # Save!
        session.add(slider)
        session.commit()

    except Exception as e:
        errors.append(str(e))

    return errors


def _validate_data(old_slide=None):
    data = {}
    errors = defaultdict(list)

    try:
        data['image'] = request.POST.get('image')
        if data['image'] is None or \
                not str(data['image'].__class__) == 'cgi.FieldStorage':
            raise Exception(_('Image is required.'))
        if not data['image'].type.startswith('image/'):
            raise Exception(_('Must be image file.'))
    except Exception as e:
        if not old_slide:
            errors['image'].append(str(e))

    data['position'] = request.POST.get('position')
    if not data['position'] in ['left', 'right']:
        errors['position'].append(_('Must bu `left` or `right`.'))

    data['h1'] = request.POST.get('h1')
    if not data['h1']:
        errors['h1'].append(_('H1 is required.'))
    elif len(data['h1']) > 300:
        errors['h1'].append(_('H1 is maximum characters is 300.'))

    data['p'] = request.POST.get('p')
    if not data['p']:
        errors['p'].append(_('P is required.'))
    elif len(data['p']) > 3000:
        errors['p'].append(_('P is maximum characters is 3000.'))

    data['button_left_enabled'] = \
        request.POST.get('button_left_enabled') == 'on'
    if data['button_left_enabled']:
        data['button_left_link'] = request.POST.get('button_left_link')
        if not data['button_left_link']:
            errors['button_left_link'].append(
                _('`Button left link` is required.'))
        elif len(data['button_left_link']) > 300:
            errors['button_left_link'].append(
                _('`Button left link` is maximum characters is 300.'))
        data['button_left_name'] = request.POST.get('button_left_name')
        if not data['button_left_name']:
            errors['button_left_name'].append(
                _('`Button left name` is required.'))
        elif len(data['button_left_name']) > 50:
            errors['button_left_name'].append(
                _('`Button left name` is maximum characters is 50.'))

    data['button_right_enabled'] = \
        request.POST.get('button_right_enabled') == 'on'
    if data['button_right_enabled']:
        data['button_right_link'] = request.POST.get('button_right_link')
        if not data['button_right_link']:
            errors['button_right_link'].append(
                _('`Button right link` is required.'))
        elif len(data['button_right_link']) > 300:
            errors['button_right_link'].append(
                _('`Button right link` is maximum characters is 300.'))
        data['button_right_name'] = request.POST.get('button_right_name')
        if not data['button_right_name']:
            errors['button_right_name'].append(
                _('`Button right name` is required.'))
        elif len(data['button_right_name']) > 50:
            errors['button_right_name'].append(
                _('`Button right name` is maximum characters is 50.'))

    try:
        data['ordering'] = int(request.POST.get('ordering', 0))
        if not data['ordering']:
            errors['ordering'].append(
                '`ordering` is required.')
        elif not data['ordering'] > 0 or \
                not data['ordering'] < 100:
            errors['ordering'].append(_('`Ordering` must be in 1..99 range.'))
    except (ValueError, TypeError):
        errors['ordering'].append(_('`Ordering` must be integer.'))

    data['is_active'] = request.POST.get('is_active') == 'on'

    return data, errors


def _get_static_path():
    return plugins.toolkit.config['slider_static_folder']
