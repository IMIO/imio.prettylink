# -*- coding: utf-8 -*-

from zope.interface import Interface


class IPrettyLink(Interface):
    """ """

    def getLink(self):
        """Returns complete link to the element."""

    def _leadingIcons(self):
        """Returns icons to prepend to the link."""
