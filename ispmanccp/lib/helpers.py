# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: helpers.py 40 2006-11-07 22:30:49Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/ispmanccp/lib/helpers.py $
# $LastChangedDate: 2006-11-07 22:30:49 +0000 (Tue, 07 Nov 2006) $
#             $Rev: 40 $
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
from genshi.builder import tag


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

# Don't know why but this import needs to be done after the wrapper
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
    if not in_obj or in_obj == '':
        pass
    elif isinstance(in_obj, unicode) or isinstance(in_obj, int):
        return in_obj
    elif isinstance(in_obj, str):
        return unicode(in_obj, 'UTF-8')
    elif isinstance(in_obj, list):
        return [to_unicode(x) for x in in_obj if x not in ('', u'', None)]
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


def remap_user_dict(form_dict, user_dict):
    uid = user_dict['ispmanUserId']
    lengths = {}
    lengths[uid] = {}

    for key, val in form_dict.iteritems():
        if isinstance(val, list):
            # Make shure we're not passing empty mailAlias and/or
            # mailForwardingAddress's
            new_list = to_unicode(val)
            if len(new_list) > 0:
                user_dict[key] = new_list
        else:
            user_dict[key] = to_unicode(val)
    # calculate lenghts
    try:
        lengths[uid]['forwards'] = len(user_dict['mailForwardingAddress'])
    except:
        pass # there are no forwards
    try:
        lengths[uid]['aliases'] = len(user_dict['mailAlias'])
    except:
        pass # there are no aliases

    return lengths, user_dict


def random_pass(alpha, num):
    """
    Returns a human-readble password (say rol86din instead of
    a difficult to remember K8Yn9muL )
    From http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/410076
    """
    import string
    import random
    vowels = ['a','e','i','o','u']
    consonants = [a for a in string.ascii_lowercase if a not in vowels]
    digits = string.digits

    ####utility functions
    def a_part(slen):
        ret = ''
        for i in range(slen):
            if i%2 ==0:
                randid = random.randint(0,20) #number of consonants
                ret += consonants[randid]
            else:
                randid = random.randint(0,4) #number of vowels
                ret += vowels[randid]
        return ret

    def n_part(slen):
        ret = ''
        for i in range(slen):
            randid = random.randint(0,9) #number of digits
            ret += digits[randid]
        return ret

    ###
    fpl = alpha/2
    if alpha % 2 :
        fpl = int(alpha/2) + 1
    lpl = alpha - fpl

    start = a_part(fpl)
    mid = n_part(num)
    end = a_part(lpl)

    return u"%s%s%s" % (start,mid,end)



