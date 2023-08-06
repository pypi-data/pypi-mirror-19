# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import url

from .views import ContactFormSuccessView, ContactFormView


urlpatterns = [
    url(r'^$',
        ContactFormView.as_view(),
        name="contact_form"),
    url(r'^sent/$',
        ContactFormSuccessView.as_view(),
        name="contact_form_success"),
]
