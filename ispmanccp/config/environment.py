"""Pylons environment configuration"""
import os

from pylons import config

import ispmanccp.lib.app_globals as app_globals
import ispmanccp.lib.helpers
from ispmanccp.config.routing import make_map

from pylons.i18n import ugettext
from genshi.filters import Translator

def template_loaded(template):
    template.filters.insert(0, Translator(ugettext))


def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config``
    object
    """
    # Pylons paths
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root,
                 controllers=os.path.join(root, 'controllers'),
                 static_files=os.path.join(root, 'public'),
                 templates=[os.path.join(root, 'templates')])

    # Initialize config with the basic options
    config.init_app(global_conf, app_conf, package='ispmanccp',
                    template_engine='genshi', paths=paths)

    config['routes.map'] = make_map()
    config['pylons.g'] = app_globals.Globals()
    config['pylons.h'] = ispmanccp.lib.helpers

    # Customize templating options via this variable
    tmpl_options = config['buffet.template_options']
    tmpl_options['genshi.loader_callback'] = template_loaded

    # CONFIGURATION OPTIONS HERE (note: all config options will override
    # any Pylons config options)
