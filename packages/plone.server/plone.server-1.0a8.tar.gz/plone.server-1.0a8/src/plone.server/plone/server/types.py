from plone.server.content import get_cached_factory
from plone.server.interfaces import IConstrainTypes
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(IConstrainTypes)
@adapter(Interface)
class FTIConstrainAllowedTypes(object):

    def __init__(self, context: Interface):
        self.context = context

    def is_type_allowed(self, type_id: str) -> bool:
        allowed = self.get_allowed_types()
        if allowed is None:
            # not define
            return True
        return type_id in allowed

    def get_allowed_types(self) -> list:
        pt = getattr(self.context, 'portal_type', None)
        if pt:
            factory = get_cached_factory(pt)
            return factory.allowed_types
        return None
