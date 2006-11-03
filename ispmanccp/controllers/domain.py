# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: domain.py 27 2006-11-03 23:09:28Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/ispmanccp/controllers/domain.py $
# $LastChangedDate: 2006-11-03 23:09:28 +0000 (Fri, 03 Nov 2006) $
#             $Rev: 27 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

from ispmanccp.models.domain import ChangeDomainPassword
from ispmanccp.lib.base import *

class DomainController(BaseController):
    # Grab Domain Info
    domain = request.environ['REMOTE_USER']
    dominfo = dict(g.ispman.getDomainInfo(domain).items())

    def index(self):
        # Translate -1 to unlimited for more readability
        if self.dominfo['ispmanMaxVhosts'] == '-1':
            self.dominfo['ispmanMaxVhosts'] = _('unlimited')
        if self.dominfo['ispmanMaxAccounts'] == '-1':
            self.dominfo['ispmanMaxAccounts'] = _('unlimited')

        # Grab Current Accounts and VHosts Totals
        self.dominfo['ispmanVhosts'] = g.ispman.getVhostCount(self.domain)
        self.dominfo['ispmanAccounts'] = g.ispman.getUserCount(self.domain)
        c.dominfo = self.dominfo
        return render_response('domain.index')

    @rest.dispatch_on(POST='changepass_post')
    def changepass(self):
        c.dominfo = self.dominfo
        return render_response('domain.changepass')

    @validate(template='domain.changepass', schema=ChangeDomainPassword(), form='changepass')
    def changepass_post(self):
        if request.method == 'GET':
            return redirect_to(action='changepass')

        domain = request.POST['ispmanDomain']
        passwd = request.POST['new_pass']
        print "Changing password for domain '%s'. LDAP Bind will fail shortly." % domain
        retcode = g.ispman.changeDomainPassword(domain, passwd)
        if retcode != 1:
            session['message'] = _('Problems occured while changing password.')
            session.save()
            return redirect_to(action='changepass')

        session['message'] = _('Operation successfull.')
        session.save()
        return redirect_to(action='index')

