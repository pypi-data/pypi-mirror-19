# -*- coding: utf-8 -*-
from plone.server.auth import authenticate_request
from plone.server.auth.groups import PloneGroup
from plone.server.auth.users import AnonymousUser
from plone.server.interfaces import IRequest
from plone.server.transactions import get_current_request
from zope.component import adapter
from zope.interface import implementer
from zope.security.interfaces import IParticipation


class AnonymousParticipation(object):

    def __init__(self, request):
        self.principal = AnonymousUser(request)
        self.principal._roles['plone.Anonymous'] = 1
        self.interaction = None


@adapter(IRequest)
@implementer(IParticipation)
class PloneParticipation(object):
    principal = None

    def __init__(self, request):
        self.request = request

    async def __call__(self):
        # Cached user
        if not hasattr(self.request, '_cache_user'):
            user = await authenticate_request(self.request)
            if user is not None:
                self.request._cache_user = user
                self.principal = user
        else:
            self.principal = getattr(self.request, '_cache_user', None)

        self.interaction = None


class ZopeAuthentication(object):
    """ Class used to get groups. """

    def getPrincipal(self, ident):
        request = get_current_request()
        if not hasattr(request, '_cache_groups'):
            request._cache_groups = {}
        if ident not in request._cache_groups.keys():
            request._cache_groups[ident] = PloneGroup(request, ident)
        return request._cache_groups[ident]
