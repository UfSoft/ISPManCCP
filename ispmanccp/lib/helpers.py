# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: helpers.py 10 2006-10-21 15:21:01Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/ispmanccp/lib/helpers.py $
# $LastChangedDate: 2006-10-21 16:21:01 +0100 (Sat, 21 Oct 2006) $
#             $Rev: 10 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

"""
Helper functions

All names available in this module will be available under the Pylons h object.
"""
from webhelpers import *
from pylons import h
from datetime import date
from genshi.builder import tag
from genshi.core import Markup

def wrap_helpers(localdict):
    def helper_wrapper(func):
        def wrapped_helper(*args, **kw):
            return Markup(func(*args, **kw))
        wrapped_helper.__name__ = func.__name__
        return wrapped_helper
    for name, func in localdict.iteritems():
        if not callable(func) or not func.__module__.startswith('webhelpers.rails'):
            continue
        localdict[name] = helper_wrapper(func)
wrap_helpers(locals())



def date_from_tstamp(tstamp):
    return date.fromtimestamp(int(tstamp))

def convert_size(size):
    """ Helper function  to convert ISPMan sizes to readable units. """
    size = int(size)
    if size < 1024:
        return '%d KB' % size
    elif size < 1048576:
        return '%d MB' % (size / 1024)
    else:
        return '%.2f GB' % (size / 1048576.0)

def get_nav_class_state(url, request, partial=False):
    """ Helper function that just returns the 'active'/'inactive'
    link class based on the passed url. """
    if partial:
        _url = '/' + '/'.join(
            [request.environ['pylons.routes_dict']['controller']])
    else:
        _url = '/' + '/'.join([
            request.environ['pylons.routes_dict']['controller'],
            request.environ['pylons.routes_dict']['action']])

    if url == request.path_info:
        return 'active'
    elif url.startswith(_url) and partial:
        return 'active'
    elif url == _url:
        return 'active'
    else:
        return 'inactive'
