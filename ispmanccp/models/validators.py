# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: validators.py 26 2006-11-03 19:29:49Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/ispmanccp/models/validators.py $
# $LastChangedDate: 2006-11-03 19:29:49 +0000 (Fri, 03 Nov 2006) $
#             $Rev: 26 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

import re
from formencode import validators, FancyValidator, Invalid
from pylons import request, h, g


class CurrentPassword(FancyValidator):
    """ Validator to check the domain's current password."""
    def _to_python(self, value, state):
        # Strip any leading/trailing whitespace
        return value.strip()

    def validate_python(self, value, state):
        ldap_pass = g.ispman.getDomainAttribute(
            request.POST['ispmanDomain'], 'userPassword').strip()
        coded_pass = g.ispman.encryptPassWithMethod(
            value, g.ispman.getConf('userPassHashMethod')).strip()
        if coded_pass != ldap_pass:
            raise Invalid(h._("Current password not correct"),
                                     value, state)

class PasswordsMatch(validators.UnicodeString):
    """ Validator that does not complain about the empty value. This is to
    allow the update of a user's account, which if pass is the same as the
    stored one, no modification is made. If a value is found, then check
    against the first value and fail if they dont match."""
    def validate_python(self, value, state):
        if value is '':
            return value

        to_match = request.POST['userPassword']
        if value != to_match:
            raise Invalid(h._("Passwords do not match."), value, state)


class SecurePassword(validators.UnicodeString):
    """Validator to enforce some minimaly secure passwords."""

    config = request.environ['paste.config']['app_conf']
    bad_passwords_file = config['bad_passwords_file'] or None
    min_length = int(config['passwords_min_length']) or 5
    min_non_letter = int(config['passwords_non_letter_min_chars']) or 1
    letter_regex = re.compile(r'[a-zA-Z]')

    messages = {
        'too_few': h._(
            'Your password must be longer than %(min_length)i characters long'
        ),
        'non_letter': h._(
            'You must include at least %(min_non_letter)i numeric '
                     'character(s) in your password'),
        'non_dict': h._(
            'Please do not base your password on a dictionary term'),
    }

    def _to_python(self, value, state):
        # Strip any leading/trailing whitespace
        return value.strip()

    def validate_python(self, value, state):
        if len(value) < self.min_length:
            raise Invalid(self.message(
                "too_few", state, min_length=self.min_length), value, state)

        non_letters = self.letter_regex.sub('', value)
        if len(non_letters) < self.min_non_letter:
            raise Invalid(self.message(
                "non_letter", state, min_non_letter=self.min_non_letter),
                value, state)

        if self.bad_passwords_file is not None:
            f = open(self.bad_passwords_file)
            lower = value.strip().lower()
            for line in f:
                if line.strip().lower() == lower:
                    raise Invalid(self.message(
                        "non_dict", state), value, state)


class ValidMailAlias(validators.Email):
    """Validator that checks if the alias being added is for the same
    domain. We won't allow alias to remote emails."""

    messages = {
        'same_domain': h._(
            "The alias must be kept under the same domain: %(domain)s"
        )
    }

    def validate_python(self, value, state):
        domain = request.POST['ispmanDomain']
        if not value.endswith(domain):
            raise Invalid(self.message('same_domain', state, domain=domain),
                          value, state)
        validators.Email.validate_python(self, value, state)


class CorrectNamesValidator(validators.UnicodeString):
    """Validator for person's names, which normally don't include numbers,
    underscores, etc. We do although, allow spaces in case we'd like to add
    more than one name, ie, FirstName: Steve Jonas, LastName: Alchemy."""

    messages = {
        'not_valid': h._('%(chars)s %(plural)s not allowed on names.')
    }

    def validate_python(self, value, state):
        validators.UnicodeString.validate_python(self, value, state)
        if value:
            chars = re.findall(r'[^\w\s]|[0-9]|[_]', value, re.U)
            if chars:
                if len(chars) == 1:
                    plural = h._('is')
                else:
                    plural = h._('are')
                chars =  u''.join(chars)
                raise Invalid(
                    self.message(
                        'not_valid', state, chars=chars, plural=plural
                    ), value, state)
