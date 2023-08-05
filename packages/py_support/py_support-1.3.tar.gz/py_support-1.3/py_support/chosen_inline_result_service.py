# -*- coding: utf-8 -*-
#!/usr/bin/python

from telegram import User, Location, ChosenInlineResult
from py_support.object_support import DefaultBuilder, get_object

INLINE_RESULT_MAPPING = {
    User: [('from')],
    Location: [('location')]
}


class ChosenInlineResultBuilder(DefaultBuilder):
    prefix = None

    def __init__(self):
        self.prefix = 'chosen_inline_result'

    def _get_object(self, json_obj, model, key_index):
        return get_object(json_obj, model, key_index, self.prefix, INLINE_RESULT_MAPPING)

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

    def create_chosen_inline_result(self, json_obj):
        result_id = self._get_simple_field(json_obj, 'result_id')
        from_user = self.get_from(json_obj)
        location = self.get_location(json_obj)
        query = self._get_simple_field(json_obj, 'query')
        inline_message_id = self._get_simple_field(json_obj, 'inline_message_id')

        chosen_inline_result = ChosenInlineResult(
            id=result_id, from_user=from_user, query=query
        )

        if location:
            chosen_inline_result.location = location

        if inline_message_id:
            chosen_inline_result.inline_message_id = inline_message_id

        return chosen_inline_result