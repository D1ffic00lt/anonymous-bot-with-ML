import telebot
import configure
import threading
from telebot import types
from database import Database
import pickle                                                                        # Loading library for reading models
from ModelLibrary.predict import GetToxicity                                    # Loading the training program
import nltk
from datetime import datetime
import json
import os
from langdetect.lang_detect_exception import LangDetectException
print("\n" + "Program started" + "\n")
nltk.download('punkt')
nltk.download('stopwords')


with open("ModelLibrary/models/EnglishModel.bf", "rb") as EnglishModel, \
        open("ModelLibrary/models/RussianModel.bf", "rb") as RussianModel:  # Loading Models
    models_ = [pickle.load(RussianModel), pickle.load(EnglishModel)]  # Loading Models

with open("ModelLibrary/models/RussianVectorizer.bf", "rb") as RussianVectorizer, \
        open("ModelLibrary/models/EnglishVectorizer.bf", "rb") as EnglishVectorizer:  # Loading vectorizervectorizers_ = [pickle.load(RussianVectorizer), pickle.load(EnglishVectorizer)]  # Loading vectorizers
    vectorizers_ = [pickle.load(RussianVectorizer), pickle.load(EnglishVectorizer)]


lock = threading.Lock()


db = Database('db.db')
client = telebot.TeleBot(configure.config['token'])
print("Bot connected")
db.restart()


month = int(datetime.today().strftime('%m'))
day = int(datetime.today().strftime('%d'))
if not os.path.exists("last_save.json"):
    with open('last_save.json', 'w+') as outfile:
        json.dump({
            "day": day,
            "month": month,
        }, outfile)
else:
    with open("last_save.json", "r") as f:
        data = json.loads(f.read())
        day_json = data["day"]
        month_json = data["month"]
    if (day > day_json and month == month_json) or \
            (day < day_json and month > month_json) or \
            (month == 1 and day == 1 and day < day_json):
        with open('last_save.json', 'w+') as outfile:
            json.dump({
                "day": day,
                "month": month,
            }, outfile)


rating = {}

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


@client.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Я парень')
    item2 = types.KeyboardButton('Я девушка')
    markup.add(item1, item2)

    client.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Добро пожаловать в анонимный чат!'
                                         'Укажите ваш пол. ', reply_markup=markup)

@client.message_handler(commands=['help'])
def help(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Поиск собеседника')
    item2 = types.KeyboardButton('Меню')
    markup.add(item1, item2)

    client.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Добро пожаловать в анонимный чат!'
                                         'Укажите ваш пол. ', reply_markup=markup)


