# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: index.py 2 2006-08-26 17:51:50Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/ispmanccp/controllers/index.py $
# $LastChangedDate: 2006-08-26 18:51:50 +0100 (Sat, 26 Aug 2006) $
#             $Rev: 2 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

from ispmanccp.lib.base import *

class IndexController(BaseController):
    def index(self):
        domain = request.environ['REMOTE_USER']
        # Grab Domain Info
        dominfo = dict(g.ispman.getDomainInfo(domain).items())
        # Translate -1 to unlimited for more readability
        if dominfo['ispmanMaxVhosts'] == '-1':
            dominfo['ispmanMaxVhosts'] = 'unlimited'
        if dominfo['ispmanMaxAccounts'] == '-1':
            dominfo['ispmanMaxAccounts'] = 'unlimited'

        # Grab Current Accounts and VHosts Totals
        dominfo['ispmanVhosts'] = g.ispman.getVhostCount(domain)
        dominfo['ispmanAccounts'] = g.ispman.getUserCount(domain)

        c.dominfo = dominfo
        return render_response('index.myt')
