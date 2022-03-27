import telebot
import configure
from telebot import types
from database import Database

db = Database('db.db')
client = telebot.TeleBot(configure.config['token'])


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Поиск собеседника')
    markup.add(item1)
    return markup


def stop_dialog():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Сказать свой профиль')
    item2 = types.KeyboardButton('/stop')
    markup.add(item1, item2)
    return markup


def stop_search():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Остановить поиск')
    markup.add(item1)
    return markup

@client.message_handler(commands = ['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Я парень')
    item2 = types.KeyboardButton('Я девушка')
    markup.add(item1, item2)

    client.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Добро пожаловать в анонимный чат!'
                                         'Укажите ваш пол. ', reply_markup=markup)


@client.message_handler(commands = ['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Поиск собеседника')
    markup.add(item1)

    client.send_message(message.chat.id, 'Меню', reply_markup=markup)


@client.message_handler(commands = ['stop'])
def stop(message):
    chat_info = db.get_active_chat(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Следующий диалог')
    item2 = types.KeyboardButton('/menu')
    markup.add(item1, item2)
    if chat_info != False:
        db.delete_chat(chat_info[0])

        client.send_message(chat_info[1], 'Собеседник покинул чат', reply_markup=markup)
        client.send_message(message.chat.id, 'Вы вышли из чата', reply_markup=markup)
    else:
        client.send_message(message.chat.id, 'Вы не начали чат', reply_markup=markup)



@client.message_handler(content_types= ['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Поиск собеседника' or message.text == 'Следующий диалог':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Парень')
            item2 = types.KeyboardButton('Девушка')
            item3 = types.KeyboardButton('Рандом')
            markup.add(item1, item2, item3)

            client.send_message(message.chat.id, 'Кого искать?', reply_markup=markup)

        elif message.text == 'Остановить поиск':
            db.delete_queue(message.chat.id)
            client.send_message(message.chat.id, 'Поиск остановлен, напишите /menu', reply_markup=main_menu())

        elif message.text == 'Парень':
            user_info = db.get_gender_chat('male')
            chat_two = user_info[0]
            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                client.send_message(message.chat.id, 'Поиск собеседника', reply_markup=stop_search())
            else:
                mess = 'Собеседник найден! Чтобы остановить диалог, напишите /stop'

                client.send_message(message.chat.id, mess, reply_markup=stop_dialog())
                client.send_message(chat_two, mess, reply_markup=stop_dialog())

        elif message.text == 'Девушка':
            user_info = db.get_gender_chat('female')
            chat_two = user_info[0]
            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                client.send_message(message.chat.id, 'Поиск собеседника', reply_markup=stop_search())
            else:
                mess = 'Собеседник найден! Чтобы остановить диалог, напишите /stop'

                client.send_message(message.chat.id, mess, reply_markup=stop_dialog())
                client.send_message(chat_two, mess, reply_markup=stop_dialog())

        elif message.text == 'Рандом':
            user_info = db.get_chat()
            chat_two = user_info[0]

            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                client.send_message(message.chat.id, 'Поиск собеседника', reply_markup=stop_search())
            else:
                mess = 'Собеседник найден! Чтобы остановить диалог, напишите /stop'

                client.send_message(message.chat.id, mess, reply_markup=stop_dialog())
                client.send_message(chat_two, mess, reply_markup=stop_dialog())

        elif message.text == 'Я парень':
            if db.set_gender(message.chat.id, 'male'):
                client.send_message(message.chat.id, 'Ваш пол успешно добавлен!', reply_markup=main_menu())
            else:
                client.send_message(message.chat.id, 'Вы уже указали пол. Напишите админу: @dfilinov8\n'
                                                     'Чтобы вернуться напишите /menu')
        elif message.text == 'Я девушка':
            if db.set_gender(message.chat.id, 'female'):
                client.send_message(message.chat.id, 'Ваш пол успешно добавлен!', reply_markup=main_menu())
            else:
                client.send_message(message.chat.id, 'Вы уже указали пол. Напишите админу: @dfilinov8\n'
                                                     'Чтобы вернуться напишите /menu')
        else:
            if db.get_active_chat(message.chat.id) != False:
                chat_info = db.get_active_chat(message.chat.id)
                client.send_message(chat_info[1], message.text)
            else:
                client.send_message(message.chat.id, 'Вы не начали диалог')

client.polling(non_stop = True, interval = 0)