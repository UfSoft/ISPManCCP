# -*- coding: iso8859-15 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: forms.py 5 2006-09-01 19:30:14Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/ispmanccp/lib/forms.py $
# $LastChangedDate: 2006-09-01 20:30:14 +0100 (Fri, 01 Sep 2006) $
#             $Rev: 5 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

from formbuild.form import FormBase
from formbuild.builder.field.basic import HtmlFields
from formbuild.builder.layout import basic, pages, LayoutBuilder


class ISPManLayout(LayoutBuilder):
    def start(self, div_id=None, div_class=None):
        html = '<div'

        if div_id:
            html += ' id="%s"' % div_id

        if div_class:
            html += ' class="%s"' % div_class

        return html + '>'

    def end(self):
        return '</div>'


class Form(FormBase):
    field = HtmlFields()
    layout = ISPManLayout(), pages.HtmlLayout(), basic.HtmlLayout()
