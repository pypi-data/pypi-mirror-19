# -*- coding: utf-8 -*-
#!/usr/bin/python

from py_support.telebot.update_service import UpdateBuilder
from telegram import Bot
from telegram.error import InvalidToken
from object_support import logger
update_builder = UpdateBuilder()

# what we can catch with update - for UpdateReactor
# WE DO NOT USE THIS VALUES YET! x)
UPDATE_TYPE = ['message', 'edited_message', 'channel_post', 'edited_channel_post',
    'inline_query', 'chosen_inline_result', 'callback_query']


def get_update(json_update):
    """ get update model (last entitie is still in json)"""
    return update_builder.create_update(json_obj=json_update)


class UpdateReactor:
    bot = None

    @staticmethod
    def _get_bot(token):
        bot = Bot(token=token)
        return bot

    @staticmethod
    def _is_it_command(message):
        if message.entities:
            for ent in message.entities:
                for key in ent:
                    if key == 'type' and ent[key] == 'bot_command':
                        return True
        return False

    def __init__(self, token):
        try:
            self.bot = self._get_bot(token)
        except InvalidToken:
            logger.err('wrong telebot token: %s' % token)

    def _send_simple_message(self, chat_id, message_text, keyboard):
        try:
            self.bot.sendMessage(chat_id=chat_id,
                                 text=message_text, reply_markup=keyboard)
        except Exception as e:
            logger.err('can not send simple message to %s, %s' % (chat_id, e))

    def react(self, update, message_text, keyboard):
        """ it will react for updates with message and keyboard """
        # if it's message update type
        if update.message:
            message = update.message
            self._send_simple_message(message.from_user['id'], message_text, keyboard)
            if message.text:
                # command
                if self._is_it_command(message):
                    pass
                # simple message
                else:
                    pass
            # message - not command and not simple message
            else:
                pass
        # edited message
        elif update.edited_message:
            pass
        # channel post
        elif update.channel_post:
            pass
        # edited channel post
        elif update.edited_channel_post:
            pass
        # inline query
        elif update.inline_query:
            pass
        # chosen inline result
        elif update.chosen_inline_result:
            pass
        # callback query
        elif update.callback_query:
            pass
        # something new!
        else:
            pass


