# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: mail.py 6 2006-10-20 10:41:43Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/ispmanccp/controllers/mail.py $
# $LastChangedDate: 2006-10-20 11:41:43 +0100 (Fri, 20 Oct 2006) $
#             $Rev: 6 $
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
        import string
        self.form_letters = ['All']
        self.form_letters.extend(list(string.digits + string.uppercase))
        c.form_letters = self.form_letters
        return render_response('mail.index')

    def userlist(self):
        sort_by = request.POST['sort_by']
        sort_how = bool(request.POST['sort_how'])

        if 'letter' in request.POST:
            start_letter = request.POST['letter']
        else:
            start_letter = 'All'

        if 'None' in request.POST['letter']:
            c.users = []
            return render_response('mail.snippets.userlist')

        userlist = get_users_list(start_letter, sortby=sort_by, sort_ascending=sort_how)

        if not userlist:
            c.error = h._("No results retrieved.")
        else:
            c.users = userlist
        return render_response('mail.snippets.userlist')

    def new(self):
        return render_response('mail.myt')

    def edit(self, dn):
        pass
