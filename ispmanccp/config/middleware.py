# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: middleware.py 2 2006-08-26 17:51:50Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/ispmanccp/config/middleware.py $
# $LastChangedDate: 2006-08-26 18:51:50 +0100 (Sat, 26 Aug 2006) $
#             $Rev: 2 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

from paste import httpexceptions
from paste.cascade import Cascade
from paste.urlparser import StaticURLParser
from paste.registry import RegistryManager
from paste.deploy.config import ConfigMiddleware

from pylons.error import error_template
from pylons.middleware import ErrorHandler, ErrorDocuments, StaticJavascripts, error_mapper
import pylons.wsgiapp

from ispmanccp.config.environment import load_environment

def make_app(global_conf, **app_conf):
    """Create a WSGI application and return it

    global_conf is a dict representing the Paste configuration options, the
    paste.deploy.converters should be used when parsing Paste config options
    to ensure they're treated properly.

    """
    # Load our Pylons configuration defaults
    config = load_environment()
    config.init_app(global_conf, app_conf, package='ispmanccp')

    # Load our default Pylons WSGI app and make g available
    app = pylons.wsgiapp.PylonsApp(config)
    g = app.globals
    app = ConfigMiddleware(app, {'app_conf':app_conf,
        'global_conf':global_conf})

    # YOUR MIDDLEWARE
    # Put your own middleware here, so that any problems are caught by the error
    # handling middleware underneath

    # @@@ Change HTTPExceptions to HTTP responses @@@
    app = httpexceptions.make_middleware(app, global_conf)

    # @@@ Error Handling @@@
    app = ErrorHandler(app, global_conf, error_template=error_template, **config.errorware)

    # @@@ Static Files in public directory @@@
    static_app = StaticURLParser(config.paths['static_files'])

    # @@@ WebHelper's static javascript files @@@
    javascripts_app = StaticJavascripts()

    # @@@ Cascade @@@ 
    app = Cascade([static_app, javascripts_app, app])

    # @@@ Display error documents for 401, 403, 404 status codes (if debug is disabled also
    # intercepts 500) @@@
    app = ErrorDocuments(app, global_conf, mapper=error_mapper, **app_conf)

    # @@@ Establish the Registry for this application @@@
    app = RegistryManager(app)

    def authenticate(aplication, domain, password):
        domaindn = 'ispmanDomain=' + domain + ',' + app_conf['ispman_ldap_base_dn']
        try:
            g.ldap.simple_bind_s(who=domaindn, cred=password)
            return True
        except Exception, e:
            print "Failed LDAP bind: %s" % e
            return False

    from paste.auth.basic import AuthBasicHandler
    app = AuthBasicHandler(app, app_conf['app_realm'], authenticate)

    return app
