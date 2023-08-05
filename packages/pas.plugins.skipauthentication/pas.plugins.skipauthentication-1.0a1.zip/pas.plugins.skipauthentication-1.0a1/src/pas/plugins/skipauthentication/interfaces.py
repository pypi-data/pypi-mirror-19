# -*- coding: utf-8 -*-
"""
pas.plugins.skipauthentication
------------------------------

Created by mpeeters
:license: GPL, see LICENCE.txt for more details.
"""

from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from pas.plugins.skipauthentication import _


class IPasPluginsSkipauthenticationLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ISkipAuthenticationPlugin(Interface):
    """Skip Authentication Plugin"""


class ISkipAuthenticationSettings(Interface):
    """Skip Authentication Plugin settings"""

    password = schema.TextLine(
        title=_(u'Master password'),
        description=_(
            u'Password used for the authentication'
        ),
        required=True,
    )
