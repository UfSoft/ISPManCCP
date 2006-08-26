<!--
 vim: sw=4 ts=4 fenc=utf-8
 $Id$
-->
<div id="menu">
%   if 'REMOTE_USER' in request.environ:
    <ul>
%      for link, url, key in c.menu:
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

<%init>
    def create_i18n_menu():
        keys_list = {}
        menu = []
        for name, url in c.menu:
            for n in range(len(name)):
                if name[n].upper() not in [x.upper() for x in keys_list.values()]:
                    keys_list[url] = name[n]
                    break
                else:
                    n += 1
            else:
                keys_list[url] = None
            menu.append((name, url, keys_list[url]))
        return menu

    cache = m.get_cache()
    if not cache.has_key('i18n_menu'):
        cache.set_value('i18n_menu', create_i18n_menu(), expiretime=60)
    c.menu = cache.get_value('i18n_menu', type='memory',
                            createfunc=create_i18n_menu, expiretime=60)
</%init>

<%args>
toggle
</%args>
