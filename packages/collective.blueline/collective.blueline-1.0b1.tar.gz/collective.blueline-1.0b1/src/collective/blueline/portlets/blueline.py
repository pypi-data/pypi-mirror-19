# -*- coding: utf-8 -*-
from collective.blueline import _
from collective.blueline.interfaces import IBluelineSettings
from lxml import etree
from plone import api
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.formlib import form
from zope.interface import implementer
from zope.schema import ValidationError


class InvalidHTMLCode(ValidationError):

    """The code is not valid."""


def validateHTMLCode(code):
    """Validate code inserted into portlet."""
    if code:
        parser = etree.HTMLParser(recover=False)
        try:
            etree.HTML(code, parser)
        except etree.XMLSyntaxError:
            raise InvalidHTMLCode
    return True


class IBluelinePortlet(IPortletDataProvider):

    """Blueline Portlet."""

    code = schema.Text(
        title=_(u'Portlet code'),
        description=_(u'This code will be included inside the portlet.'),
        required=False,
        default=u'',
        constraint=validateHTMLCode,
    )


@implementer(IBluelinePortlet)
class Assignment(base.Assignment):

    code = u''
    title = u'Blueline'

    def __init__(self, code=u''):
        self.code = code


class Renderer(base.Renderer):

    # TODO: add template with Plone 5 markup
    render = ViewPageTemplateFile('blueline.pt')

    @property
    def available(self):
        """Check if the portlet will be shown. By default, it will be
        shown for anonymous users only; that can be changed in the
        control panel configlet.
        """
        show_authenticated = api.portal.get_registry_record(
            interface=IBluelineSettings, name='show_authenticated')
        return api.user.is_anonymous() or show_authenticated


class AddForm(base.AddForm):

    form_fields = form.Fields(IBluelinePortlet)
    label = _(u'Add Blueline Portlet')
    description = _(u'This portlet is used to insert HTML code.')

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):

    form_fields = form.Fields(IBluelinePortlet)
    label = _(u'Edit Blueline Portlet')
    description = _(u'This portlet is used to insert HTML code.')
