# -*- coding: utf-8 -*-
#!/usr/bin/python

from telegram import User, Location, InlineQuery
from py_support.object_support import DefaultBuilder, get_object


INLINE_QUERY_MAPPING = {
    User: [('from')],
    Location: [('location')]
}


class InlineQueryBuilder(DefaultBuilder):
    prefix = None

    def __init__(self):
        self.prefix = 'inline_query'

    def _get_object(self, json_obj, model, key_index):
        return get_object(json_obj, model, key_index, self.prefix, INLINE_QUERY_MAPPING)

    # USER section
    def get_from(self, json_obj):
        return self._get_object(
            json_obj=json_obj, model=User, key_index=0
        )

    # LOCATION section
    def get_location(self, json_obj):
        return self._get_object(
            json_obj=json_obj, model=Location, key_index=0
        )

    def create_inline_query(self, json_obj):
        query_id = self._get_simple_field(json_obj, 'id')
        from_user = self.get_from(json_obj)
        location = self.get_location(json_obj)
        query = self._get_simple_field(json_obj, 'query')
        offset = self._get_simple_field(json_obj, 'offset')

        inline_query = InlineQuery(
            id=query_id, from_user=from_user, query=query, offset=offset
        )

        if location:
            inline_query.location = location

        return inline_query