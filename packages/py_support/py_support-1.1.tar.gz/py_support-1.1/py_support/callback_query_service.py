# -*- coding: utf-8 -*-
#!/usr/bin/python

from telegram import User, Message, CallbackQuery
from py_support.object_support import DefaultBuilder, get_object


CALLBACK_QUERY_MAPPING = {
    User: [('from')],
    Message: [('message')]
}


class CallbackQueryBuilder(DefaultBuilder):
    prefix = None

    def __init__(self):
        self.prefix = 'callback_query'

    def _get_object(self, json_obj, model, key_index):
        return get_object(json_obj, model, key_index, self.prefix, CALLBACK_QUERY_MAPPING)

    # USER section
    def get_from(self, json_obj):
        return self._get_object(
            json_obj=json_obj, model=User, key_index=0
        )

    # MESSAGE section
    def get_message(self, json_obj):
        return self._get_object(
            json_obj=json_obj, model=Message, key_index=0
        )

    def create_callback_query(self, json_obj):
        query_id = self._get_simple_field(json_obj, 'id')
        from_user = self.get_from(json_obj)
        message = self.get_message(json_obj)
        chat_instance = self._get_simple_field(json_obj, 'chat_instance')
        inline_message_id = self._get_simple_field(json_obj, 'inline_message_id')
        data = self._get_simple_field(json_obj, 'data')
        game_short_name = self._get_simple_field(json_obj, 'game_short_name')

        callback_query = CallbackQuery(
            id=query_id, from_user=from_user, chat_instance=chat_instance
        )

        if message:
            callback_query.message = message

        if inline_message_id:
            callback_query.inline_message_id = inline_message_id

        if data:
            callback_query.data = data

        if game_short_name:
            callback_query.game_short_name = game_short_name

        return callback_query