# -*- coding: utf-8 -*-

from collective.blueline import _
from lxml import etree
from plone.autoform import directives as form
from plone.supermodel import model
from zope import schema
from zope.interface import Interface
from zope.interface import Invalid


class IBrowserLayer(Interface):

    """A layer specific for this add-on product."""


def validCodeConstraint(value):
    """Validate code inserted into control panel configlet fields.

    :param value: code to be validated
    :type value: unicode
    :return: True if code is valid
    :rtype: bool
    :raises:
        :class:`~zope.interface.Invalid` if the code is not valid
    """
    if value:
        parser = etree.HTMLParser(recover=False)
        try:
            etree.HTML(value, parser)
        except Exception as e:
            raise Invalid(_(u'Invalid code: ') + e.message)
    return True


class IBluelineSettings(model.Schema):

    """Schema for the control panel form."""

    show_authenticated = schema.Bool(
        title=_(u'Show to authenticated users?'),
        description=_(
            u'By default, viewlets will be visible for anonymous users only. '
            u'If selected, the code will be shown to authenticated users also.'
        ),
        default=False,
    )

    form.widget('html_head', cols=80, rows=10)
    html_head = schema.Text(
        title=_(u'HTML Head'),
        description=_(u'This code will be included inside the head tag.'),
        default=u'',
        required=False,
        constraint=validCodeConstraint
    )

    form.widget('header', cols=80, rows=10)
    header = schema.Text(
        title=_(u'Header'),
        description=_(u'This code will be included at the top of the page.'),
        default=u'',
        required=False,
        constraint=validCodeConstraint
    )

    form.widget('above_content', cols=80, rows=10)
    above_content = schema.Text(
        title=_(u'Above Content'),
        description=_(u'This code will be included above the content of the page.'),
        default=u'',
        required=False,
        constraint=validCodeConstraint
    )

    form.widget('below_content_body', cols=80, rows=10)
    below_content_body = schema.Text(
        title=_(u'Below Content Body'),
        description=_(u'This code will be included below the body of the content of the page.'),
        default=u'',
        required=False,
        constraint=validCodeConstraint
    )

    form.widget('below_content', cols=80, rows=10)
    below_content = schema.Text(
        title=_(u'Below Content'),
        description=_(u'This code will be included below the content of the page.'),
        default=u'',
        required=False,
        constraint=validCodeConstraint
    )

    form.widget('footer', cols=80, rows=10)
    footer = schema.Text(
        title=_(u'Footer'),
        description=_(u'This code will be included at the end of the page.'),
        default=u'',
        required=False,
        constraint=validCodeConstraint
    )
