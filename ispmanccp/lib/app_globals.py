"""The application's Globals object"""
import os
import sys
from pylons import config
from ispmanccp.lib.helpers import check_path_perms

class Globals(object):
    """Globals acts as a container for objects available throughout the
    life of the application
    """

    def __init__(self):
        """One instance of Globals is created during application
        initialization and is available during requests via the 'g'
        variable
        """
        ispman_installdir = os.path.abspath(config['app_conf']['ispman_base_dir'])
        check_path_perms(ispman_installdir)

        try:
            import perl
        except ImportError:
            print "You need the pyperl module installed."
            print "You can get it from:"
            print "   http://www.felix-schwarz.name/files/opensource/pyperl/"
            sys.exit(1)

        # Get Perl's @INC reference
        inc = perl.get_ref("@INC")

        # Add ISPMan lib directory to perl's @INC
        ispman_libs = os.path.join(ispman_installdir, 'lib')
        check_path_perms(ispman_libs)
        inc.append(ispman_libs)
        # Setup an ISPMan instance
        perl.require('ISPMan')
        perl.require('CGI')

        try:
            # Make ISPMan recognize us as a Control Panel
            self.ispman = perl.eval(
                '$ENV{"HTTP_USER_AGENT"} = "PYTHON-CCP"; ' +
                '$ispman = ISPMan->new() or die "$@"'
            )
        except Exception, e:
            print e

        self.ldap_host = self.ispman.getConf('ldapHost')
        self.ldap_version = self.ispman.getConf('ldapVersion')
        self.ldap_base_dn = self.ispman.getConfig('ldapBaseDN')

        # Also pass the perl reference for further use within the app
        self.perl = perl
        pass
