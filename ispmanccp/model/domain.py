# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: domain.py 137 2008-01-27 07:00:17Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/ispmanccp/model/domain.py $
# $LastChangedDate: 2008-01-27 07:00:17 +0000 (Sun, 27 Jan 2008) $
#             $Rev: 137 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

from formencode import validators, Schema
from ispmanccp.model.validators import *

class ChangeDomainPassword(Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    ispmanDomain = validators.String(not_empty=True)
    cur_pass = CurrentPassword(not_empty=True)
    new_pass = SecurePassword(not_empty=True)
    chk_pass = validators.String(not_empty=True)
    chained_validators = [
        validators.FieldsMatch('new_pass', 'chk_pass')
    ]
