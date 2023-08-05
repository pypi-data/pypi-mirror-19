# -*- coding: utf-8 -*-

from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from plone import api

from pas.plugins.skipauthentication.plugin import SkipAuthenticationPlugin


TITLE = 'Skip Authentication plugin (pas.plugins.skipauthentication)'
DEFAULTID = 'skipauthentication'


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            'pas.plugins.skipauthentication:uninstall',
        ]


def post_install(context):
    """Post install script"""
    _add_plugin(api.portal.get().acl_users)


def uninstall(context):
    """Uninstall script"""
    _remove_plugin(api.portal.get().acl_users)


def _add_plugin(acl_users, pluginid=DEFAULTID):
    if pluginid in acl_users.objectIds():
        return TITLE + ' already installed.'
    plugin = SkipAuthenticationPlugin(pluginid, title=TITLE)
    acl_users._setObject(pluginid, plugin)
    plugin = acl_users[plugin.getId()]  # get plugin acquisition wrapped!
    for info in acl_users.plugins.listPluginTypeInfo():
        interface = info['interface']
        if not interface.providedBy(plugin):
            continue
        acl_users.plugins.activatePlugin(interface, plugin.getId())
        acl_users.plugins.movePluginsDown(
            interface,
            [x[0] for x in acl_users.plugins.listPlugins(interface)[:-1]],
        )


def _remove_plugin(acl_users, pluginid=DEFAULTID):
    if pluginid in acl_users.objectIds():
        acl_users.manage_delObjects([pluginid])
