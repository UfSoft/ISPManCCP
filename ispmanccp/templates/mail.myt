<!--
 vim: sw=4 ts=4 fenc=utf-8
 $Id: mail.myt 5 2006-09-01 19:30:14Z s0undt3ch $
-->

<% c.form.layout.start(div_id="UsersListNav") %>
<% c.form.start(name='sortby', action='/mail/userlist', id='sortby') %>
<nobr>
    <% c.form.field.radio('letter', value='all', id='letter_all') %>
    <% h.content_tag('label', 'All', for_='letter_all') %>

&nbsp;
%   for d in string.digits:
    <% c.form.field.radio('letter', value=d, id='letter_%s' % d) %>
    <% h.content_tag('label', d, for_='letter_%s' % d) %>
%   #endfor

</nobr>
<nobr>
&nbsp;
%   for l in string.uppercase:
    <% c.form.field.radio('letter', value=l, id='letter_%s' % l) %>
    <% h.content_tag('label', l, for_='letter_%s' % l) %>
%   #endfor

</nobr>
<nobr>
&nbsp;
<% c.form.field.dropdown('sort_by', [
                                    ('ispmanUserId', 'User ID'),
                                    ('mailLocalAddress', 'Email Address'),
                                    ('givenName', 'First Name'),
                                    ('sn', 'Last Name'),
                                    ('ispmanCreateTimestamp', 'Date Created'),
                                    ('mailQuota', 'Email Quota')
                                    ], id='sort_by') %>
<% c.form.field.dropdown('sort_how', [
                                    ('True', 'Ascending'),
                                    ('False', 'Descending')
                                    ], id="sort_how") %>
</nobr>
<% c.form.end() %>
<% c.form.layout.end() %>

<% h.observe_form(
    'sortby',
    frequency=1,
    url=h.url(action='userlist'),
    update="UsersList",
    loading=h.update_element_function(
                "spinner",
                content = h.image_tag('/images/loading.gif')),
    loaded=h.update_element_function("spinner", content = ''),
    complete=h.visual_effect('grow', 'UsersList'),
    with="Form.serialize($('sortby'))"
    ) %>
<div id="UsersList" style="display:none"></div>
<div id="errors"></div>

<%method title>
 - <% h._('Mail') %>
</%method>
<%method nav>
<% h._('Mail') %>
</%method>

<%init>
import string
</%init>
