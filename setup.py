#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: setup.py 6 2006-10-20 10:41:43Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/setup.py $
# $LastChangedDate: 2006-10-20 11:41:43 +0100 (Fri, 20 Oct 2006) $
#             $Rev: 6 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

from setuptools import setup, find_packages

setup(
    name='ISPManCCP',
    version="0.1",
    description="Customer Control Pannel for ISPMan",
    author="Pedro Algarvio",
    author_email="ufs@ufsoft.org",
    url="http://ispmanccp.ufsoft.org/",
    install_requires=["Pylons", "python-ldap>=2.0.11", "Genshi"],
    packages=find_packages(),
    include_package_data=True,
    test_suite = 'nose.collector',
    package_data={'ispmanccp': ['i18n/*/LC_MESSAGES/*.mo']},
    entry_points="""
    [paste.app_factory]
    main=ispmanccp:make_app
    [paste.app_install]
    main=paste.script.appinstall:Installer
    """,
)
