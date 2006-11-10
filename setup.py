#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: setup.py 50 2006-11-10 20:49:35Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/setup.py $
# $LastChangedDate: 2006-11-10 20:49:35 +0000 (Fri, 10 Nov 2006) $
#             $Rev: 50 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

from setuptools import setup, find_packages

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
    version = "0.1",
    description = "Customer Control Pannel for ISPMan",
    long_description = DESCRIPTION,
    license = 'BSD',
    platforms = "Anywhere you've got ISPMan working.",
    author = "Pedro Algarvio",
    author_email = "ufs@ufsoft.org",
    url = "http://ccp.ufsoft.org/",
    zip_safe = False,
    install_requires = [
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
