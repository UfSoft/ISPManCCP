# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: domain.py 12 2006-10-22 14:19:41Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/ispmanccp/controllers/domain.py $
# $LastChangedDate: 2006-10-22 15:19:41 +0100 (Sun, 22 Oct 2006) $
#             $Rev: 12 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

import formencode
from ispmanccp.models.domain import ChangeDomainPassword
from ispmanccp.lib.base import *

class DomainController(BaseController):
    domain = request.environ['REMOTE_USER']
    dominfo = dict(g.ispman.getDomainInfo(domain).items())

    def index(self):
        #self.domain = request.environ['REMOTE_USER']
        # Grab Domain Info
        #dominfo = dict(g.ispman.getDomainInfo(self.domain).items())
        # Translate -1 to unlimited for more readability
        if self.dominfo['ispmanMaxVhosts'] == '-1':
            self.dominfo['ispmanMaxVhosts'] = 'unlimited'
        if self.dominfo['ispmanMaxAccounts'] == '-1':
            self.dominfo['ispmanMaxAccounts'] = 'unlimited'

        # Grab Current Accounts and VHosts Totals
        self.dominfo['ispmanVhosts'] = g.ispman.getVhostCount(self.domain)
        self.dominfo['ispmanAccounts'] = g.ispman.getUserCount(self.domain)
        c.dominfo = self.dominfo
        return render_response('domain.index')

    @rest.dispatch_on(POST='changepass_post')
    def changepass(self):
        c.dominfo = self.dominfo
        return render_response('domain.changepass')

    @validate(template='domain.changepass', schema=ChangeDomainPassword(), form='changepass', state=g)
    def changepass_post(self):
        domain = request.POST['domain']
        passwd = request.POST['new_pass']
        print "Changing password for domain '%s'. LDAP Bind will fail shortly." % domain
        res = g.ispman.changeDomainPassword(domain, passwd)

        return redirect_to(action='index')

