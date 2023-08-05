from collective.simplewiki.filter import WikiFilter
from collective.simplewiki.testing import COLLECTIVE_SIMPLEWIKI_INTEGRATION_TESTING
from plone import api
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import TEST_USER_NAME

import unittest


class TestFilter(unittest.TestCase):
    layer = COLLECTIVE_SIMPLEWIKI_INTEGRATION_TESTING

    def setUp(self):
        self.request = self.layer['request']
        self.portal = self.layer['portal']

    def test_rewrite_link(self):
        login(self.portal, TEST_USER_NAME)
        page = api.content.create(self.portal, 'Document', 'foobar', title="Foobar")
        api.content.create(self.portal, 'Document', 'foobar2', title="Foobar 2")

        filter_ = WikiFilter(page, self.request)
        self.assertEquals(
            filter_('<p> blah [[foobar2]] sdflk </p>'),
            '<p> blah <a href="http://nohost/plone/foobar2" title="Foobar 2">Foobar 2</a> sdflk </p>'
        )

    def test_rewrite_private_link(self):
        login(self.portal, TEST_USER_NAME)
        page = api.content.create(self.portal, 'Document', 'foobar', title="Foobar")
        page2 = api.content.create(self.portal, 'Document', 'foobar2', title="Foobar 2")
        api.content.transition(page2, 'hide')

        logout()
        filter_ = WikiFilter(page, self.request)
        self.assertEquals(
            filter_('<p> blah [[foobar2]] sdflk </p>'),
            '<p> blah Foobar 2[no access to link] sdflk </p>'
        )

    def test_add_link(self):
        login(self.portal, TEST_USER_NAME)
        page = api.content.create(self.portal, 'Document', 'foobar', title="Foobar")

        filter_ = WikiFilter(page, self.request)
        result = filter_('<p> blah [[foobar2|Foobar 2]] sdflk </p>')
        self.assertTrue(
            '<p> blah <a href="http://nohost/plone/++add++Document?form.widgets.IShortName.id=foobar2' in result
        )
        self.assertTrue(
            '>+ Foobar 2</a> sdflk </p>' in result
        )
