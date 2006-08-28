<!--
 vim: sw=4 ts=4 fenc=utf-8
 $Id: mainnav.myt 4 2006-08-28 14:00:08Z s0undt3ch $
-->
<div id="menu">
%   if 'REMOTE_USER' in request.environ:
    <ul>
%      for link, url, key in c.menus['mainmenu']:
%           if toggle.strip() == link:
        <li class="active">
%               if key is not None:
            <% h.link_to(
                        link.replace(key, h.content_tag('u', key)),
                        url,
                        class_='active',
                        accesskey=key) %>
%               else:
            <% h.link_to(link, url, class_='active') %>
%               # endif

        </li>
%           else:
        <li>
%               if key is not None:
            <% h.link_to(link.replace(key, h.content_tag('u', key)), url, accesskey=key) %>
%               else:
            <% h.link_to(link, url) %>
%               # endif

        </li>

%   #       endif

%   #   endfor

%   # endif

    </ul>
</div>

<%args>
toggle
</%args>
