# -*- coding: utf-8 -*-
#!/usr/bin/python
import emoji
from py_support.object_support import logger
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup
from telegram import KeyboardButton

EMO_CODES = {
    'game': ':game_die:', 'shit': ':shit:',
    'boom': ':boom:', 'man': ':guardsman:'
}


def get_emotion(emo_code):
    emo = emoji.emojize(EMO_CODES[emo_code], use_aliases=True)
    return emo


def get_buttons_line(btn_captions, is_inline):
    buttons_line = []
    for emo_caption_dict in btn_captions:
        for emo_code in emo_caption_dict:
            button_text = '%s %s' % (get_emotion(emo_code), emo_caption_dict[emo_code])
            if not is_inline:
                button = KeyboardButton(button_text)
            else:
                button = InlineKeyboardButton(text=button_text, callback_data=emo_code)
            buttons_line.append(button)
    return buttons_line


def get_buttons_set(markup):
    """ markup is dict format: {'1': buttons_line } """
    """ buttons line is list or tuple """
    if type(markup) is dict:
        buttons_set = []
        for line_number in markup:
            buttons_line = markup[line_number]
            buttons_set.append(buttons_line)
        return buttons_set
    else:
        logger.err("Markup should be in format: {'1': buttons_line }, where buttons_line is dict ")
        return None


def get_markup(buttons_lines_list):
    markup = {}
    for ind, button_line in enumerate(buttons_lines_list):
        markup[str(ind)] = button_line
    return markup


def get_keyboard(buttons_set):
    first_button = buttons_set[0][0]
    if not isinstance(first_button, InlineKeyboardButton):
        keyboard = ReplyKeyboardMarkup(keyboard=buttons_set)
    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons_set)
    return keyboard