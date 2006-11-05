# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: accounts.py 34 2006-11-05 18:57:20Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/trunk/ispmanccp/controllers/accounts.py $
# $LastChangedDate: 2006-11-05 18:57:20 +0000 (Sun, 05 Nov 2006) $
#             $Rev: 34 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

from string import uppercase, digits
from ispmanccp.lib.base import *
from ispmanccp.models.accounts import AccountUpdate

class AccountsController(BaseController):

    def index(self):
        c.nav_1st_half = ['All']
        c.nav_1st_half.extend(list(digits))
        c.nav_2nd_half = list(uppercase)
        c.domain = self.domain
        return render_response('accounts.index')


    def userlist(self):
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


    def get_stored_pass(self, id):
        uid = id + '@' + self.domain
        c.userinfo = {}
        c.userinfo['userPassword'] = get_user_attribute_values(uid, self.domain, 'userPassword')
        return render_response('accounts.snippets.password')


    @rest.dispatch_on(POST='edit_post')
    def edit(self, id, message=None):
        c.lengths, c.userinfo = get_user_info(id, self.domain)
        if c.form_result:
            # Form has been submited
            # Assign the form_result to c.userinfo
            for key, val in c.form_result.iteritems():
                if isinstance(val, list):
                    # Make shure we're not passing empty mailAlias and
                    # mailForwardingAddress's
                    new_list = h.to_unicode(val)
                    if len(new_list) > 0:
                        c.userinfo[key] = new_list
                else:
                    c.userinfo[key] = h.to_unicode(val)
            # re-calculate lenghts
            try:
                c.lengths[uid]['forwards'] = len(c.form_result['mailForwardingAddress'])
            except:
                pass # there are no forwards
            try:
                c.lengths[uid]['aliases'] = len(c.form_result['mailAlias'])
            except:
                pass # there are no aliases
        return render_response('accounts.edituser')


    @validate(template='accounts.edituser', schema=AccountUpdate(), form='edit', variable_decode=True)
    def edit_post(self, id):
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
        c.domain = self.domain
        return render_response('accounts.newuser')

    def new_post(self, id):
        pass
