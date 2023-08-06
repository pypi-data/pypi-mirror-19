# -*- coding: utf-8 -*-
from collective.blueline.portlets import blueline as bluelineprofile
from collective.blueline.testing import INTEGRATION_TESTING
from plone.app.portlets.storage import PortletAssignmentMapping
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletRenderer
from plone.portlets.interfaces import IPortletType
from zope.component import getMultiAdapter
from zope.component import getUtility

import unittest


HTML = u"""<script>
  var html = document.createElement("div");
  html.innerHTML = "TEST";
  document.body.appendChild(divtest);
</script>"""


class PortletTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_portlet_type_registered(self):
        name = 'collective.blueline'
        portlet = getUtility(IPortletType, name=name)
        self.assertEqual(portlet.addview, name)

    def test_interfaces(self):
        portlet = bluelineprofile.Assignment(code=HTML)

        self.assertTrue(IPortletAssignment.providedBy(portlet))
        self.assertTrue(IPortletDataProvider.providedBy(portlet.data))

    def test_invoke_add_view(self):
        name = 'collective.blueline'
        portlet = getUtility(IPortletType, name=name)
        mapping = self.portal.restrictedTraverse('++contextportlets++plone.leftcolumn')

        for m in mapping.keys():
            del mapping[m]

        addview = mapping.restrictedTraverse('+/' + portlet.addview)

        addview.createAndAdd(data=dict(code=HTML))

        self.assertEqual(len(mapping), 1)
        self.assertIsInstance(mapping.values()[0], bluelineprofile.Assignment)

    def test_invoke_edit_view(self):
        mapping = PortletAssignmentMapping()
        request = self.request

        mapping['foo'] = bluelineprofile.Assignment(code=HTML)

        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.assertIsInstance(editview, bluelineprofile.EditForm)

    def test_obtain_renderer(self):
        context = self.portal
        request = self.request
        view = context.restrictedTraverse('@@plone')
        manager = getUtility(
            IPortletManager, name='plone.rightcolumn', context=self.portal)

        assignment = bluelineprofile.Assignment(code=HTML)

        renderer = getMultiAdapter(
            (context, request, view, manager, assignment), IPortletRenderer)

        self.assertIsInstance(renderer, bluelineprofile.Renderer)


class RenderTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.portlet = self._get_portlet_renderer()
        self.portlet.update()

    def _get_portlet_renderer(self):
        context, request = self.portal, self.request
        view = self.portal.restrictedTraverse('@@plone')
        manager = getUtility(
            IPortletManager, name='plone.rightcolumn', context=self.portal)
        assignment = bluelineprofile.Assignment(code=HTML)
        renderer = getMultiAdapter(
            (context, request, view, manager, assignment), IPortletRenderer)
        return renderer.__of__(self.portal)

    def test_render_authenticated(self):
        output = self.portlet.render()
        self.assertNotIn('html.innerHTML = "TEST";', output)

        from collective.blueline.controlpanel import IBluelineSettings
        from plone.registry.interfaces import IRegistry
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IBluelineSettings)
        settings.show_authenticated = True
        output = self.portlet.render()
        self.assertIn('html.innerHTML = "TEST";', output)

    def test_render_anonymous(self):
        from plone.app.testing import logout
        logout()
        output = self.portlet.render()
        self.assertIn('html.innerHTML = "TEST";', output)
