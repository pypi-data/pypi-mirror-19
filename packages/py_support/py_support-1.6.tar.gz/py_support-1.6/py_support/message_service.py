# -*- coding: utf-8 -*-
#!/usr/bin/python

from telegram import (
    User, Message, Chat, MessageEntity, Audio, Document, Game, PhotoSize, Sticker,
    Video, Voice, Contact, Location, Venue
)

from py_support.object_support import DefaultBuilder, get_object

MESSAGE_MAPPING = {
    Message: ('reply_to_message', 'pinned_message'),
    User: ('from', 'forward_from',
                    'new_chat_member', 'left_chat_member'),
    Chat: ('chat', 'forward_from_chat'),
    MessageEntity: (['entities']),
    Audio: [('audio')],
    Document: [('document')],
    Game: [('game')],
    PhotoSize: [('photo'), ('new_chat_photo')],
    Sticker: [('sticker')],
    Video: [('video')],
    Voice: [('voice')],
    Contact: [('contact')],
    Location: [('location')],
    Venue: [('venue')],
}


class MessageBuilder(DefaultBuilder):
    prefix = None

    def __init__(self):
        self.prefix = 'message'

    def _get_object(self, json_obj, model, key_index):
        return get_object(json_obj, model, key_index, self.prefix, MESSAGE_MAPPING)

    # MESSAGE section
    def get_reply_to_message(self, json_obj):
        return self._get_object(
            json_obj=json_obj, model=Message, key_index=0
        )

    def get_pinned_message(self, json_obj):
        return self._get_object(
            json_obj=json_obj, model=Message, key_index=1
        )

    # USER section
    def get_from(self, json_obj):
        return self._get_object(
            json_obj=json_obj, model=User, key_index=0
        )

    def get_forward_from(self, json_obj):
        return self._get_object(
            json_obj=json_obj, model=User, key_index=1
        )

    def get_new_chat_member(self, json_obj):
        return self._get_object(
            json_obj=json_obj, model=User, key_index=2
        )

    def get_left_chat_member(self, json_obj):
        return self._get_object(
            json_obj=json_obj, model=User, key_index=3
        )

    # CHAT section
    def get_chat(self, json_obj):
        return self._get_object(
            json_obj=json_obj, model=Chat, key_index=0
        )

    def get_forward_from_chat(self, json_obj):
        return self._get_object(
            json_obj=json_obj, model=Chat, key_index=1
        )

    # MessageEntity section
    def get_message_entities(self, json_obj):
        return self._get_object(
            json_obj=json_obj, model=MessageEntity, key_index=0
        )

    # AUDIO section
    def get_audio(self, json_obj):
        return self._get_object(
            json_obj=json_obj, model=Audio, key_index=0
        )

    # DOCUMENT section
    def get_document(self, json_obj):
        return self._get_object(
            json_obj=json_obj, model=Document, key_index=0
        )

    # GAME section
    def get_game(self, json_obj):
        return self._get_object(
            json_obj=json_obj, model=Game, key_index=0
        )

    # PHOTO SIZE section
    def get_photo(self, json_obj):
        return self._get_object(
            json_obj=json_obj, model=PhotoSize, key_index=0
        )

    def get_new_chat_photo(self, json_obj):
        return self._get_object(
            json_obj=json_obj, model=PhotoSize, key_index=1
        )

    # STICKER section
    def get_sticker(self, json_obj):
        return self._get_object(
            json_obj=json_obj, model=Sticker, key_index=0
        )

    # VIDEO section
    def get_video(self, json_obj):
        return self._get_object(
            json_obj=json_obj, model=Video, key_index=0
        )

    # VOICE section
    def get_voice(self, json_obj):
        return self._get_object(
            json_obj=json_obj, model=Voice, key_index=0
        )

    # CONTACT section
    def get_contact(self, json_obj):
        return self._get_object(
            json_obj=json_obj, model=Contact, key_index=0
        )

    # LOCATION section
    def get_location(self, json_obj):
        return self._get_object(
            json_obj=json_obj, model=Location, key_index=0
        )

    # VENUE section
    def get_venue(self, json_obj):
        return self._get_object(
            json_obj=json_obj, model=Venue, key_index=0
        )

    def create_message(self, json_obj):
        """ this is like a magic - will create a valid message object """
        message_id = self._get_simple_field(json_obj, 'message_id')
        message_from = self.get_from(json_obj)
        message_date = self._get_simple_field(json_obj, 'date')
        message_chat = self.get_chat(json_obj)
        forward_from = self.get_forward_from(json_obj)
        forward_from_chat = self.get_forward_from_chat(json_obj)
        forward_from_message_id = self._get_simple_field(json_obj, 'forward_from_message_id')
        forward_date = self._get_simple_field(json_obj, 'forward_date')
        reply_to_message = self.get_reply_to_message(json_obj)
        edit_date = self._get_simple_field(json_obj, 'edit_date')
        text = self._get_simple_field(json_obj, 'text')
        entities = self.get_message_entities(json_obj)
        audio = self.get_audio(json_obj)
        document = self.get_document(json_obj)
        game = self.get_game(json_obj)
        photo = self.get_photo(json_obj)
        sticker = self.get_sticker(json_obj)
        video = self.get_video(json_obj)
        voice = self.get_voice(json_obj)
        caption = self._get_simple_field(json_obj, 'caption')
        contact = self.get_contact(json_obj)
        location = self.get_location(json_obj)
        venue = self.get_venue(json_obj)
        new_chat_member = self.get_new_chat_member(json_obj)
        left_chat_member = self.get_left_chat_member(json_obj)
        new_chat_title = self._get_simple_field(json_obj, 'new_chat_title')
        new_chat_photo = self.get_new_chat_photo(json_obj)
        delete_chat_photo = self._get_simple_field(json_obj, 'delete_chat_title')
        group_chat_created = self._get_simple_field(json_obj, 'group_chat_created')
        supergroup_chat_created = self._get_simple_field(json_obj, 'supergroup_chat_created')
        channel_chat_created = self._get_simple_field(json_obj, 'channel_chat_created')
        migrate_to_chat_id = self._get_simple_field(json_obj, 'migrate_to_chat_id')
        migrate_from_chat_id = self._get_simple_field(json_obj, 'migrate_from_chat_id')
        pinned_message = self.get_pinned_message(json_obj)

        self.logger.info("\n\n id=%s\n from=%s\n date=%s\n chat=%s\n" %
        (message_id, message_from, message_date, message_chat))

        # create basic message
        message = Message(
            message_id=message_id, from_user=message_from, date=message_date, chat=message_chat
        )
        # fill if with optional data
        if forward_from:
            message.forward_from = forward_from
        if forward_from_chat:
            message.forward_from_chat = forward_from_chat
        if forward_from_message_id:
            message.forward_from_message_id = forward_from_message_id
        if forward_date:
            message.forward_date = forward_date
        if reply_to_message:
            message.reply_to_message = reply_to_message
        if edit_date:
            message.edit_date = edit_date
        if text:
            message.text = text
        if audio:
            message.audio = audio
        if document:
            message.document = document
        if game:
            message.game = game
        if photo:
            message.photo = photo
        if sticker:
            message.sticker = sticker
        if video:
            message.video = video
        if voice:
            message.voice = voice
        if caption:
            message.caption = caption
        if contact:
            message.contact = contact
        if location:
            message.location = location
        if new_chat_member:
            message.new_chat_member = new_chat_member
        if left_chat_member:
            message.left_chat_member = left_chat_member
        if new_chat_title:
            message.new_chat_title = new_chat_title
        if new_chat_photo:
            message.new_chat_photo = new_chat_photo
        if delete_chat_photo:
            message.delete_chat_photo = delete_chat_photo
        if group_chat_created:
            message.group_chat_created = group_chat_created
        if supergroup_chat_created:
            message.supergroup_chat_created = supergroup_chat_created
        if migrate_to_chat_id:
            message.migrate_to_chat_id = migrate_to_chat_id
        if migrate_from_chat_id:
            message.migrate_from_chat_id = migrate_from_chat_id
        if channel_chat_created:
            message.channel_chat_created = channel_chat_created
        if entities:
            message.entities = entities
        if venue:
            message.venue = venue
        if pinned_message:
            message.pinned_message = pinned_message

        return message