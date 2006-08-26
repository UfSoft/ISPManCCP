# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: environment.py 2 2006-08-26 17:51:50Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/ispmanccp/config/environment.py $
# $LastChangedDate: 2006-08-26 18:51:50 +0100 (Sat, 26 Aug 2006) $
#             $Rev: 2 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================
import os

import pylons.config

from ispmanccp.config.routing import make_map

def load_environment():
    map = make_map()
    # Setup our paths
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = {'root_path': root_path,
             'controllers': os.path.join(root_path, 'controllers'),
             'templates': [os.path.join(root_path, path) for path in \
                           ('components', 'templates')],
             'static_files': os.path.join(root_path, 'public')
             }

    # The following options are passed directly into Myghty, so all configuration options
    # available to the Myghty handler are available for your use here
    myghty = {}
    myghty['log_errors'] = True

    # Add your own Myghty config options here, note that all config options will override
    # any Pylons config options

    # Return our loaded config object
    return pylons.config.Config(myghty, map, paths)
