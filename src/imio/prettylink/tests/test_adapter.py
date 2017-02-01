# -*- coding: utf-8 -*-

from imio.prettylink.interfaces import IPrettyLink
from imio.prettylink.testing import IntegrationTestCase
from plone import api
from plone.locking.interfaces import ILockable


class TestPrettyLinkAdapter(IntegrationTestCase):

    def test_getLink_caching_modified(self):
        """Cache is invalidated when modified."""
        self.assertEqual(
            IPrettyLink(self.folder).getLink(),
            u"<a class='pretty_link state-private' title='Folder' href='http://nohost/plone/folder' "
            u"target='_self'><span class='pretty_link_content'>Folder</span></a>")
        # change Title and do not notify modified
        self.folder.setTitle('Folder other title')
        self.assertTrue(" title='Folder' " in IPrettyLink(self.folder).getLink())
        # notify modified so cache is invalidated
        self.folder.notifyModified()
        self.assertTrue(" title='Folder other title' " in IPrettyLink(self.folder).getLink())

    def test_getLink_caching_context(self):
        """Cached by context so getLink on self.folder2 is correct."""
        self.assertEqual(
            IPrettyLink(self.folder).getLink(),
            u"<a class='pretty_link state-private' title='Folder' href='http://nohost/plone/folder' "
            u"target='_self'><span class='pretty_link_content'>Folder</span></a>")
        self.assertEqual(
            IPrettyLink(self.folder2).getLink(),
            u"<a class='pretty_link state-private' title='Folder2' href='http://nohost/plone/folder2' "
            u"target='_self'><span class='pretty_link_content'>Folder2</span></a>")

    def test_getLink_caching_locking(self):
        """Cache takes locking into account."""
        ILockable(self.folder).lock()
        self.assertTrue(u"lock_icon.png" in IPrettyLink(self.folder).getLink())
        ILockable(self.folder).unlock()
        self.assertFalse(u"lock_icon.png" in IPrettyLink(self.folder).getLink())

    def test_getLink_caching_review_state(self):
        """Cache takes 'locking 'review_state' into account."""
        self.assertTrue(u"<a class='pretty_link state-private' "
                        in IPrettyLink(self.folder).getLink())
        api.content.transition(self.folder, 'publish')
        self.assertTrue(u"<a class='pretty_link state-published' "
                        in IPrettyLink(self.folder).getLink())

    def test_getLink_caching_showColors(self):
        """Cache takes the 'showColors' parameter into account."""
        adapted = IPrettyLink(self.folder)
        self.assertTrue(adapted.showColors)
        self.assertTrue(u"<a class='pretty_link state-private'" in adapted.getLink())
        adapted.showColors = False
        self.assertFalse(u"<a class='pretty_link state-private'" in adapted.getLink())

    def test_getLink_caching_showIcons(self):
        """Cache takes the 'showIcons' parameter into account."""
        adapted = IPrettyLink(self.folder)
        self.assertTrue(adapted.showIcons)
        ILockable(self.folder).lock()
        self.assertTrue(u"lock_icon.png" in adapted.getLink())
        adapted.showIcons = False
        self.assertFalse(u"lock_icon.png" in adapted.getLink())

    def test_getLink_caching_showContentIcon(self):
        """Cache takes the 'showContentIcon' parameter into account."""
        adapted = IPrettyLink(self.folder)
        self.assertFalse(adapted.showContentIcon)
        self.assertFalse(u"contenttype-Folder" in adapted.getLink())
        adapted.showContentIcon = True
        self.assertTrue(u"contenttype-Folder" in adapted.getLink())

    def test_getLink_caching_showLockedIcon(self):
        """Cache takes the 'showLockedIcon' parameter into account."""
        adapted = IPrettyLink(self.folder)
        self.assertTrue(adapted.showLockedIcon)
        ILockable(self.folder).lock()
        self.assertTrue(u"lock_icon.png" in adapted.getLink())
        adapted.showLockedIcon = False
        self.assertFalse(u"lock_icon.png" in adapted.getLink())

    def test_getLink_caching_contentValue(self):
        """Cache takes the 'contentValue' parameter into account."""
        adapted = IPrettyLink(self.folder)
        self.assertFalse(adapted.contentValue)
        self.assertTrue(u"<span class='pretty_link_content'>Folder</span>" in adapted.getLink())
        adapted.contentValue = 'Content value'
        self.assertFalse(u"<span class='pretty_link_content'>Folder</span>" in adapted.getLink())
        self.assertTrue(u"<span class='pretty_link_content'>Content value</span>" in adapted.getLink())

    def test_getLink_caching_tag_title(self):
        """Cache takes the 'tag_title' parameter into account."""
        adapted = IPrettyLink(self.folder)
        self.assertFalse(adapted.tag_title)
        self.assertTrue(u" title='Folder' " in adapted.getLink())
        adapted.tag_title = 'Tag title'
        self.assertFalse(u" title='Folder' " in adapted.getLink())
        self.assertTrue(u" title='Tag title' " in adapted.getLink())

    def test_getLink_caching_maxLength(self):
        """Cache takes the 'maxLength' parameter into account."""
        adapted = IPrettyLink(self.folder)
        self.assertFalse(adapted.maxLength)
        self.assertTrue(u"<span class='pretty_link_content'>Folder</span>" in adapted.getLink())
        adapted.maxLength = 2
        self.assertFalse(u"<span class='pretty_link_content'>Folder</span>" in adapted.getLink())
        self.assertTrue(u"<span class='pretty_link_content'>Fo...</span>" in adapted.getLink())

    def test_getLink_caching_target(self):
        """Cache takes the 'target' parameter into account."""
        adapted = IPrettyLink(self.folder)
        self.assertEqual(adapted.target, '_self')
        self.assertTrue(u" target='_self'>" in adapted.getLink())
        adapted.target = '_blank'
        self.assertFalse(u" target='_self'>" in adapted.getLink())
        self.assertTrue(u" target='_blank'>" in adapted.getLink())

    def test_getLink_caching_appendToUrl(self):
        """Cache takes the 'appendToUrl' parameter into account."""
        adapted = IPrettyLink(self.folder)
        self.assertFalse(adapted.appendToUrl)
        self.assertTrue(u" href='http://nohost/plone/folder' " in adapted.getLink())
        adapted.appendToUrl = '/@@append_to_url'
        self.assertTrue(u" href='http://nohost/plone/folder/@@append_to_url' " in adapted.getLink())

    def test_getLink_caching_additionalCSSClasses(self):
        """Cache takes the 'additionalCSSClasses' parameter into account."""
        adapted = IPrettyLink(self.folder)
        self.assertFalse(adapted.additionalCSSClasses)
        self.assertTrue(u" class='pretty_link state-private' " in adapted.getLink())
        adapted.additionalCSSClasses = ['custom_css_class']
        self.assertTrue(u" class='pretty_link custom_css_class state-private' " in adapted.getLink())

    def test_getLink_caching_isViewable(self):
        """Cache takes the 'isViewable' parameter into account."""
        adapted = IPrettyLink(self.folder)
        self.assertTrue(adapted.isViewable)
        self.assertFalse(adapted.notViewableHelpMessage in adapted.getLink())
        adapted.isViewable = False
        self.assertTrue(adapted.notViewableHelpMessage in adapted.getLink())

    def test_getLink_caching_kwargs(self):
        """Cache takes the 'kwargs' parameter into account.
           By default it is used together with maxLength to define the ellipsis type."""
        adapted = IPrettyLink(self.folder)
        adapted.maxLength = 2
        self.assertFalse(adapted.kwargs)
        self.assertTrue(u"<span class='pretty_link_content'>Fo...</span>" in adapted.getLink())
        adapted.kwargs['ellipsis'] = ' [truncated]'
        self.assertFalse(u"<span class='pretty_link_content'>Fo...</span>" in adapted.getLink())
        self.assertTrue(u"<span class='pretty_link_content'>Fo [truncated]</span>" in adapted.getLink())