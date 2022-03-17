import telebot
import configure
from telebot import types
from database import Database

db = Database('db.db')
client = telebot.TeleBot(configure.config['token'])

@client.message_handler(commands = ['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Поиск собеседника')
    markup.add(item1)

    client.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Добро пожаловать в анонимный чат!'
                                         'Нажмите на поиск собеседника. ', reply_markup=markup)


@client.message_handler(commands = ['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Поиск собеседника')
    markup.add(item1)

    client.send_message(message.chat.id, 'Меню', reply_markup=markup)


@client.message_handler(content_types= ['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Поиск собеседника':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Остановить поиск')
            markup.add(item1)

            chat_two = db.get_chat() # получение id собеседника, который стоит в очереди первый

            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_queue(message.chat.id)
                client.send_message(message.chat.id, 'Поиск собеседника', reply_markup=markup)

        elif message.text == 'Остановить поиск':
            db.delete_queue(message.chat.id)
            client.send_message(message.chat.id, 'Поиск остановлен, напишите /menu')

client.polling(non_stop = True, interval = 0)