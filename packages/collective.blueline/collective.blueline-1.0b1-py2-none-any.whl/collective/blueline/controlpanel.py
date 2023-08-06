# -*- coding: utf-8 -*-
from collective.blueline import _
from collective.blueline.interfaces import IBluelineSettings
from plone.app.registry.browser import controlpanel


class BluelineSettingsEditForm(controlpanel.RegistryEditForm):

    """Control panel edit form."""

    schema = IBluelineSettings
    label = _(u'Blueline')
    description = _(u'Settings for the collective.blueline package')


class BluelineSettingsControlPanel(controlpanel.ControlPanelFormWrapper):

    """Control panel form wrapper."""

    form = BluelineSettingsEditForm
