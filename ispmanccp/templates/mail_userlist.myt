<!--
 vim: sw=4 ts=4 fenc=utf-8
 $Id: mail_userlist.myt 4 2006-08-28 14:00:08Z s0undt3ch $
-->
<div id="UsersList">
%	if c.users:
%		for user in c.users.keys():
	<fieldset id="short_user_details">
	<legend><% c.users[user]['mailLocalAddress'] %></legend>
%			for k, v in c.users[user].items():
%				if k == 'mailAlias':
%					for vv in v:
		<b><% k %>:</b> <% vv %><BR />
%				# endfor
%				elif k == "ispmanCreateTimestamp":
		<b><% k %>:</b><% h.date_from_tstamp(v) %><BR />
%				elif k == "mailQuota":
		<b><% k %>:</b><% int(v)/1024 %> Mb<BR />
%				else:
		<b><% k %>:</b><% v %><BR />
%				# endif				
%			# endfor
    </fieldset>
%		# endfor
%	else:
	<div id="errors">
		<h2><% c.error %></h2>
	</div>
%	# endif
</div>
