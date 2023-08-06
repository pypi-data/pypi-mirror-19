from AccessControl import getSecurityManager
from collective.simplewiki.interfaces import ISimpleWikiLayer
from collective.simplewiki.interfaces import WRAPPER_CLASSNAME
from lxml.html import fromstring
from lxml.html import tostring
from plone import api
from plone.protect.auto import ProtectTransform
from plone.transformchain.interfaces import ITransform
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from zope.component import adapts
from zope.component import getMultiAdapter
from zope.interface import implements
from zope.interface import Interface
from Products.CMFPlone.utils import safe_unicode
from plone.i18n.normalizer.base import mapUnicode

import re


PAREN_RE = re.compile(r'\(\(([\w\W]+?)\)\)')  # matches ((Some Text To link 123))
BRACKET_RE = re.compile(r'\[\[([\w\W]+?)\]\]')  # matches [[Some Text To link 123]]
NUM_SORT_REGEX = re.compile('\d+')
MAX_SORTABLE_TITLE = 40


def zero_fill(matchobj):
    return matchobj.group().zfill(4)


def get_sortable_title(title):
    sortabletitle = mapUnicode(safe_unicode(title)).lower().strip()
    # Replace numbers with zero filled numbers
    sortabletitle = NUM_SORT_REGEX.sub(zero_fill, sortabletitle)
    # Truncate to prevent bloat, take bits from start and end
    if len(sortabletitle) > MAX_SORTABLE_TITLE:
        start = sortabletitle[:(MAX_SORTABLE_TITLE - 13)]
        end = sortabletitle[-10:]
        sortabletitle = start + '...' + end
    return sortabletitle.encode('utf-8')


class WikiTransform(ProtectTransform):
    implements(ITransform)
    adapts(Interface, ISimpleWikiLayer)  # any context, any request

    order = 8999

    def __init__(self, published, request):
        super(WikiTransform, self).__init__(published, request)
        self.catalog = api.portal.get_tool('portal_catalog')
        self.sm = getSecurityManager()
        self.context_state = getMultiAdapter((self.getContext(), self.request),
                                             name='plone_context_state')

    def transformIterable(self, result, encoding):
        resultTree = self.parseTree(result, encoding)
        if resultTree is None:
            return None
        root = resultTree.tree.getroot()

        for el in root.cssselect('.' + WRAPPER_CLASSNAME):
            # get raw html
            html = original_html = tostring(el)
            for pattern in (PAREN_RE, BRACKET_RE):
                result = []
                for idx, val in enumerate(pattern.split(html)):
                    # with this split, every other is a wiki link
                    if idx % 2 != 0:
                        val = self.resolve_link(val)
                    result.append(val)
                html = ''.join(result)

            if original_html != html:
                # set new html on output...
                new_el = fromstring(html)
                el.getparent().replace(el, new_el)
        return resultTree

    def make_link(self, obj, name):
        title = obj.Title() or obj.getId()

        if not self.sm.checkPermission('View', obj):
            return '{}[no access to link]'.format(name or title)

        return '<a href="{}" title="{}">{}</a>'.format(
            obj.absolute_url(),
            title,
            name or title
        )

    def can_add(self, folder, type_id):
        constraints = ISelectableConstrainTypes(folder, None)
        addable = None
        if constraints is not None:
            addable = constraints.getLocallyAllowedTypes()

        if addable is None:
            addable = [t.getId() for t in folder.allowedContentTypes()]

        if type_id not in addable:
            return False
        return True

    def make_add_link(self, folder, id_, name):
        pt = self.getContext().portal_type
        if self.can_add(folder, pt):
            return '<a href="{}/++add++{}?form.widgets.IShortName.id={}&form.widgets.IDublinCore.title={}" title="Create missing content">+ {}</a>'.format(  # noqa
                folder.absolute_url(),
                pt,
                id_,
                name or id_,
                name or id_
            )
        else:
            return '{}[missing page]'.format(name or id_)

    def resolve_link(self, link):
        """
        A link will resolve under one of the following conditions:

         1. a matching id within the same folder
         2. a matching title within the same folder
         3. a matching id somewhere else in the site
         4. a matching title somewhere else in the site
        """
        id_, _, name = link.partition('|')
        folder = self.context_state.folder()
        if id_ in folder:
            ob = folder[id_]
            return self.make_link(ob, name)

        sortable_title = get_sortable_title(name or id_)
        brains = self.catalog(
            path={
                'query': '/'.join(folder.getPhysicalPath()),
                'depth': 1
            },
            sortable_title=sortable_title,
            sort_on="created",
            sort_order="reverse"
        )
        if len(brains) > 0:
            return self.make_link(brains[0].getObject(), name)

        brains = self.catalog(id=id_, sort_on="created", sort_order="reverse")
        if len(brains) > 0:
            return self.make_link(brains[0].getObject(), name)

        brains = self.catalog(sortable_title=sortable_title,
                              sort_on="created", sort_order="reverse")
        if len(brains) > 0:
            return self.make_link(brains[0].getObject(), name)

        return self.make_add_link(folder, id_, name)
