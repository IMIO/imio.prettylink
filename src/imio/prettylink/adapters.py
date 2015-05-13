# -*- coding: utf-8 -*-


class PrettyLinkAdapter(object):
    """Adapter that manage rendering the pretty link."""

    def __init__(self, context):
        self.context = context
        self.request = self.context.REQUEST

    def getLink(self):
        """See docstring in interfaces.py."""
        return "<a href='{0}'>{1}</a>".format(self._leadingIcons(), self.context.absolute_url(), self.context.Title())

    def _leadingIcons(self):
        """See docstring in interfaces.py."""
        return ''
