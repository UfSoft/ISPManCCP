# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: domain.py 10 2006-10-21 15:21:01Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/ispmanccp/controllers/domain.py $
# $LastChangedDate: 2006-10-21 16:21:01 +0100 (Sat, 21 Oct 2006) $
#             $Rev: 10 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

from ispmanccp.lib.base import *

class DomainController(BaseController):
    def index(self):
        self.domain = request.environ['REMOTE_USER']
        # Grab Domain Info
        dominfo = dict(g.ispman.getDomainInfo(self.domain).items())
        # Translate -1 to unlimited for more readability
        if dominfo['ispmanMaxVhosts'] == '-1':
            dominfo['ispmanMaxVhosts'] = 'unlimited'
        if dominfo['ispmanMaxAccounts'] == '-1':
            dominfo['ispmanMaxAccounts'] = 'unlimited'

        # Grab Current Accounts and VHosts Totals
        dominfo['ispmanVhosts'] = g.ispman.getVhostCount(self.domain)
        dominfo['ispmanAccounts'] = g.ispman.getUserCount(self.domain)

        c.dominfo = dominfo
        return render_response('domain.index')

    def changepass(self):
        if not request.POST:
            return render_response('domain.changepass')
