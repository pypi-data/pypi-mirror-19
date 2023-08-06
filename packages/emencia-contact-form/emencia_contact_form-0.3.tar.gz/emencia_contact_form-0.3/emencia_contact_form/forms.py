# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from captcha.fields import ReCaptchaField

from .fields import MultiEmailField
from .forms_utils import create_basic_form_helper
from .mails import send_mail_to_contact
from .models import Contact, ContactFormSettings


class ContactForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    captcha = ReCaptchaField(attrs={'theme': 'clean'})

    class Meta:
        model = Contact
        fields = ('civility', 'first_name', 'last_name', 'email', 'message',
                  'phone', 'company', 'city', 'state', 'country',
                  'optin_newsletter', 'captcha', )

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = create_basic_form_helper()

    def save(self, commit=True):
        contact = super(ContactForm, self).save()
        send_mail_to_contact(contact)
        return contact


class ContactFormSettingsForm(ModelForm):
    email_to = MultiEmailField(
        _("Send mail to"),
        help_text=_(
            "You can specify multiple mail addresses: "
            "Separate them with a comma.")
    )

    class Meta:
        model = ContactFormSettings
        fields = ("site", "subject", "email_to", "email_from", "success_html")
