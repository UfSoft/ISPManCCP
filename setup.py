#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: setup.py 56 2006-11-15 08:06:55Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/setup.py $
# $LastChangedDate: 2006-11-15 08:06:55 +0000 (Wed, 15 Nov 2006) $
#             $Rev: 56 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

from setuptools import setup, find_packages

try:
    # Let's find out if we have python-ldap
    import ldap
except ImportError:
    # We don't have python-ldap, exit nicely
    from sys import exit
    print
    print "You must have the python-ldap module instaled."
    print "Most distributions already provide it, just install it."
    print "As an alternative, you can get it from:"
    print "   http://python-ldap.sourceforge.net/"
    print
    exit(1)

def setup_pyperl():
    """Function that call's pyperl's setup.py"""
    import os, subprocess
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.join(cur_dir, 'extra-packages', 'pyperl-1.0.1d'))
    retcode = subprocess.call(['python', './setup.py', 'install'])
    os.chdir(cur_dir)


try:
    # Let's find out if we have PyPerl installed
    import perl
except ImportError:
    # We don't have PyPerl, so, install it
    setup_pyperl()


# We now resume normal setup operation


VERSION = "0.1"
DESCRIPTION = """
==========================================
ISPManCCP - ISPMan Customer Control Pannel
==========================================

ISPManCCP is a customer control pannel to use with
`ISPMan <http://ispman.net>`_.

It's the alternative to the deprecated customer control pannel included with
`ISPMan <http://ispman.net>`_.

Current features
----------------
**Change Domain Password**

- Enforce passwords with a minumum 5 char's lenght;
- Enforce at least one number in the password;
- Make sure a user is not using a word from a dictionary(words file can be
  setup, for example, the cracklib file);

**Edit User Accounts**

- No remote mail aliases are allowed, ie, only aliases for the same domain;
- Email forwards are checked for valid DNS MX reccords;
- No underscores nor numbers are allowed for first and last names;
- Change mail quota;
- Change FTP quota and status;

You can find more info on the
`ISPManCCP <http://ccp.ufsoft.org/>`_ site where bugs and new feature requests
should go to.

Download and Installation
-------------------------

WikiTemplates can be installed with `Easy Install
<http://peak.telecommunity.com/DevCenter/EasyInstall>`_ by typing::

    > easy_install ISPManCCP

"""
setup(
    name = 'ISPManCCP',
    version = VERSION,
    description = "Customer Control Pannel for ISPMan",
    long_description = DESCRIPTION,
    license = 'BSD',
    platforms = "Anywhere you've got ISPMan working.",
    author = "Pedro Algarvio",
    author_email = "ufs@ufsoft.org",
    url = "http://ccp.ufsoft.org/",
    download_url = "http://ccp.ufsoft.org/download/%s/" % VERSION,
    zip_safe = False,
    install_requires = [
        "pyperl>=1.0.1c",
        "Pylons>=0.9.3",
        "Genshi>=0.3.4",
        "formencode>=0.6",
    ],
    packages = find_packages(),
    include_package_data = True,
    test_suite = 'nose.collector',
    package_data = {'ispmanccp': ['i18n/*/LC_MESSAGES/*.mo']},
    entry_points = """
    [paste.app_factory]
    main=ispmanccp:make_app
    [paste.app_install]
    main=paste.script.appinstall:Installer
    """,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Customer Service',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Natural Language :: Portuguese',
        'Programming Language :: Python',
        'Programming Language :: Perl',
        'Topic :: Database :: Front-Ends',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Utilities',
    ],
    keywords = "ISPMan PyPerl Python Customer Control Pannel"

)
