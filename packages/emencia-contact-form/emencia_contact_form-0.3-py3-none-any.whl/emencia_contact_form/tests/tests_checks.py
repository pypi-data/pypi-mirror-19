# -*- coding: utf-8 -*-

import pytest

import django

from distutils.version import LooseVersion

from django.test import TestCase

from ..checks import check_mandatory_apps_are_in_installed_apps


class DummyDecorator(object):
    def __init__(self, installed_apps, **kwargs):
        self.installed_apps = installed_apps

    def __call__(self, decorated, *args):
        return decorated


if LooseVersion(django.get_version()) < LooseVersion('1.10'):
    isolate_apps = DummyDecorator
else:
    from django.test.utils import isolate_apps


@pytest.mark.skipif(LooseVersion(django.get_version()) < LooseVersion('1.10'),
                    reason="requires django 1.10")
@isolate_apps('contact_form', attr_name="apps")
class TestCheck(TestCase):
    def test_check_installed_app(self):
        installed_apps = ('django.contrib.admin', )
        with self.settings(INSTALLED_APPS=installed_apps):
            assert len(
                check_mandatory_apps_are_in_installed_apps(
                    app_configs=self.apps.get_app_configs())
            ) == 9

        assert len(
            check_mandatory_apps_are_in_installed_apps(
                app_configs=self.apps.get_app_configs())
        ) == 0
