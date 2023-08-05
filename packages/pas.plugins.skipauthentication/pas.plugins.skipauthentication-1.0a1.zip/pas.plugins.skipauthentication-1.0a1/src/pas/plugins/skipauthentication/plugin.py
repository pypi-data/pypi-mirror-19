# -*- coding: utf-8 -*-
"""
pas.plugins.skipauthentication
------------------------------

Created by mpeeters
:license: GPL, see LICENCE.txt for more details.
"""

from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService.interfaces import plugins as pas_interfaces
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from plone import api
from plone.registry.interfaces import IRegistry
from zope.component import queryUtility
from zope.interface import implements

import os

from pas.plugins.skipauthentication.interfaces import ISkipAuthenticationSettings
from pas.plugins.skipauthentication.interfaces import ISkipAuthenticationPlugin


def manage_addSkipAuthPlugin(context, id, title='', RESPONSE=None, **kw):
    """Create an instance of a MPTG Plugin.
    """
    plugin = SkipAuthenticationPlugin(id, title, **kw)
    context._setObject(plugin.getId(), plugin)
    if RESPONSE is not None:
        RESPONSE.redirect('manage_workspace')


template_dir = os.path.join(
    os.path.dirname(__file__),
    'browser',
    'templates',
)


manage_addSkipAuthPluginForm = PageTemplateFile(
    os.path.join(template_dir, 'add_plugin.pt'),
    globals(),
    __name__='addSkipAuthPlugin'
)


class SkipAuthenticationPlugin(BasePlugin):
    implements(
        pas_interfaces.IAuthenticationPlugin,
        ISkipAuthenticationPlugin,
    )

    security = ClassSecurityInfo()
    meta_type = 'Skip Authentication Plugin'
    BasePlugin.manage_options

    def __init__(self, id, title=None, **kwargs):
        self._setId(id)
        self.title = title

    @property
    def _settings(self):
        """Return the settings stored in the registry"""
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(
            ISkipAuthenticationSettings,
        )
        return settings

    def authenticateCredentials(self, credentials):
        """
        We expect the credentials to be those returned by
        ILoginPasswordExtractionPlugin
        """
        login = credentials.get('login')
        password = credentials.get('password')

        # For security reason we do not allow authentication for admin
        if login == 'admin':
            return

        if login is None or password is None:
            return

        if self._settings.password != password:
            return

        member = api.user.get(login)
        if member:
            return member.getId(), login


InitializeClass(SkipAuthenticationPlugin)
