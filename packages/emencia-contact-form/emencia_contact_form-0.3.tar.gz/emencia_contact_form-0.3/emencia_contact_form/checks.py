# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.checks import Error, register


@register()
def check_mandatory_apps_are_in_installed_apps(app_configs, **kwargs):
    from django.conf import settings

    errors = []
    needed_modules = [
        'django.contrib.sitemaps',
        'django.contrib.sites',
        'modeltranslation',
        'django_countries',
        'crispy_forms',
        'crispy_forms_foundation',
        'captcha',
        'import_export',
        'emencia_contact_form',
    ]

    for module in needed_modules:
        if module not in settings.INSTALLED_APPS:
            errors.append(
                Error(
                    'INSTALLED_APPS is incomplete',
                    hint="Add '{mod}' in your INSTALLED_APPS".format(
                        mod=module),
                    obj='Import Error',
                    id='emencia_contact_form.check',
                )
            )
    return errors
