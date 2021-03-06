#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: setup.py 137 2008-01-27 07:00:17Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/setup.py $
# $LastChangedDate: 2008-01-27 07:00:17 +0000 (Sun, 27 Jan 2008) $
#             $Rev: 137 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

from sys import exit
from setuptools import setup, find_packages

try:
    # Let's find out if we have python-ldap
    import ldap
except ImportError:
    # We don't have python-ldap, exit nicely
    print
    print "You must have the python-ldap module instaled."
    print "Most distributions already provide it, just install it."
    print "As an alternative, you can get it from:"
    print "   http://python-ldap.sourceforge.net/"
    print
    exit(1)


try:
    # Let's find out if we have PyPerl installed
    import perl
    if perl.MULTI_PERL:
        print
        print "You already have PyPerl installed but it's thread enabled and that"
        print "will make ISPMan CCP not work correclty."
        print "You must either recompile your PyPerl without the MULTI_PERL file,"
        print "or, completely remove PyPerl from your system and allow ISPMan CCP"
        print "to install it's own."
        print
        print "A simple way to remove PyPerl from you system is:"
        print "  rm -rf /usr/lib/python2.4/site-packages/perl* && \ "
        print "  rm -rf /usr/local/lib/perl/5.8.8/auto/Python && \ "
        print "  rm -rf /usr/lib/perl/5.8.8/auto/Python"
        print "That shoud take care of PyPerl. Of course adapt to your system's"
        print "Python and Perl versions"
        print
        exit(1)
except ImportError:
    # We don't have PyPerl, so, install it
    import os, subprocess
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.join(cur_dir, 'extra-packages', 'pyperl-1.0.1d'))
    retcode = subprocess.call(['python', './setup.py', 'build'])
    retcode = subprocess.call(['python', './setup.py', 'install'])
    os.chdir(cur_dir)



# We now resume normal setup operation


VERSION = "0.1.0"

readme_file = open('README.txt')

setup(
    name = 'ISPManCCP',
    version = VERSION,
    description = "Customer Control Panel for ISPMan",
    long_description = readme_file.read(),
    license = 'BSD',
    platforms = "Anywhere you've got ISPMan working.",
    author = "Pedro Algarvio",
    author_email = "ufs@ufsoft.org",
    url = "http://ispmanccp.ufsoft.org/",
    #download_url = "http://ccp.ufsoft.org/download/%s/" % VERSION,
    zip_safe = False,
    install_requires = [
        "Pylons>=0.9.6rc3dev-r2352",
        "Genshi>=0.4",
        "formencode>=0.9",
        "Babel"
    ],
    packages = find_packages(),
    include_package_data = True,
    test_suite = 'nose.collector',
    package_data = {'ispmanccp': ['i18n/*/LC_MESSAGES/*.mo']},    
    message_extractors = {'ispmanccp': [
            ('**.py', 'python', None),
            ('**/templates/**.html', 'genshi', None),
            ('public/**', 'ignore', None)]},
    entry_points = """
    [paste.app_factory]
    main = ispmanccp.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
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
