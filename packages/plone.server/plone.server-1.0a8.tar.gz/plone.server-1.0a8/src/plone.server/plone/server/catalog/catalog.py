# -*- coding: utf-8 -*-
from plone.server.content import iter_schemata_for_type
from plone.server.directives import index
from plone.server.directives import merged_tagged_value_dict
from plone.server.directives import merged_tagged_value_list
from plone.server.directives import metadata
from plone.server.interfaces import ICatalogDataAdapter
from plone.server.interfaces import ICatalogUtility
from plone.server.json.serialize_value import json_compatible
from zope.component import queryAdapter
from zope.interface import implementer
from zope.securitypolicy.principalpermission import principalPermissionManager
from zope.securitypolicy.rolepermission import rolePermissionManager


global_principal_permission_setting = principalPermissionManager.getSetting
global_roles_for_permission = rolePermissionManager.getRolesForPermission


@implementer(ICatalogUtility)
class DefaultSearchUtility(object):

    async def search(self, query):
        pass

    async def get_by_uuid(self, uuid):
        pass

    async def get_object_by_uuid(self, uuid):
        pass

    async def get_by_type(self, doc_type, query={}):
        pass

    async def get_by_path(self, path, depth, doc_type=None):
        pass

    async def get_folder_contents(self, obj):
        pass

    async def index(self, datas):
        """
        {uid: <dict>}
        """
        pass

    async def remove(self, uids):
        """
        list of UIDs to remove from index
        """
        pass

    async def reindex_all_content(self):
        """ For all Dexterity Content add a queue task that reindex the object
        """
        pass

    async def initialize_catalog(self):
        """ Creates an index
        """
        pass

    async def remove_catalog(self):
        """ Deletes an index
        """
        pass

    def get_data(self, content):
        data = {}
        adapter = queryAdapter(content, ICatalogDataAdapter)
        if adapter:
            data.update(adapter())
        return data


@implementer(ICatalogDataAdapter)
class DefaultCatalogDataAdapter(object):

    def __init__(self, content):
        self.content = content

    def get_data(self, ob, iface, field_name):
        try:
            field = iface[field_name]
            real_field = field.bind(ob)
            try:
                value = real_field.get(ob)
                json_compatible(value)
            except AttributeError:
                pass
        except KeyError:
            pass

        return json_compatible(getattr(ob, field_name, None))

    def __call__(self):
        # For each type
        values = {}
        for schema in iter_schemata_for_type(self.content.portal_type):
            behavior = schema(self.content)
            for index_name, index_data in merged_tagged_value_dict(schema, index.key).items():
                if 'accessor' in index_data:
                    values[index_name] = index_data['accessor'](behavior)
                else:
                    values[index_name] = self.get_data(behavior, schema, index_name)
            for metadata_name in merged_tagged_value_list(schema, metadata.key):
                values[index_name] = self.get_data(behavior, schema, index_name)

        return values
