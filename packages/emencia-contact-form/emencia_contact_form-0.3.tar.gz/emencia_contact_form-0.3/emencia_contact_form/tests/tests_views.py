from __future__ import unicode_literals

from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.test import RequestFactory, TestCase

from ..models import ContactFormSettings
from ..views import ContactFormView, ContactFormSuccessView


class TestView(TestCase):
    @classmethod
    def setUpTestData(self):
        site = Site.objects.get_current()
        ContactFormSettings.objects.get_or_create(site__pk=site.pk)
        self.factory = RequestFactory()


class TestContactFormView(TestView):
    @classmethod
    def setUpTestData(cls):
        super(TestContactFormView, cls).setUpTestData()
        cls.url = reverse("contact_form")

    def test_template(self):
        with self.assertTemplateUsed('contact_form/contact_form.html'):
            request = self.factory.get(self.url)
            resp = ContactFormView.as_view()(request)
            resp.render()

    def test_queries(self):
        with self.assertNumQueries(0):
            self.client.get(self.url)

    def test_success_url(self):
        assert ContactFormView().get_success_url() == '/sent/'


class TestContactFormSuccessView(TestView):
    @classmethod
    def setUpTestData(cls):
        super(TestContactFormSuccessView, cls).setUpTestData()
        cls.url = reverse("contact_form_success")

    def test_template(self):
        with self.assertTemplateUsed('contact_form/contact_form_success.html'):
            request = self.factory.get(self.url)
            resp = ContactFormSuccessView.as_view()(request)
            resp.render()

    def test_queries(self):
        with self.assertNumQueries(1):
            self.client.get(reverse("contact_form_success"))

    def test_context(self):
        resp = self.client.get(self.url)
        assert "message_success_content" in resp.context
