# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: validators.py 11 2006-10-22 10:03:27Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/ispmanccp/models/validators.py $
# $LastChangedDate: 2006-10-22 11:03:27 +0100 (Sun, 22 Oct 2006) $
#             $Rev: 11 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

import re
import formencode
from pylons import request

class SecurePassword(formencode.FancyValidator):

    config = request.environ['paste.config']['app_conf']
    bad_passwords_file = config['bad_passwords_file'] or None
    min_length = int(config['passwords_min_length']) or 5
    min_non_letter = int(config['passwords_non_letter_min_chars']) or 1
    letter_regex = re.compile(r'[a-zA-Z]')

    messages = {
        'too_few': 'Your password must be longer than %(min_length)i '
                  'characters long',
        'non_letter': 'You must include at least %(min_non_letter)i '
                     'numeric character(s) in your password',
        'non_dict': 'Please do not base your password on a dictionary term',
    }

    def _to_python(self, value, state):
        # Strip any leading/trailing whitespace
        return value.strip()

    def validate_python(self, value, state):
        if len(value) < self.min_length:
            raise formencode.Invalid(self.message(
                "too_few", state, min_length=self.min_length), value, state)

        non_letters = self.letter_regex.sub('', value)
        if len(non_letters) < self.min_non_letter:
            raise formencode.Invalid(self.message(
                "non_letter", state, min_non_letter=self.min_non_letter),
                value, state)

        if self.bad_passwords_file is not None:
            f = open(self.bad_passwords_file)
            lower = value.strip().lower()
            for line in f:
                if line.strip().lower() == lower:
                    raise formencode.Invalid(self.message(
                        "non_dict", state), value, state)

