# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: ispman_helpers.py 6 2006-10-20 10:41:43Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/ispmanccp/lib/ispman_helpers.py $
# $LastChangedDate: 2006-10-20 11:41:43 +0100 (Fri, 20 Oct 2006) $
#             $Rev: 6 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

from pylons import request, g

def get_users_list(letter, sortby=None, sort_ascending=True):
    domain_users = dict(g.ispman.getUsers(
        request.environ['REMOTE_USER'], [
            "dn",
            "givenName",
            "surname",
            "ispmanCreateTimestamp",
            "ispmanUserId",
            "mailLocalAddress",
            "mailForwardingAddress",
            "userPassword",
            "mailQuota",
            "mailAlias"
        ]
    ))

    userlist = []
    for user, vals in domain_users.items():
        # add the dn since the user data does not carry that info
        vals['dn'] = user
        user_id = vals['ispmanUserId']
        if letter == 'All':
            userlist.append(dict(vals))
        elif user_id.upper().startswith(letter):
            userlist.append(dict(vals))
    if sortby:
        decorated = [(dict_[sortby], dict_) for dict_ in userlist]
        if sort_ascending:
            decorated.sort()
        else:
            decorated.sort(reversed=True)
        result = [dict_ for (key, dict_) in decorated]
    else:
        decorated = [(dict_['ispmanUserId'], dict_) for dict_ in userlist]
        if sort_ascending:
            decorated.sort()
        else:
            decorated.sort(reversed=True)
        result = [dict_ for (key, dict_) in decorated]
    return result
