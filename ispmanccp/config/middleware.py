# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: middleware.py 34 2006-11-05 18:57:20Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/ispmanccp/config/middleware.py $
# $LastChangedDate: 2006-11-05 18:57:20 +0000 (Sun, 05 Nov 2006) $
#             $Rev: 34 $
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
from paste.deploy.converters import asbool

from pylons.error import error_template
from pylons.middleware import ErrorHandler, ErrorDocuments, StaticJavascripts, error_mapper
import pylons.wsgiapp

from ispmanccp.config.environment import load_environment
import ispmanccp.lib.helpers
import ispmanccp.lib.app_globals as app_globals

def make_app(global_conf, full_stack=True, **app_conf):
    """Create a WSGI application and return it

    global_conf is a dict representing the Paste configuration options, the
    paste.deploy.converters should be used when parsing Paste config options
    to ensure they're treated properly.

    """
    # Load our Pylons configuration defaults
    config = load_environment(global_conf, app_conf)
    config.init_app(global_conf, app_conf, package='ispmanccp')

    # Setup Genshi(only) Template Engine
    config.template_engines = []
    config.add_template_engine('genshi', 'ispmanccp.templates', {})

    # Load our default Pylons WSGI app and make g available
    app = pylons.wsgiapp.PylonsApp(config, helpers=ispmanccp.lib.helpers,
                                   g=app_globals.Globals)
    g = app.globals
    app = ConfigMiddleware(app, {'app_conf':app_conf, 'global_conf':global_conf})

    # YOUR MIDDLEWARE
    # Put your own middleware here, so that any problems are caught by the error
    # handling middleware underneath

    # If errror handling and exception catching will be handled by middleware
    # for multiple apps, you will want to set full_stack = False in your config
    # file so that it can catch the problems.
    if asbool(full_stack):
        # Change HTTPExceptions to HTTP responses
        app = httpexceptions.make_middleware(app, global_conf)

        # Error Handling
        app = ErrorHandler(app, global_conf, error_template=error_template, **config.errorware)

        # Display error documents for 401, 403, 404 status codes (if debug is disabled also
        # intercepts 500)
        app = ErrorDocuments(app, global_conf, mapper=error_mapper, **app_conf)

    # Establish the Registry for this application
    app = RegistryManager(app)

    static_app = StaticURLParser(config.paths['static_files'])
    javascripts_app = StaticJavascripts()
    app = Cascade([static_app, javascripts_app, app])

    def authenticate(aplication, domain, password):
        domaindn = 'ispmanDomain=' + domain + ',' + app_conf['ispman_ldap_base_dn']
        try:
            g.ldap.simple_bind_s(who=domaindn, cred=password)
            return True
        except Exception, e:
            print "Failed LDAP bind for domain '%s': %s." % \
                    (domain, e[0]['desc'])
            return False

    from paste.auth.basic import AuthBasicHandler
    app = AuthBasicHandler(app, app_conf['app_realm'], authenticate)

    return app
