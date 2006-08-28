# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: mail.py 4 2006-08-28 14:00:08Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/ispmanccp/controllers/mail.py $
# $LastChangedDate: 2006-08-28 15:00:08 +0100 (Mon, 28 Aug 2006) $
#             $Rev: 4 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

from ispmanccp.lib.base import *
from ispmanccp.lib.forms import Form

class MailController(BaseController):
#    c.ctxnav = [
#        ('Accounts Index', '/mail/index', 'A'),
#        ('New Account', '/mail/new', 'N')
#    ]

    def index(self):
        return render_response('mail.myt')

    def userlist(self, id):
        domain_users = dict(g.ispman.getUsers(
            request.environ['REMOTE_USER'], [
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
        userdict = {}
        for user, val in domain_users.items():
            user_id = val['ispmanUserId']
            if user_id.upper().startswith(id):
                userdict[user_id]=val

        if not userdict:
            c.error = h._("No results retrieved.")
        else:
            c.users = userdict
            c.form = Form()
        return render_response('mail_userlist.myt', fragment=True)

    def new(self):
        return render_response('mail.myt')
