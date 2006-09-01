<!--
 vim: sw=4 ts=4 fenc=utf-8
 $Id: ctxnav.myt 5 2006-09-01 19:30:14Z s0undt3ch $
-->
%   if  c.controller in c.menus:
|
%       for link, url, key in c.menus[c.controller]:
%           if ctxtoggle.strip() == link:
    <% h.link_to(link.replace(key, h.content_tag('u', key)), url, class_='active', accesskey=key) %>
|
%           else:
    <% h.link_to(link.replace(key, h.content_tag('u', key)), url, accesskey=key) %>
|
%           # endif

%       #endfor

%   #endif

<%args>
ctxtoggle
</%args>
