# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: ispman_helpers.py 24 2006-10-25 03:07:42Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/ispmanccp/lib/ispman_helpers.py $
# $LastChangedDate: 2006-10-25 04:07:42 +0100 (Wed, 25 Oct 2006) $
#             $Rev: 24 $
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

    # let's save some time and return right away if we don't need any sorting
    if len(userlist) <= 1:
        return userlist

    decorated = [(dict_[sortby], dict_) for dict_ in userlist]
    decorated.sort()

    if not sort_ascending:
        decorated.reverse()
    result = [dict_ for (key, dict_) in decorated]
    return result


def get_user_info(uid, domain):
    user_info = dict(g.ispman.getUserInfo(uid, domain))
    return user_info

