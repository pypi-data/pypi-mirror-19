# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext as _

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .forms import ContactFormSettingsForm
from .models import Contact, ContactFormSettings


class ContactResource(resources.ModelResource):
    class Meta:
        model = Contact


class ContactAdmin(ImportExportModelAdmin):
    date_hierarchy = 'creation_date'
    resource_class = ContactResource

    list_display = ('last_name', 'first_name', 'company', 'email', 'phone',
                    'city', 'country', 'optin_newsletter', 'creation_date')

    list_filter = ('creation_date', 'optin_newsletter')
    search_fields = ('first_name', 'last_name', 'company', 'email', 'phone',
                     'city', 'state')
    fieldsets = ((None, {'fields': ('civility', 'first_name', 'last_name',
                                    'company')}),
                 (None, {'fields': ('message',)}),
                 (_('Contact'), {'fields': ('email', 'phone',
                                 'optin_newsletter')}),
                 (_('Address'), {'fields': ('city', 'state', 'country')}),)


class ContactFormSettingsAdmin(admin.ModelAdmin):
    form = ContactFormSettingsForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(ContactFormSettingsAdmin, self).get_form(
            request, obj, **kwargs)
        form.base_fields['email_to'].widget.attrs['style'] = 'width: 45em;'
        return form


admin.site.register(Contact, ContactAdmin)
admin.site.register(ContactFormSettings, ContactFormSettingsAdmin)
