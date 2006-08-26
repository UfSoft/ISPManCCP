<!--
 vim: sw=4 ts=4 fenc=utf-8
 $Id$
-->
<h1><Center><% c.dominfo['cn'] + ' ' + h._('domain') %><center></h1>
<fieldset id="dominfo">
    <legend><% h._('Domain Info') %></legend>
        <p><b><% h._('Owner') %>:</b> <% c.dominfo['ispmanDomainOwner'] %>
        <p><b><% h._('Accounts') %>:</b> <% c.dominfo['ispmanAccounts'] %> of
            <% c.dominfo['ispmanMaxAccounts'] %> accounts.</p>
        <p><b><% h._('Virtual Hosts') %>:</b> <% c.dominfo['ispmanVhosts'] %> of
            <% c.dominfo['ispmanMaxVhosts'] %> virtual hosts.</p>
</fieldset>

<%method title>
 - <% h._('Home') %>
</%method>
<%method nav>
<% h._('Home') %>
</%method>
