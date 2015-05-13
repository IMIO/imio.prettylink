# -*- coding: utf-8 -*-

from zope.interface import Interface


class IPrettyLinkify(Interface):
    """ """

    def getLink(self):
        """Returns complete link to the element."""

    def _leadingIcons(self):
        """Returns icons to prepend to the link."""
