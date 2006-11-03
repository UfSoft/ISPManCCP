# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: base.py 26 2006-11-03 19:29:49Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/ispmanccp/lib/base.py $
# $LastChangedDate: 2006-11-03 19:29:49 +0000 (Fri, 03 Nov 2006) $
#             $Rev: 26 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

from pylons import Response, c, g, h, cache, request, session
from pylons.controllers import WSGIController
from pylons.decorators import jsonify, rest
from pylons.templating import render, render_response
from pylons.helpers import abort, redirect_to, etag_cache
import ispmanccp.models as model
from ispmanccp.lib.ispman_helpers import *
from ispmanccp.lib.forms import Form

from ispmanccp.lib.decorators import validate

class BaseController(WSGIController):
    def __call__(self, environ, start_response):
        # Insert any code to be run per request here. The Routes match
        # is under environ['pylons.routes_dict'] should you want to check
        # the action or route vars here
        if request.path_info == '/':
            h.redirect_to('/domain')

        ccache = cache.get_cache('navigation')

        c.menus = ccache.get_value('i18n_menus',
                                  createfunc=self.__create_i18n_menus,
                                  type='memory', expiretime=3600)

        c.controller = request.environ['pylons.routes_dict']['controller']
        c.action = request.environ['pylons.routes_dict']['action']

        c.form = Form()
        if 'message' in session and session['message'] != '':
            c.message = session['message']
            session['message'] = ''
            session.save()
        return WSGIController.__call__(self, environ, start_response)

    def __create_i18n_menus(self):
        menulist = {}
        # App's Main Menu
        menulist['mainmenu'] = [
            (h._('Home'), h.url_for(controller='domain', action='index', id=None)),
            (h._('Mail'), h.url_for(controller='mail', action='index', id=None)),
        ]
        # Mail context menu
        menulist['mail'] = [
            (h._('Accounts'), h.url_for(controller='mail', action='index', id=None)),
            (h._('New Account'), h.url_for(controller='mail', action='new', id=None)),
        ]

        # Domain context menu
        menulist['domain'] = [
            (h._('Domain Overview'),
             h.url_for(controller="domain", action="index")),
            (h._('Change Domain Password'),
             h.url_for(controller="domain", action="changepass"))
        ]
        keys = {}
        menus = {}
        for key, val in menulist.items():
            menus[key] = []
            for name, url in val:
                for n in range(len(name)):
                    if name[n].upper() not in [x.upper() for x in keys.values() if x != None]:
                        keys[name] = name[n]
                        break
                    else:
                        n += 1
                else:
                    keys[name] = None
                menus[key].append((name, url, keys[name]))
        return menus
