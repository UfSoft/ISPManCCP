# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: accounts.py 40 2006-11-07 22:30:49Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/ispmanccp/controllers/accounts.py $
# $LastChangedDate: 2006-11-07 22:30:49 +0000 (Tue, 07 Nov 2006) $
#             $Rev: 40 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

from string import uppercase, digits
from ispmanccp.lib.base import *
from ispmanccp.models.accounts import *


class AccountsController(BaseController):

    def index(self):
        """Main Index."""
        c.nav_1st_half = ['All']
        c.nav_1st_half.extend(list(digits))
        c.nav_2nd_half = list(uppercase)
        c.domain = self.domain
        return render_response('accounts.index')


    def userlist(self):
        """Action that returns the user list for the passed start key."""
        sort_by = request.POST['sort_by']
        sort_how = bool(int(request.POST['sort_how']))

        if 'None' in request.POST['letter']:
            c.users = []
            return render_response('accounts.snippets.userlist')

        if 'letter' in request.POST:
            start_letter = request.POST['letter']
        else:
            start_letter = 'All'

        c.lengths, userlist = get_users_list(self.domain,
                                             start_letter,
                                             sortby=sort_by,
                                             sort_ascending=sort_how)

        if not userlist:
            c.error = _("No results retrieved.")
        else:
            c.users = userlist
        return render_response('accounts.snippets.userlist')


    def search(self):
        """Action that returns an html list of entries for the
        auto-complete search field."""
        sort_by = request.POST['sort_by']
        sort_how = bool(int(request.POST['sort_how']))
        c.lengths, userlist = get_users_list(self.domain,
                                             'All',
                                             sortby=sort_by,
                                             sort_ascending=sort_how)

        html = u'<ul>\n'
        for user in userlist:
            html += u'<li>\n'
            html += u'<div class="uid">%(ispmanUserId)s</div>\n'
            html += u'<span class="informal">%(cn)s</span>\n'
            html += u'<div class="email">'
            html += u'<span class="informal">%(mailLocalAddress)s</span>'
            html += u'</div>\n</li>\n'
            html = html % user
        html += u'</ul>\n'
        return Response(html)


    def get_stored_pass(self, id):
        """Action that restores the stored password of the user."""
        uid = id + '@' + self.domain
        c.userinfo = {}
        c.userinfo['userPassword'] = get_user_attribute_values(uid, self.domain, 'userPassword')
        return render_response('accounts.snippets.password')



    @rest.dispatch_on(POST='delete_post')
    def delete(self, id):
        """Action to delete the account."""
        c.lengths, c.userinfo = get_user_info(id, self.domain)
        return render_response('accounts.deleteuser')


    @validate(template='accounts.deleteuser', schema=AccountDelete(), form='delete')
    def delete_post(self, id):
        """The real work for the above action."""
        retval = delete_user(request.POST)
        if retval != "1" or retval != 1:
            session['message'] = _('Backend Error')
            session.save()
            self.message = 'Backend Error'
            h.redirect_to(action="delete", id=id)
        session['message'] = _('Operation Successfull')
        session.save()
        redirect_to(action="index", id=None)



    @rest.dispatch_on(POST='edit_post')
    def edit(self, id):
        """Action to edit the account details."""
        c.lengths, c.userinfo = get_user_info(id, self.domain)
        if c.form_result:
            # Form has been submited
            # Assign the form_result to c.userinfo
            c.lengths, c.userinfo = h.remap_user_dict(c.form_result, c.userinfo)
        return render_response('accounts.edituser')


    @validate(template='accounts.edituser', schema=AccountUpdate(), form='edit', variable_decode=True)
    def edit_post(self, id):
        """The real work for the above action, where modifications
        are made permanent."""
        if request.method != 'POST':
            redirect_to(action='edit', id=id)
        user_dict = request.POST.copy()
        user_dict['uid'] = user_dict['uid'] + '@' + self.domain
        uid = user_dict['uid']
        retval = update_user_info(user_dict)
        if retval != 1:
            session['message'] = _('Backend Error')
            session.save()
            self.message = 'Backend Error'
            h.redirect_to(action="edit", id=id)
        session['message'] = _('Operation Successfull')
        session.save()
        redirect_to(action="index", id=None)


    @rest.dispatch_on(POST='new_post')
    def new(self, id):
        """Action to create a new account."""
        # Can the domain have more accounts
        max_accounts = int(get_domain_user_count(self.domain))
        cur_accounts = int(self.dominfo['ispmanMaxAccounts'])
        if max_accounts != -1 and cur_accounts + 1 > max_accounts:
            session['message'] = _(
                'You cannot create more accounts. Allowed maximum reached.'
            )
            session.save()
            redirect_to(action="index", id=None)

        # It can, let's continue
        c.defaults = get_default_acount_vars()
        c.dominfo = self.dominfo
        c.password = self._generate_new_password()
        print self.dominfo
        if 'ispmanUserId' not in request.POST:
            c.userinfo = {'ispmanUserId': u'please change me'}

        if c.form_result:
            c.lengths, c.userinfo = h.remap_user_dict(c.form_result, request.POST.copy())
        return render_response('accounts.newuser')


    @validate(template='accounts.newuser', schema=AccountCreate(), form='new', variable_decode=True)
    def new_post(self, id):
        """The real work for the above action, where modifications
        are made permanent."""
        if request.method != 'POST':
            redirect_to(action='new', id=None)
        # DO SOMETHING
        APP_CONF = request.environ['paste.config']['app_conf']

        userinfo = request.POST.copy()
        # add some account defaults
        userinfo['dialupAccess'] = u'disabled'
        userinfo['radiusProfileDN'] = 'cn=default, ou=ou=radiusprofiles, ' + \
                APP_CONF['ispman_ldap_base_dn']
        userinfo['mailHost'] = self.dominfo['ispmanDomainDefaultMailDropHost']
        userinfo['fileHost'] = self.dominfo['ispmanDomainDefaultFileServer']

        retval = add_user(userinfo)
        if retval != 1:
            session['message'] = _('Backend Error')
            session.save()
            self.message = 'Backend Error'
            h.redirect_to(action="new", id=None)
        session['message'] = _('Operation Successfull')
        session.save()
        redirect_to(action="index", id=None)


    def _generate_new_password(self):
        """Private method that returns a new random password(value)."""
        APP_CONF = request.environ['paste.config']['app_conf']
        numbers = int(APP_CONF['passwords_non_letter_min_chars'])
        alpha = int(APP_CONF['passwords_min_length']) - numbers
        return h.random_pass(alpha, numbers)


    def generate_new_password(self):
        """Action that returns a new random password(rendered html)."""
        c.password = self._generate_new_password()
        return render_response('accounts.snippets.newpassword')

