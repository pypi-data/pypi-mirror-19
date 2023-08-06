# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.views.generic import FormView, TemplateView

from .forms import ContactForm


class ContactFormView(FormView):
    form_class = ContactForm
    template_name = 'contact_form/contact_form.html'

    def get_success_url(self):
        return reverse('contact_form_success')

    def form_valid(self, form):
        form.save()
        return super(ContactFormView, self).form_valid(form)


class ContactFormSuccessView(TemplateView):
    template_name = "contact_form/contact_form_success.html"

    def get_context_data(self, **kwargs):
        context = super(ContactFormSuccessView, self).get_context_data(**kwargs)
        html_success = Site.objects\
            .select_related("contactformsettings")\
            .get(pk=settings.SITE_ID)\
            .contactformsettings.success_html
        context["message_success_content"] = html_success
        return context