@client.message_handler(commands=['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Поиск собеседника')
    markup.add(item1)

    keyboard = types.InlineKeyboardMarkup()
    key1 = types.InlineKeyboardButton(text='Следующий собеседник', callback_data='search', row_width=3)
    keyboard.add(key1)
    client.send_message(message.chat.id, '···МЕНЮ···\n'
                                         'Ваш профиль (виден только Вам):\n'
                                         f'Имя: {message.from_user.first_name}\n'
                                         f'Пол: {"Мужской" if db.get_gender(message.chat.id) == "male" else "Женский"}\n'
                                         f'Рейтинг: {db.get_rating(message.chat.id)[0]:.4f}\n'
                                         f'/help - помощь в использовании бота', reply_markup=keyboard)

    @client.callback_query_handler(func=lambda call: True)
    def callback_work(call):
        if call.data == 'search':
            if not db.is_register(message.chat.id) and message.text != '/start':
                client.send_message(message.chat.id, 'Вы не зарегистрировались! Напишите /start для регистрации!')
            else:
                markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton('Парень')
                item2 = types.KeyboardButton('Девушка')
                item3 = types.KeyboardButton('Любое')
                markup2.add(item1, item2, item3)

                client.send_message(message.chat.id, 'Кого искать?', reply_markup=markup2)
        client.answer_callback_query(callback_query_id=call.id) # должно убрать часы на кнопке


@client.message_handler(commands=['stop'])
def stop(message):
    chat_info = db.get_active_chat(message.chat.id)

    keyboard = types.InlineKeyboardMarkup()
    key1 = types.InlineKeyboardButton(text='Спам', callback_data='spam', row_width=3)
    key2 = types.InlineKeyboardButton(text='Обман', callback_data='deceit', row_width=3)
    key3 = types.InlineKeyboardButton(text='Продажа', callback_data='sale', row_width=3)
    key4 = types.InlineKeyboardButton(text='18+', callback_data='18+', row_width=3)
    key5 = types.InlineKeyboardButton(text='Следующий собеседник', callback_data='search', row_width=1)
    keyboard.add(key1)
    keyboard.add(key2)
    keyboard.add(key3)
    keyboard.add(key4)
    keyboard.add(key5)

    @client.callback_query_handler(func=lambda call: True)
    def callback_worker(call):
        print(call)
        if call.data == 'spam':
            markup = types.InlineKeyboardMarkup()
            item = types.InlineKeyboardButton(text='Поиск собеседника', callback_data='search')
            markup.add(item)
            client.edit_message_text(chat_id=call.from_user.id, message_id=call.message.id, text="Жалоба отправлена", reply_markup=markup)
        elif call.data == 'deceit':
            markup = types.InlineKeyboardMarkup()
            item = types.InlineKeyboardButton(text='Поиск собеседника', callback_data='search')
            markup.add(item)
            client.edit_message_text(chat_id=call.from_user.id, message_id=call.message.id, text="Жалоба отправлена", reply_markup=markup)
        elif call.data == 'sale':
            markup = types.InlineKeyboardMarkup()
            item = types.InlineKeyboardButton(text='Поиск собеседника', callback_data='search')
            markup.add(item)
            client.edit_message_text(chat_id=call.from_user.id, message_id=call.message.id, text="Жалоба отправлена", reply_markup=markup)
        elif call.data == '18+':
            markup = types.InlineKeyboardMarkup()
            item = types.InlineKeyboardButton(text='Поиск собеседника', callback_data='search')
            markup.add(item)
            client.edit_message_text(chat_id=call.from_user.id, message_id=call.message.id, text="Жалоба отправлена", reply_markup=markup)
        elif call.data == 'search':
            if not db.is_register(message.chat.id) and message.text != '/start':
                client.send_message(message.chat.id, 'Вы не зарегистрировались! Напишите /start для регистрации!')
            else:
                markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton('Парень')
                item2 = types.KeyboardButton('Девушка')
                item3 = types.KeyboardButton('Любое')
                markup2.add(item1, item2, item3)

                client.send_message(message.chat.id, 'Кого искать?', reply_markup=markup2)
        client.answer_callback_query(callback_query_id=call.id) # должно убрать часы на кнопке


    if chat_info != False:
        db.delete_chat(chat_info[0])

        client.send_message(chat_info[1], 'Собеседник покинул чат\n\nВы можете оставить жалобу на вашего собеседника:', reply_markup=keyboard)
        client.send_message(message.chat.id, 'Вы вышли из чата\n\nВы можете оставить жалобу на вашего собеседника:', reply_markup=keyboard)

        db.change_rating(message.chat.id, rating[str(message.chat.id)])
        db.change_rating(chat_info[1], rating[str(chat_info[1])])
        del rating[str(message.chat.id)]
        del rating[str(chat_info[1])]
    else:
        client.send_message(message.chat.id, 'Вы не начали диалог!', reply_markup=keyboard)


@client.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Поиск собеседника' or message.text == 'Следующий диалог':
            if not db.is_register(message.chat.id) and message.text != '/start':
                client.send_message(message.chat.id, 'Вы не зарегистрировались! Напишите /start для регистрации!')
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton('Парень')
                item2 = types.KeyboardButton('Девушка')
                item3 = types.KeyboardButton('Любое')
                markup.add(item1, item2, item3)

                client.send_message(message.chat.id, 'Кого искать?', reply_markup=markup)

        elif message.text == 'Остановить поиск':
            db.delete_queue(message.chat.id)
            client.send_message(message.chat.id, 'Поиск остановлен:\n'
                                                 '· Напишите /menu для выхода в меню\n'
                                                 '· Нажмите на кнопку "Поиск собеседника", чтобы найти следующий диалог', reply_markup=main_menu())

        elif message.text == 'Парень':
            user_info = db.get_gender_chat('male')
            chat_two = user_info[0]
            if db.create_chat(message.chat.id, chat_two) is False:
                db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                client.send_message(message.chat.id, 'Поиск собеседника', reply_markup=stop_search())
            else:
                mess = 'Собеседник найден! Чтобы остановить диалог, напишите /stop'

                client.send_message(message.chat.id, mess, reply_markup=stop_dialog())
                client.send_message(chat_two, mess, reply_markup=stop_dialog())
                rating[str(message.chat.id)] = 0
                rating[str(chat_two)] = 0
                print(rating)

        elif message.text == 'Девушка':
            user_info = db.get_gender_chat('female')
            chat_two = user_info[0]
            if db.create_chat(message.chat.id, chat_two) is False:
                db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                client.send_message(message.chat.id, 'Поиск собеседника', reply_markup=stop_search())
            else:
                mess = 'Собеседник найден! Чтобы остановить диалог, напишите /stop'

                client.send_message(message.chat.id, mess, reply_markup=stop_dialog())
                client.send_message(chat_two, mess, reply_markup=stop_dialog())
                rating[str(message.chat.id)] = 0
                rating[str(chat_two)] = 0
                print(rating)

        elif message.text == 'Любое':
            user_info = db.get_chat()
            chat_two = user_info[0]

            if db.create_chat(message.chat.id, chat_two) is False:
                db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                client.send_message(message.chat.id, 'Поиск собеседника', reply_markup=stop_search())
            else:
                mess = 'Собеседник найден! Чтобы остановить диалог, напишите /stop'

                client.send_message(message.chat.id, mess, reply_markup=stop_dialog())
                client.send_message(chat_two, mess, reply_markup=stop_dialog())
                rating[str(message.chat.id)] = 0
                rating[str(chat_two)] = 0
                print(rating)

        elif message.text == 'Сказать свой профиль':
            chat_info = db.get_active_chat(message.chat.id)
            if chat_info is not False:
                if message.from_user.username:
                    client.send_message(chat_info[1], '@' + message.from_user.username)
                    client.send_message(message.chat.id, 'Вы сказали свой профиль')
                else:
                    client.send_message(message.chat.id, 'В вашем аккаунте не указан username')
            else:
                client.send_message(message.chat.id, 'Вы не начали диалог!')

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
            if db.get_active_chat(message.chat.id) is not False:
                chat_info = db.get_active_chat(message.chat.id)
                client.send_message(chat_info[1], message.text)
                try:
                    toxicity = GetToxicity(message.text, models=models_, vectorizers=vectorizers_)[1]
                    toxicity_score = 70 - (toxicity * 100) if toxicity < 0.6 else 40 - (toxicity * 100)
                    print(rating[str(message.chat.id)])
                    print(message.chat.id)
                    rating[str(message.chat.id)] += toxicity_score
                    print(rating)
                except LangDetectException:
                    pass
            else:
                client.send_message(message.chat.id, 'Вы не начали диалог!')


@client.message_handler(content_types=['sticker'])
def bot_stickers(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info is not False:
            client.send_sticker(chat_info[1], message.sticker.file_id)
        else:
            client.send_message(message.chat.id, 'Вы не начали диалог!')


@client.message_handler(content_types=['voice'])
def bot_voice(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info is not False:
            client.send_voice(chat_info[1], message.voice.file_id)
        else:
            client.send_message(message.chat.id, 'Вы не начали диалог!')


@client.message_handler(content_types=['document'])
def bot_document(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info is not False:
            client.send_document(chat_info[1], message.document.file_id)
        else:
            client.send_message(message.chat.id, 'Вы не начали диалог!')


@client.message_handler(content_types=['video'])
def bot_video(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info is not False:
            client.send_video(chat_info[1], message.video.file_id)
        else:
            client.send_message(message.chat.id, 'Вы не начали диалог!')


@client.message_handler(content_types=['photo'])
def bot_photo(message):
    with lock:
        if message.chat.type == 'private':
            chat_info = db.get_active_chat(message.chat.id)
            if chat_info is not False:
                print(message.photo[0])
                client.send_photo(chat_info[1], message.photo[0].file_id)
            else:
                client.send_message(message.chat.id, 'Вы не начали диалог!')


client.polling(non_stop=True, interval=0)
