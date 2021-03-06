"""The base Controller API

Provides the BaseController class for subclassing, and other objects
utilized by Controllers.
"""
from pylons import c, cache, config, g, request, response, session
from pylons.controllers import WSGIController
from pylons.controllers.util import abort, etag_cache, redirect_to
from pylons.decorators import rest
from pylons.decorators.cache import beaker_cache

from pylons.i18n import _, ungettext, N_
from pylons.templating import render

from pylonsgenshi.decorators import validate

import ispmanccp.lib.helpers as h
import ispmanccp.model as model


from ispmanccp.lib.ispman_helpers import *

# Helper to add ispman_helpers to __all__
def add_ispman_helpers(localdict):
    for name, func in localdict.iteritems():
        if callable(func) and \
           func.__module__.startswith('ispmanccp.lib.ispman_helpers'):
            __all__.append(name)


class BaseController(WSGIController):

    def __before__(self, *args, **kwargs):
        # Don't allow Locked Domains to make any changes
        if 'ispmanDomainLocked' in self.dominfo:
            if self.dominfo['ispmanDomainLocked'] == 'true' and \
               request.path_info != '/locked':
                redirect_to(h.url_for('/locked'))
            elif request.path_info == '/':
                redirect_to(h.url_for('/domain'))
        elif request.path_info == '/':
            redirect_to(h.url_for('/domain'))

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        # Grab Domain Info
        self.domain = request.environ['REMOTE_USER']
        self.dominfo = get_domain_info(self.domain)


        ccache = cache.get_cache('navigation')

        if session.has_key('lang'):
            c.menus = self.__create_i18n_menus(lang=session['lang'])
        else:
            c.menus = self.__create_i18n_menus()

        c.controller = request.environ['pylons.routes_dict']['controller']
        c.action = request.environ['pylons.routes_dict']['action']

        c.imgs_list = self.__images_list()

        if 'message' in session and session['message'] != '':
            c.message = session['message']
            session['message'] = ''
            session.save()
        return WSGIController.__call__(self, environ, start_response)

    @beaker_cache(expire=3600, type="memory", query_args=True)
    def __create_i18n_menus(self, lang=None):
        menulist = {}
        # App's Main Menu
        menulist['mainmenu'] = [
            (_(u'Home'), h.url_for(controller='domain', action='index', id=None)),
            (_(u'Accounts'), h.url_for(controller='accounts', action='index', id=None)),
        ]
        # Mail context menu
        menulist['accounts'] = [
            (_(u'Search Accounts'), h.url_for(controller='accounts', action='index', id=None)),
            (_(u'New Account'), h.url_for(controller='accounts', action='new', id=None)),
        ]

        # Domain context menu
        menulist['domain'] = [
            (_(u'Domain Overview'),
             h.url_for(controller="domain", action="index", id=None)),
            (_(u'Change Domain Password'),
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


    # Cache for a day, altough, we should never need to expire this.
    @beaker_cache(expire=86400)
    def __images_list(self):
        """Internal function to create an images list to be pre-lodaded(fed to a JS function)."""
        import os
        from webhelpers.rails.asset_tag import compute_public_path
        from pkg_resources import resource_filename
        img_list = []
        img_dir = os.path.join(resource_filename('ispmanccp', 'public'), 'images')
        for img in os.listdir(img_dir):
            if os.path.splitext(img)[1].lower() in ('.png', '.jpg', '.gif'):
                img_list.append(compute_public_path(img, 'images'))
        return img_list

# Include the '_' function in the public names
__all__ = [__name for __name in locals().keys() if not __name.startswith('_') \
           or __name == '_']

# Add ispman_helpers to __all__
add_ispman_helpers(locals())
