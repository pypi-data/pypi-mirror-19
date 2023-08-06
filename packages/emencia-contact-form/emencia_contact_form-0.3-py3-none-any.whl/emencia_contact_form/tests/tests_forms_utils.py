from django import forms
from django.test import SimpleTestCase

from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Row

from ..forms_utils import create_basic_form_helper, get_simple_row_column


class TestFormsUtils(SimpleTestCase):
    def test_get_simple_row_column(self):
        field = forms.CharField()
        result = get_simple_row_column(field)
        assert isinstance(result, Row)

        result = get_simple_row_column("foo")
        assert isinstance(result, Row)

    def test_create_basic_form_helper(self):
        helper = create_basic_form_helper()
        assert isinstance(helper, FormHelper)
        assert helper.attrs["data_abide"] == ""
        assert helper.form_action == '.'
