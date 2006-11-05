# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: base.py 34 2006-11-05 18:57:20Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/ispmanccp/lib/base.py $
# $LastChangedDate: 2006-11-05 18:57:20 +0000 (Sun, 05 Nov 2006) $
#             $Rev: 34 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

__all__ = ['Response', 'c', 'g', 'cache', 'request', 'session', 'validate',
           'WSGIController', 'jsonify', 'rest', 'render', 'render_response',
           'abort', 'redirect_to', 'etag_cache', '_', 'model', 'h', 
           'BaseController']

from pylons import Response, c, g, cache, request, session
from pylons.controllers import WSGIController
from pylons.decorators import jsonify, rest
from pylons.templating import render, render_response
from pylons.helpers import abort, redirect_to, etag_cache
from pylons.util import _
import ispmanccp.models as model
import ispmanccp.lib.helpers as h
from ispmanccp.lib.decorators import validate
from ispmanccp.lib.ispman_helpers import *

# Add ispman_helpers to __all__
def add_ispman_helpers(localdict):
    for name, func in localdict.iteritems():
        if callable(func) and \
           func.__module__.startswith('ispmanccp.lib.ispman_helpers'):
            __all__.append(name)

add_ispman_helpers(locals())

class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        # Insert any code to be run per request here. The Routes match
        # is under environ['pylons.routes_dict'] should you want to check
        # the action or route vars here

        # Grab Domain Info
        self.domain = request.environ['REMOTE_USER']
        self.dominfo = get_domain_info(self.domain)

        # Don't allow Locked Domains to make any changes
        if self.dominfo['ispmanDomainLocked'] == 'true' and \
           request.path_info != '/locked':
            h.redirect_to('/locked')
        elif request.path_info == '/':
            h.redirect_to('/domain')

        ccache = cache.get_cache('navigation')

        c.menus = ccache.get_value('i18n_menus',
                                  createfunc=self.__create_i18n_menus,
                                  type='memory', expiretime=3600)

        c.controller = request.environ['pylons.routes_dict']['controller']
        c.action = request.environ['pylons.routes_dict']['action']

        if 'message' in session and session['message'] != '':
            c.message = session['message']
            session['message'] = ''
            session.save()
        return WSGIController.__call__(self, environ, start_response)


    def __create_i18n_menus(self):
        menulist = {}
        # App's Main Menu
        menulist['mainmenu'] = [
            (_('Home'), h.url_for(controller='domain', action='index', id=None)),
            (_('Accounts'), h.url_for(controller='accounts', action='index', id=None)),
        ]
        # Mail context menu
        menulist['accounts'] = [
            (_('Search Accounts'), h.url_for(controller='accounts', action='index', id=None)),
            (_('New Account'), h.url_for(controller='accounts', action='new', id=None)),
        ]

        # Domain context menu
        menulist['domain'] = [
            (_('Domain Overview'),
             h.url_for(controller="domain", action="index", id=None)),
            (_('Change Domain Password'),
             h.url_for(controller="domain", action="changepass", id=None))
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

