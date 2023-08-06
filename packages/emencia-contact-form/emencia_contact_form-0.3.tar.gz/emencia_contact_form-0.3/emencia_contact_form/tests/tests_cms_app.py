# -*- coding: utf-8 -*-

from django.test import SimpleTestCase

from ..cms_app import ContactApphook


class SmokeTest(SimpleTestCase):
    def test_smoke(self):
        c = ContactApphook()
        assert c.name == "Contact form"
