<!--
 vim: sw=4 ts=4 fenc=utf-8
 $Id$
-->
%   if c.ctxnav:
    <ul id="ctxnav">
%       if toggle.strip() == link:
%           for link, url, key in c.ctxnav:
        <li class="active"><% h.link_to(link, url, class_='active', accesskey=key) %></li>
%       else:
            <li><% h.link_to(link, url, accesskey=key) %></li>
%           # endfor

    </ul>
%       #endif

%   #endif

<%args>
ctxtoggle
</%args>
