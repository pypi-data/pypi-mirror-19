# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime
import os

from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from . import forms


class ContactFormEntryBase(object):
    """
    Dummy object to simulate a model entry because contact forms did not have a
    model

    You can use children of ``ContactFormEntryBase`` to fill in
    ``ContactFormSitemapBase.contact_forms`` and expose your contact forms in
    the sitemap.
    """
    url_name = None  # You contact form MUST have an url name
    priority = None  # Optional custom priority

    def get_pub_date(self):
        """
        Implement this method if you want to return a custom last modification
        datetime
        """
        return None


class ContactFormSitemap(Sitemap):
    """
    Simple sitemap for contact forms, because they are not database entries,
    only just forms
    """
    changefreq = "never"
    priority_base = 1.0
    contact_forms = []
    # We determine the default last modification datetime from the forms file
    # modification time because we don't have any other date to check for forms
    my_timestamp = os.path.getmtime(forms.__file__)
    global_pub_date = datetime.datetime.fromtimestamp(my_timestamp)

    def items(self):
        return [item() for item in self.contact_forms]

    def location(self, obj):
        return reverse(obj.url_name)

    def priority(self, obj):
        return obj.priority or self.priority_base

    def lastmod(self, obj):
        return obj.get_pub_date() or self.global_pub_date
