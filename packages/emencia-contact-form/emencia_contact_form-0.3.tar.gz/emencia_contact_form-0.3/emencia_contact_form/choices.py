# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _


MRS = "mrs"
MR = "mr"


CIVILITY_CHOICES = (
    (MRS, _('Mrs')),
    (MR, _('Mr')),
)


CIVILITY_DICT = dict(CIVILITY_CHOICES)
