# -*- coding: utf-8 -*-
#!/usr/bin/python

from telegram import Update, Message, InlineQuery, ChosenInlineResult, CallbackQuery
from py_support.object_support import DefaultBuilder, get_object


UPDATE_MAPPING = {
    Message: ('message', 'edited_message', 'channel_post', 'edited_channel_post'),
    InlineQuery: [('inline_query')],
    ChosenInlineResult: [('chosen_inline_result')],
    CallbackQuery: [('callback_query')]
}


class UpdateBuilder(DefaultBuilder):
    prefix = None

    def __init__(self):
        pass

    def _get_object(self, json_obj, model, key_index):
        return get_object(json_obj, model, key_index, self.prefix, UPDATE_MAPPING)

    # MESSAGE section
    def get_message(self, json_obj):
        json_obj['message']['from_user'] = json_obj['message']['from']
        del json_obj['message']['from']
        return self._get_object(
            json_obj=json_obj, model=Message, key_index=0
        )

    def get_edited_message(self, json_obj):
        return self._get_object(
            json_obj=json_obj, model=Message, key_index=1
        )

    def get_channel_post(self, json_obj):
        return self._get_object(
            json_obj=json_obj, model=Message, key_index=2
        )

    def get_edited_channel_post(self, json_obj):
        return self._get_object(
            json_obj=json_obj, model=Message, key_index=3
        )

    # InlineQuery section
    def get_inline_query(self, json_obj):
        return self._get_object(
            json_obj=json_obj, model=InlineQuery, key_index=0
        )

    # ChosenInlineResult section
    def get_chosen_inline_result(self, json_obj):
        return self._get_object(
            json_obj=json_obj, model=ChosenInlineResult, key_index=0
        )

    # CallbackQuery section
    def get_callback_query(self, json_obj):
        return self._get_object(
            json_obj=json_obj, model=CallbackQuery, key_index=0
        )

    def create_update(self, json_obj):
        update_id = self._get_simple_field(json_obj, 'update_id')
        message = self.get_message(json_obj)
        edited_message = self.get_edited_message(json_obj)
        channel_post = self.get_channel_post(json_obj)
        edited_channel_post = self.get_edited_channel_post(json_obj)
        inline_query = self.get_inline_query(json_obj)
        chosen_inline_result = self.get_chosen_inline_result(json_obj)
        callback_query = self.get_callback_query(json_obj)

        update = Update(
            update_id=update_id
        )

        if message:
            update.message = message

        if edited_message:
            update.edited_message = edited_message

        if channel_post:
            update.channel_post = channel_post

        if edited_channel_post:
            update.edited_channel_post = edited_channel_post

        if inline_query:
            update.inline_query = inline_query

        if chosen_inline_result:
            update.chosen_inline_result = chosen_inline_result

        if callback_query:
            update.callback_query = callback_query

        return update