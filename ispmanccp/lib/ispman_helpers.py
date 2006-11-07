# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: ispman_helpers.py 40 2006-11-07 22:30:49Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/ispmanccp/lib/ispman_helpers.py $
# $LastChangedDate: 2006-11-07 22:30:49 +0000 (Tue, 07 Nov 2006) $
#             $Rev: 40 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

from string import join
from formencode.variabledecode import variable_decode
from pylons import request, g, cache
from ispmanccp.lib.helpers import to_unicode

APP_CONF = request.environ['paste.config']['app_conf']

ispman_cache = cache.get_cache('ispman')

allowed_user_attributes = (
    'dn', 'dialupAccess', 'radiusProfileDn', 'uid', 'uidNumber', 'gidNumber',
    'homeDirectory', 'loginShell', 'ispmanStatus', 'ispmanCreateTimestamp',
    'ispmanUserId', 'ispmanDomain', 'DestinationAddress', 'DestinationPort',
    'mailQuota', 'mailHost', 'fileHost', 'cn', 'mailRoutingAddress',
    'FTPStatus', 'FTPQuotaMBytes', 'mailAlias', 'sn', 'mailLocalAddress',
    'userPassword', 'mailForwardingAddress', 'givenName')

updatable_attributes = (
    'ispmanStatus', 'mailQuota', 'mailAlias', 'sn', 'userPassword',
    'givenName', 'updateUser', 'uid', 'ispmanDomain', 'mailForwardingAddress',
    'FTPQuotaMBytes', 'FTPStatus'
)


def conv_to_list(obj):
    """Helper to covert perl ARRAY's which sometimes
    are just strings, to lists."""
    if isinstance(obj, str) or isinstance(obj, unicode):
        return 1, [to_unicode(obj)]
    else:
        listing = to_unicode(obj)
        return len(listing), listing


def get_users_list(domain, letter, sortby=None, sort_ascending=True):
    domain_users = to_unicode(g.ispman.getUsers(
        domain, [
            "dn",
            "givenName",
            "sn",
            "cn",
            "ispmanCreateTimestamp",
            "ispmanUserId",
            "mailLocalAddress",
            "mailForwardingAddress",
            "userPassword",
            "mailQuota",
            "mailAlias",
            "FTPQuotaMBytes",
            "FTPStatus"
        ]
    ))

    userlist = []
    lengths = {}
    for user, vals in domain_users.items():
        # add the dn since the user data does not carry that info
        vals = to_unicode(dict(vals))
        vals['dn'] = user
        user_id = vals['ispmanUserId']
        lengths[user_id] = {}

        # Aparently Genshi converts what it can to strings,
        # we have to make these lists
        if 'mailAlias' in vals:
            lengths[user_id]['aliases'], vals['mailAlias'] = \
                    conv_to_list(vals['mailAlias'])

        if 'mailForwardingAddress' in vals:
            lengths[user_id]['forwards'], vals['mailForwardingAddress'] = \
                    conv_to_list(vals['mailForwardingAddress'])

        if letter == 'All' or user_id.upper().startswith(letter):
            userlist.append(vals)

    # let's save some time and return right away if we don't need any sorting
    if len(userlist) <= 1:
        return lengths, userlist

    decorated = [(dict_[sortby], dict_) for dict_ in userlist]
    decorated.sort()

    if not sort_ascending:
        decorated.reverse()
    result = [dict_ for (key, dict_) in decorated]
    return lengths, result


def get_user_info(uid, domain):
    user_info = to_unicode(g.ispman.getUserInfo(uid + '@' + domain, domain))
    lengths = {}
    lengths[uid] = {}
    if 'mailAlias' in user_info:
        lengths[uid]['aliases'], user_info['mailAlias'] = \
                conv_to_list(user_info['mailAlias'])
    if 'mailForwardingAddress' in user_info:
        lengths[uid]['forwards'], user_info['mailForwardingAddress'] = \
                conv_to_list(user_info['mailForwardingAddress'])
    user_info['mailQuota'] = int(user_info['mailQuota'])/1024
    return lengths, user_info


def get_perl_cgi(params_dict):
    attrib_tpl = """ '%(key)s' => ['%(val)s'], """
    params_dict = variable_decode(params_dict)
    cgi_params = "$q = new CGI({"
    for key, val in params_dict.iteritems():
        if key in updatable_attributes:
            if isinstance(val, list):
                cgi_params += attrib_tpl % ( {'key': key, 'val': join(val)} )
            else:
                cgi_params += attrib_tpl % ( {'key': key, 'val': val} )
    cgi_params += """}) or die "$@";"""
    cgi = g.perl.eval(cgi_params)
    g.perl.eval('$q->header(-charset => "UTF-8");')
    return cgi


def update_user_info(attrib_dict):
    cgi = get_perl_cgi(attrib_dict)
    return g.ispman.update_user(cgi)


def get_user_attribute_values(id, domain, attribute):
    return to_unicode(
        g.ispman.getUserAttributeValues(id, domain, attribute)
    )


def delete_user(post_dict):
    cgi = get_perl_cgi(post_dict)
    return g.ispman.deleteUser(cgi)


def user_exists(user_id):
    uid = user_id + '@' + request.POST['ispmanDomain']
    return bool(int(g.ispman.userExists(uid)))


def get_domain_info(domain):
    def get():
        return to_unicode(dict(
            g.ispman.getDomainInfo(domain, 2))
        )

    cached = ispman_cache.get_value(        # cache it for 5 minutes
        'domain_info', createfunc=get, type="memory", expiretime=300)
    return cached


def get_domain_vhost_count(domain):
    return to_unicode(g.ispman.getVhostCount(domain))


def get_domain_user_count(domain):
    return to_unicode(g.ispman.getUserCount(domain))


def get_default_acount_vars():
    def get():
        defaults = {}
        defaults['defaultUserFtpQuota'] = to_unicode(
            g.ispman.getConf('defaultUserFtpQuota')
        )
        defaults['defaultUserMailQuota'] = to_unicode(
            g.ispman.getConf('defaultUserMailQuota')
        )
        return defaults
    cached = ispman_cache.get_value(               # cache it for one hour
        'account_defaults', createfunc=get, type="memory", expiretime=3600)
    return cached


def address_exists(address):
    base = APP_CONF['ispman_ldap_base_dn']
    scope = 'sub'
    ldap_filter = "&(mailAlias=%(address)s)(mailLocalAddress=%(address)s)"
    ldap_filter = ldap_filter % {'address': address}
    return bool(int(g.ispman.getCount(base, ldap_filter)))


def add_user(attrib_dict):
    cgi = get_perl_cgi(attrib_dict)
    return g.ispman.addUser(cgi)

