# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Column, Field, Row, Submit

try:
    unicode = unicode
except NameError:
    # 'unicode' is undefined, must be Python 3
    unicode = str
    basestring = (str, bytes)


def get_simple_row_column(field, *args, **kwargs):
    """
    For use with crispy forms and foundation.
    Shortcut for simple row with only a full column
    """
    if isinstance(field, basestring):
        field = Field(field, *args, **kwargs)
    return Row(Column(field), )


def create_basic_form_helper():
    """
    Returns a classic crispy-forms FormHelper with default for Abide
    and a submit button
    """
    helper = FormHelper()
    helper.attrs = {'data_abide': ''}
    helper.form_action = '.'
    helper.add_input(Submit('submit', _('Submit')))
    return helper
