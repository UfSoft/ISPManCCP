# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: domain.py 11 2006-10-22 10:03:27Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/ispmanccp/models/domain.py $
# $LastChangedDate: 2006-10-22 11:03:27 +0100 (Sun, 22 Oct 2006) $
#             $Rev: 11 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

import formencode
from ispmanccp.models.validators import SecurePassword

class ChangeDomainPassword(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    domain = formencode.validators.String(not_empty=True)
    new_pass = SecurePassword(not_empty=True)
    chk_pass = formencode.validators.String(not_empty=True)
    chained_validators = [
        formencode.validators.FieldsMatch('new_pass', 'chk_pass')
    ]
