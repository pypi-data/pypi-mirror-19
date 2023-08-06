# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from modeltranslation.translator import translator, TranslationOptions

from .models import ContactFormSettings


class ContactFormSettingsTranslationOptions(TranslationOptions):
    fields = ('subject', 'success_html', )


translator.register(ContactFormSettings, ContactFormSettingsTranslationOptions)
