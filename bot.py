import telebot
import configure
from telebot import types

client = telebot.TeleBot(configure.config['token'])

@client.message_handler(commands = ['start'])
def info(message):
    markup_inline = types.InlineKeyboardMarkup()
    item_next = types.InlineKeyboardButton('Начать поиск', callback_data='start')
    markup_inline.add(item_next)
    client.send_message(message.chat.id, 'Приветствуем в нашем анонимной чате!\n\n'
                                         'Для того, чтобы начать поиск собеседников:\n/next\n'
                                         'Чтобы остановить диалог с собеседником: \n/stop\n\n'
                                         'Приятного общения!', reply_markup=markup_inline)


@client.callback_query_handler(func = lambda call: True)
def start(call):
    markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item_next = types.KeyboardButton('Следующий собеседник')
    item_stop = types.KeyboardButton('Остановить диалог')
    markup_reply.add(item_next, item_stop)
    client.send_message(call.message.chat.id, 'Вы успешно начали поиск!', reply_markup=markup_reply)
    client.answer_callback_query(callback_query_id=call.id)


@client.message_handler()
def next(message):
    pass
def stop(message):
    pass


client.polling(non_stop = True, interval = 0)

# @client.callback_query_handler(func = lambda call: True)
# def start(message):
#     markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
#     item_next = types.ReplyKeyboardMarkup('Следующий собеседник')
#     item_stop = types.ReplyKeyboardMarkup('Остановить диалог')
#     markup_reply.add(item_next, item_stop)
#     client.send_message(message.chat.id, 'Узнать информацию о себе?')
#
#
#
# @client.message_handler(content_types = ['text'])
# def get_text(message):
#     if message.text == 'Мой id':
#         client.send_message(message.chat.id, f'Ваш id: {message.from_user.id}')
#     elif message.text == 'Мой ник':
#         client.send_message(message.chat.id, f'Ваше имя: {message.from_user.first_name} {message.from_user.last_name}')



# def answer(call):
#     if call.data == 'yes':
#         markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
#         item_id = types.KeyboardButton('Мой id')
#         item_username = types.KeyboardButton('Мой ник')
#
#         markup_reply.add(item_id, item_username)
#         client.send_message(call.message.chat.id, 'Нажмите на одну из кнопок',
#                             reply_markup = markup_reply
#         )
#     elif call.data == 'no':
#         client.send_message(call.message.chat.id, 'ПОКА!!!!!!!!!!!!!!')



# @client.message_handler(commands = ['get_info', 'info'])
# def get_user_info(message):
#     markup_inline = types.InlineKeyboardMarkup()
#     item_yes = types.InlineKeyboardButton(text = 'ДА', callback_data = 'yes')
#     item_no = types.InlineKeyboardButton(text = 'НЕТ', callback_data = 'no')
#
#     markup_inline.add(item_yes, item_no)
#     client.send_message(message.chat.id, 'Узнать информацию о себе?',
#                         reply_markup = markup_inline
#     )
