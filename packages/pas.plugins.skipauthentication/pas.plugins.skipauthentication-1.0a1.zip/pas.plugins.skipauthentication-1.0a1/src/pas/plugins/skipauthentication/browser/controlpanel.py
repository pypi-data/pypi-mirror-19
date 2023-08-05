# -*- coding: utf-8 -*-
"""
pas.plugins.skipauthentication
------------------------------

Created by mpeeters
:license: GPL, see LICENCE.txt for more details.
"""

from plone.app.registry.browser import controlpanel

from pas.plugins.skipauthentication import _
from pas.plugins.skipauthentication.interfaces import ISkipAuthenticationSettings


class SkipAuthenticattionSettingsEditForm(controlpanel.RegistryEditForm):
    schema = ISkipAuthenticationSettings
    label = _(u'Skip Authentication Settings')


class SkipAuthenticationSettingsView(controlpanel.ControlPanelFormWrapper):
    form = SkipAuthenticattionSettingsEditForm
