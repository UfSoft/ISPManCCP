# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: accounts.py 137 2008-01-27 07:00:17Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/ispmanccp/model/accounts.py $
# $LastChangedDate: 2008-01-27 07:00:17 +0000 (Sun, 27 Jan 2008) $
#             $Rev: 137 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

from pylons.i18n import _
from formencode import Schema, validators, ForEach, All
from ispmanccp.model.validators import *

__all__ = ['AccountUpdate', 'AccountDelete', 'AccountCreate']

try:
    import DNS
    dns_available = True
except ImportError:
    dns_available = False


class AccountUpdate(Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    ispmanDomain = validators.UnicodeString(not_empty=True, encoding='UTF-8')
    uid = validators.UnicodeString(not_empty=True, encoding='UTF-8')
    givenName = CorrectNamesValidator(not_empty=True, strip=True, encoding='UTF-8')
    sn = CorrectNamesValidator(not_empty=True, strip=True, encoding='UTF-8')
    userPassword = SecurePassword(
        not_empty=True, strip=True,
        messages={'empty': _("Please enter a value or click button to restore password")}
    )
    userPasswordConfirm = PasswordsMatch(not_empty=False, strip=True)
    FTPQuotaMBytes = validators.Int(not_empty=False, strip=True)
    FTPStatus = validators.OneOf([u'enabled', u'disabled'])
    mailQuota = validators.Int(not_empty=False, strip=True)
    mailAlias = ForEach(ValidMailAlias(not_empty=True, strip=True))
    mailForwardingAddress = ForEach(
        validators.Email(not_empty=True,
                         strip=True,
                         resolve_domain=dns_available)
    )
    ForwardingOnly = ForwardingOnlyValidator(not_empty=True)


class AccountDelete(Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    ispmanDomain = validators.UnicodeString(not_empty=True, encoding='UTF-8')
    uid = validators.UnicodeString(not_empty=True, encoding='UTF-8')


class AccountCreate(Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    ispmanDomain = validators.UnicodeString(not_empty=True, encoding='UTF-8')
    uid = validators.UnicodeString(not_empty=True, encoding='UTF-8')
    givenName = CorrectNamesValidator(not_empty=True, strip=True, encoding='UTF-8')
    sn = CorrectNamesValidator(not_empty=True, strip=True, encoding='UTF-8')
    userPassword = SecurePassword(
        not_empty=True, strip=True,
        messages={'empty': _("Please enter a value or click button to regenerate password")}
    )
    ispmanUserId = UniqueUserId(not_empty=True, strip=True, encoding='UTF-8')
    FTPQuotaMBytes = validators.Int(not_empty=False, strip=True)
    FTPStatus = validators.OneOf([u'enabled', u'disabled'])
    mailQuota = validators.Int(not_empty=False, strip=True)
    mailAlias = ForEach(ValidMailAlias(not_empty=True, strip=True))#, unique=True)
    mailForwardingAddress = ForEach(
        validators.Email(not_empty=True,
                         strip=True,
                         resolve_domain=dns_available)
    )
