# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


class ContactApphook(CMSApp):
    name = "Contact form"

    def get_urls(self, page=None, language=None, **kwargs):
        return ["emencia_contact_form.urls"]


apphook_pool.register(ContactApphook)
