# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: ispman_helpers.py 5 2006-09-01 19:30:14Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/ispmanccp/lib/ispman_helpers.py $
# $LastChangedDate: 2006-09-01 20:30:14 +0100 (Fri, 01 Sep 2006) $
#             $Rev: 5 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

from pylons import request, g

def get_users_list(id, sortby=None, sort_ascending=True):
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

    usertuple = ()
    userlist = []
    userdict = {}
    for user, vals in domain_users.items():
        # add the dn since the user data does not carry that info
        vals['dn'] = user
        user_id = vals['ispmanUserId']
        if id == 'all':
            userdict[user]=vals
            usertuple += (user, dict(vals))
            userlist.append(dict(vals))
        elif user_id.upper().startswith(id):
            usertuple += (user, dict(vals))
            userdict[user]=vals
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
