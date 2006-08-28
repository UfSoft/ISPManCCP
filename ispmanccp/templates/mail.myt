<!--
 vim: sw=4 ts=4 fenc=utf-8
 $Id: mail.myt 4 2006-08-28 14:00:08Z s0undt3ch $
-->
<div id="UsersListChars">
%	for n in string.uppercase:
	<% h.link_to(n, '#', onclick="return fetch_mail_users('%s')" % n) %>
%	# endfor

</div>
<div id="UsersList"></div>
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
