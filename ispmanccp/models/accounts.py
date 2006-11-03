# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: accounts.py 28 2006-11-03 23:24:04Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/ispmanccp/models/accounts.py $
# $LastChangedDate: 2006-11-03 23:24:04 +0000 (Fri, 03 Nov 2006) $
#             $Rev: 28 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

from formencode import Schema, validators, ForEach, All
from ispmanccp.models.validators import *

try:
    import DNS
    dns_available = True
except ImportError:
    dns_available = False

class MailAccountUpdate(Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    ispmanDomain = validators.UnicodeString(not_empty=True, encoding='UTF-8')
    uid = validators.UnicodeString(not_empty=True, encoding='UTF-8')
    givenName = CorrectNamesValidator(not_empty=True, strip=True, encoding='UTF-8')
    sn = CorrectNamesValidator(not_empty=True, strip=True, encoding='UTF-8')
    userPassword = SecurePassword(
        not_empty=True, strip=True,
        messages={'empty': "Please enter a value or click button to restore password"}
    )
    userPasswordConfirm = PasswordsMatch(not_empty=False, strip=True)
    mailQuota = validators.Int(not_empty=False, strip=True)
    mailAlias = ForEach(ValidMailAlias(not_empty=True, strip=True))
    mailForwardingAddress = ForEach(
        validators.Email(not_empty=True,
                         strip=True,
                         resolve_domain=dns_available)
    )
