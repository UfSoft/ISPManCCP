# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: domain.py 12 2006-10-22 14:19:41Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/ispmanccp/models/domain.py $
# $LastChangedDate: 2006-10-22 15:19:41 +0100 (Sun, 22 Oct 2006) $
#             $Rev: 12 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

import formencode
from ispmanccp.models.validators import SecurePassword, CurrentPassword

class ChangeDomainPassword(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    domain = formencode.validators.String(not_empty=True)
    cur_pass = CurrentPassword(not_empty=True)
    new_pass = SecurePassword(not_empty=True)
    chk_pass = formencode.validators.String(not_empty=True)
    chained_validators = [
        formencode.validators.FieldsMatch('new_pass', 'chk_pass')
    ]
