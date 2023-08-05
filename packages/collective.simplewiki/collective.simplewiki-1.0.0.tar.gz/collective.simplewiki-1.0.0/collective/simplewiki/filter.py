from collective.simplewiki.interfaces import WRAPPER_CLASSNAME
from plone.outputfilters.interfaces import IFilter
from zope.interface import implements


class WikiFilter(object):
    """
    this filter is ONLY to add a wrapper on filtered output so we can
    transform in a later step.

    The reason we don't do all the dirty work here is because output filters
    are cached and pages would be broken after you created new pages.
    """
    implements(IFilter)

    order = 99999

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def is_enabled(self):
        return True

    def __call__(self, txt):
        return '<div class="{}">{}</div>'.format(
            WRAPPER_CLASSNAME, txt
        )
