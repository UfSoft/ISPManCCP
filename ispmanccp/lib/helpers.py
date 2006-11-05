# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: helpers.py 34 2006-11-05 18:57:20Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/ispmanccp/lib/helpers.py $
# $LastChangedDate: 2006-11-05 18:57:20 +0000 (Sun, 05 Nov 2006) $
#             $Rev: 34 $
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
from pylons.util import _, log, set_lang, get_lang

def wrap_helpers(localdict):
    from genshi import Markup
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

# These imports are made here so they don't get wrapped, there's no need to.
from genshi.builder import tag
from datetime import date

def date_from_tstamp(tstamp):
    return date.fromtimestamp(int(tstamp))


def convert_size(size):
    """ Helper function  to convert ISPMan sizes to readable units. """
    return h.number_to_human_size(int(size)*1024)


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

def to_unicode(in_obj):
    """ Function to convert whatever we can to unicode."""
    if not in_obj:
        pass
    elif isinstance(in_obj, unicode) or isinstance(in_obj, int):
        return in_obj
    elif isinstance(in_obj, str):
        return unicode(in_obj, 'UTF-8')
    elif isinstance(in_obj, list):
        return [to_unicode(x) for x in in_obj if x != '' or None]
    elif isinstance(in_obj, dict):
        out_dict = {}
        for key, val in in_obj.iteritems():
            out_dict[key] = to_unicode(val)
        return out_dict
    else:
        try:
#            print 'try dict'
            return to_unicode(dict(in_obj))
        except: # Exception, e:
            pass
#            print 'try dict', e
        try:
#            print 'try list'
            return to_unicode(list(in_obj))
        except: # Exception, e:
            pass
#                 print 'try list', e
    return in_obj
