# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: mail.py 5 2006-09-01 19:30:14Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/ispmanccp/controllers/mail.py $
# $LastChangedDate: 2006-09-01 20:30:14 +0100 (Fri, 01 Sep 2006) $
#             $Rev: 5 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

from ispmanccp.lib.base import *
from ispmanccp.lib.forms import Form

class MailController(BaseController):

    def index(self):
        return render_response('mail.myt')

    def userlist(self, id=None):
        sort_by = request.POST['sort_by']
        sort_how = bool(request.POST['sort_how'])

        if 'letter' in request.POST:
            start_letter = request.POST['letter']
        else:
            start_letter = 'all'

        userlist = get_users_list(start_letter, sortby=sort_by, sort_ascending=sort_how)

        if not userlist:
            c.error = h._("No results retrieved.")
        else:
            c.users = userlist
        return render_response('mail_userlist.myt', fragment=True)

    def new(self):
        return render_response('mail.myt')
