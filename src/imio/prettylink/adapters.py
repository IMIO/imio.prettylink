# -*- coding: utf-8 -*-
from zope.i18n import translate
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode


class PrettyLinkAdapter(object):
    """Adapter that manage rendering the pretty link."""

    def __init__(self,
                 context,
                 showColors=True,
                 showIcons=True,
                 showContentIcon=False,
                 showLockedIcon=True,
                 contentValue='',
                 tag_title='',
                 maxLength=0,
                 target='_self',
                 appendToUrl='',
                 additionalCSSClasses=[],
                 isViewable=True,
                 **kwargs):
        self.context = context
        self.request = self.context.REQUEST
        self.portal_url = getToolByName(self.context, 'portal_url').getPortalObject().absolute_url()
        # we set parameters in the init so it it reusable across every methods
        self.showColors = showColors
        self.showIcons = showIcons
        self.showContentIcon = showContentIcon
        self.showLockedIcon = showLockedIcon
        # value to use for the link, if not given, object's title will be used
        self.contentValue = contentValue
        # arbitrary tag_title
        self.tag_title = tag_title
        # truncate link content to given maxLength if any
        self.maxLength = maxLength
        # target of the link : _blank, _self, ...
        self.target = target
        # append arbitrary to the rendered URL
        self.appendToUrl = appendToUrl
        # arbitrary css classes
        self.additionalCSSClasses = additionalCSSClasses
        self.kwargs = kwargs
        # we also manage the fact that we want to display an element that is
        # actually not reachable by current user...  In this case, we display
        # a <div> to the element with a help message...
        self.isViewable = isViewable
        self.notViewableHelpMessage = translate(
            'can_not_access_this_element',
            domain="imio.prettylink",
            context=self.request,
            default="<span class='discreet'>(You can not access this element)</span>").encode('utf-8')

    def getLink(self):
        """See docstring in interfaces.py."""
        content = self.contentValue or unicode(self.context.Title(), 'utf-8')
        if self.maxLength:
            plone_view = self.context.restrictedTraverse('@@plone')
            ellipsis = self.kwargs.get('ellipsis', '...')
            content = plone_view.cropText(content, self.maxLength, ellipsis)
        icons = self.showIcons and self._icons() or ''
        if self.isViewable:
            url = self.context.absolute_url() + self.appendToUrl
            return u"{0} <a class='{1}' title='{2}' href='{3}' target='{4}'>{5}</a>" \
                   .format(icons,
                           self.CSSClasses(),
                           self.tag_title,
                           url,
                           self.target,
                           content)
        else:
            # display the notViewableHelpMessage if any
            content = self.notViewableHelpMessage and \
                ("{0} {1}".format(content, self.notViewableHelpMessage)) or \
                content
            return u"{0} <div class='{1}' title='{2}'>{3}</div>" \
                   .format(icons,
                           self.CSSClasses(),
                           self.tag_title,
                           content,
                           self.notViewableHelpMessage)

    def CSSClasses(self):
        """See docstring in interfaces.py."""
        css_classes = list(self.additionalCSSClasses)
        if self.showColors:
            wft = getToolByName(self.context, 'portal_workflow')
            css_classes.append('state-{0}'.format(wft.getInfoFor(self.context, 'review_state')))
        # in case the contentIcon must be shown and it the icon
        # is shown by the generated contentttype-xxx class
        if self.showContentIcon:
            typeInfo = getToolByName(self.context, 'portal_types')[self.context.portal_type]
            if not typeInfo.iconExpr:
                css_classes.append('contenttype-{0}'.format(typeInfo.getId()))
        return ' '.join(css_classes)

    def _icons(self, **kwargs):
        """See docstring in interfaces.py."""
        icons = []

        # manage icons we want to be displayed before managed icons
        icons = icons + self._leadingIcons()

        # display the icon that shows that an element is currently locked by another user
        if self.showLockedIcon:
            if self.context.wl_isLocked():
                icons.append(("lock_icon.png", translate("Locked", domain="plone", context=self.request)))

        # in case the contentIcon must be shown, the icon url is defined on the typeInfo
        if self.showContentIcon:
            typeInfo = getToolByName(self, 'portal_type')[self.context.portal_type]
            if typeInfo.icon_expr:
                # we assume that stored icon_expr is like string:${portal_url}/myContentIcon.png
                contentIcon = typeInfo.icon_expr.split('/')[-1]
                icons.append(contentIcon, translate(typeInfo.title,
                                                    doamin=typeInfo.i18n_domain,
                                                    context=self.request))

        # manage icons we want to be displayed after managed icons
        icons = icons + self._trailingIcons()
        return ' '.join([u"<img title='{0}' src='{1}' />".format(safe_unicode(icon[1]),
                                                                 "{0}/{1}".format(self.portal_url, icon[0]))
                         for icon in icons])

    def _leadingIcons(self):
        """See docstring in interfaces.py."""
        return []

    def _trailingIcons(self):
        """See docstring in interfaces.py."""
        return []
