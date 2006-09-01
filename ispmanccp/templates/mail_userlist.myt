<!--
 vim: sw=4 ts=4 fenc=utf-8
 $Id: mail_userlist.myt 5 2006-09-01 19:30:14Z s0undt3ch $
-->
%   if c.users:
%       for user in c.users:
    <fieldset id="short_user_details">
    <legend><% user['mailLocalAddress'] %></legend>
        <b>User ID:</b> <% user['ispmanUserId'] %><BR />
        <b>First Name:</b> <% user['givenName'] %><BR />
        <b>Last Name:</b> <% user['sn'] %><BR />
        <b>Created on:</b> <% h.date_from_tstamp(user['ispmanCreateTimestamp']) %><BR />
        <b>Email Quota:</b> <% int(user['mailQuota'])/1024 %><BR />
        <b>Email Address:</b> <% user['mailLocalAddress'] %><BR />
%           if 'mailAlias' in user:
        <b>Email Alias:</b><BR />
%               for alias in user['mailAlias']:
        &nbsp;&nbsp;&nbsp;&nbsp;<% alias %><BR />
%               # endfor

%           # endif

    </fieldset>
%       # endfor

%   else:
    <div id="errors">
        <h2><% c.error %></h2>
    </div>
%   # endif
