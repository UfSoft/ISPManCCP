# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: app_globals.py 2 2006-08-26 17:51:50Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/ispmanccp/lib/app_globals.py $
# $LastChangedDate: 2006-08-26 18:51:50 +0100 (Sat, 26 Aug 2006) $
#             $Rev: 2 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

class Globals(object):

    def __init__(self, global_conf, app_conf, **extra):
        """
        You can put any objects which need to be initialised only once
        here as class attributes and they will be available as globals
        everywhere in your application and will be intialised only once,
        not on every request.

        ``global_conf``
            The same as variable used throughout ``config/middleware.py``
            namely, the variables from the ``[DEFAULT]`` section of the
            configuration file.

        ``app_conf``
            The same as the ``kw`` dictionary used throughout 
            ``config/middleware.py`` namely, the variables the section 
            in the config file for your application.

        ``extra``
            The configuration returned from ``load_config`` in 
            ``config/middleware.py`` which may be of use in the setup of 
            your global variables.

        """
        import os
        import perl

        # Get Perl's @INC reference
        inc = perl.get_ref("@INC")

        ispman_installdir = os.path.abspath(app_conf['ispman_base_dir'])

        # Add all ISPMan directories to perl's @INC
        for dirname in os.listdir(ispman_installdir):
            if os.path.isdir(os.path.join(ispman_installdir, dirname)):
                inc.append(os.path.join(ispman_installdir, dirname))

        # Setup an ISPMan instance
        perl.require('ISPMan')
        try:
            self.ispman = perl.eval('$ispman = ISPMan->new() or die "$@"')
        except Exception, e:
            print e

        # Setup an LDAP connection, which will only be used for
        # initial authentication purposes
        import ldap
        ldap_host = self.ispman.getConf('ldapHost')
        ldap_version = self.ispman.getConf('ldapVersion')
        self.ldap = ldap.initialize("ldap://%s:389" % ldap_host)
        self.ldap.protocol_version = int(ldap_version)

        # Also pass the perl reference for further use within the app
        self.perl = perl
        pass

    def __del__(self):
        """
        Put any cleanup code to be run when the application finally exits 
        here.
        """
        pass
