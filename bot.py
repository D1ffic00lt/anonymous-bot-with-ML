import telebot
import threading
import pickle
import nltk
import json
import os

from datetime import datetime
from langdetect.lang_detect_exception import LangDetectException

from templates import *
from configure import *
from database import Database
from ModelLibrary.predict import GetToxicity

print("\n" + "Program started" + "\n")

nltk.download('punkt')
nltk.download('stopwords')
db = Database('db.db')
client = telebot.TeleBot(config['token'])
lock = threading.Lock()
rating = {}
last_dialogs = {}
db.restart()

with open("ModelLibrary/models/EnglishModel.bf", "rb") as EnglishModel, \
        open("ModelLibrary/models/RussianModel.bf", "rb") as RussianModel, \
        open("ModelLibrary/models/RussianVectorizer.bf", "rb") as RussianVectorizer, \
        open("ModelLibrary/models/EnglishVectorizer.bf", "rb") as EnglishVectorizer:
    models_ = [pickle.load(RussianModel), pickle.load(EnglishModel)]
    vectorizers_ = [pickle.load(RussianVectorizer), pickle.load(EnglishVectorizer)]

print("Bot connected")


@ignore_exceptions
@client.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Я парень'), types.KeyboardButton('Я девушка'))
    client.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! '
                                         f'Добро пожаловать в анонимный чат!'
                                         'Укажите ваш пол. 🤖', reply_markup=markup)


@ignore_exceptions
@client.message_handler(commands=["set_rating"])
def set_rating(message):
    if message.chat.id in [453169809, 1021375877]:  # админы > обычные люди
        if len(message.text.split()) == 2:
            db.set_rating(message.chat.id, int(message.text.split()[1]))
        else:
            chat_info = db.get_active_chat(message.chat.id)
            if chat_info is not False:
                db.set_rating(chat_info[1], int(message.text.split()[1]))


@ignore_exceptions
@client.message_handler(commands=['help'])
def __help(message):
    client.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! '
                                         f'Добро пожаловать в анонимный чат!'
                                         'Укажите ваш пол. 🤖', reply_markup=main_menu())


@ignore_exceptions
@client.message_handler(commands=['menu'])
def menu(message):
    client.send_message(message.chat.id, '···МЕНЮ···\n'
                                         'Ваш профиль (виден только Вам):\n'
                                         f'Имя: {message.from_user.first_name}\n'
                                         f'Пол: {db.get_gender(message.chat.id, True)}\n'
                                         f'Рейтинг: {db.get_rating(message.chat.id)[0]:.4f}\n'
                                         f'/help - помощь в использовании бота 🤖', reply_markup=next_dialog())


@ignore_exceptions
@client.message_handler(commands=['stop'])
def stop(message):
    chat_info = db.get_active_chat(message.chat.id)

    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.row(types.InlineKeyboardButton(text='💩Спам💩', callback_data='spam'),
                 types.InlineKeyboardButton(text='🤥Обман🤥', callback_data='deceit'))
    keyboard.row(types.InlineKeyboardButton(text='💸Продажа💸', callback_data='sale'),
                 types.InlineKeyboardButton(text='🔞18+🔞', callback_data='NSFW'))
    keyboard.row(types.InlineKeyboardButton(text='🔎Следующий собеседник🔎', callback_data='search'))

    if chat_info is not False:
        db.delete_chat(chat_info[0])

        client.send_message(chat_info[1], '🤖 Собеседник покинул чат\n\nВы можете оставить жалобу на вашего '
                                          'собеседника:',
                            reply_markup=keyboard)
        client.send_message(message.chat.id, '🤖 Вы вышли из чата\n\nВы можете оставить жалобу на вашего собеседника:',
                            reply_markup=keyboard)

        db.change_rating(message.chat.id, rating[str(message.chat.id)])
        db.change_rating(chat_info[1], rating[str(chat_info[1])])

        del rating[str(message.chat.id)]
        del rating[str(chat_info[1])]
    else:
        markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup2.add(types.KeyboardButton('Парень🙍‍♂'),
                    types.KeyboardButton('Девушка🙍‍♀'),
                    types.KeyboardButton('Поиск среди всех🎲'))
        client.send_message(message.chat.id, '⛔Вы не начали диалог! Нажмите /menu для начала общения! 🤖',
                            reply_markup=markup2)


@ignore_exceptions
@client.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if not db.is_register(message.chat.id) or message.text in ['Я парень', 'Я девушка']:
            if message.text == 'Я парень':
                if db.set_gender(message.chat.id, 'male'):
                    client.send_message(message.chat.id, 'Ваш пол успешно добавлен! 🤖', reply_markup=main_menu())
                else:
                    client.send_message(message.chat.id, 'Вы уже указали пол. Напишите админу: @dfilinov8\n'
                                                         'Чтобы вернуться напишите /menu 🤖')
            elif message.text == 'Я девушка':
                if db.set_gender(message.chat.id, 'female'):
                    client.send_message(message.chat.id, 'Ваш пол успешно добавлен!🤖', reply_markup=main_menu())
                else:
                    client.send_message(message.chat.id, 'Вы уже указали пол. Напишите админу: @dfilinov8\n'
                                                         'Чтобы вернуться напишите /menu🤖')
            else:
                client.send_message(message.chat.id, 'Вы не зарегистрировались! Напишите /start для регистрации!🤖')
        else:
            chat_info = db.get_active_chat(message.chat.id)
            if chat_info is False and message.text not in ['Сказать свой профиль']:
                if message.text == '🔎Поиск собеседника🔎' or message.text == '🔎Следующий собеседник🔎':
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    markup.add(types.KeyboardButton('Парень🙍‍♂'),
                               types.KeyboardButton('Девушка🙍‍♀'),
                               types.KeyboardButton('Поиск среди всех🎲'))

                    client.send_message(message.from_user.id, 'Кого искать? 🤖', reply_markup=markup)

                elif message.text == 'Остановить поиск':
                    db.delete_queue(message.chat.id)
                    client.send_message(message.chat.id, 'Поиск остановлен:\n'
                                                         '· Напишите /menu для выхода в меню\n'
                                                         '· Нажмите на кнопку "🔎Поиск собеседника🔎", чтобы найти '
                                                         'следующий '
                                                         'диалог🤖',
                                        reply_markup=main_menu())
                elif message.text == 'Меню':
                    client.send_message(message.chat.id, '🤖 ···МЕНЮ··· 🤖\n'
                                                         'Ваш профиль (виден только Вам):\n'
                                                         f'Имя: {message.from_user.first_name}\n'
                                                         f'Пол: {db.get_gender(message.chat.id, True)}\n'
                                                         f'Рейтинг: {db.get_rating(message.chat.id)[0]:.4f}\n'
                                                         f'/help - помощь в использовании бота 🤖',
                                        reply_markup=next_dialog())

                elif message.text == 'Парень🙍‍♂':
                    if db.get_rating(message.chat.id)[0] < 500:
                        client.send_message(message.chat.id, f"Ваш рейтинг меньше допустимого значения!\n"
                                                             f"Сейчас он составляет "
                                                             f"{db.get_rating(message.chat.id)[0]:.4f}!\n"
                                                             f"Каждый день, пока ваш рейтинг не превысит 500, "
                                                             f"Вам будет добавляться 200 рейтинга 🤖")
                    else:
                        user_info = db.get_gender_chat('male')
                        chat_two = user_info[0]
                        if db.create_chat(message.chat.id, chat_two) is False:
                            db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                            client.send_message(message.chat.id, '🔎Поиск собеседника🔎 🤖', reply_markup=stop_search())
                        else:
                            mess = 'Собеседник найден! Чтобы остановить диалог, напишите /stop 🤖'

                            client.send_message(message.chat.id, mess, reply_markup=stop_dialog())
                            client.send_message(chat_two, mess, reply_markup=stop_dialog())
                            rating[str(message.chat.id)] = 0
                            rating[str(chat_two)] = 0
                            last_dialogs[str(message.chat.id)] = str(chat_two)
                            last_dialogs[str(chat_two)] = str(message.chat.id)

                elif message.text == 'Девушка🙍‍♀':
                    if db.get_rating(message.chat.id)[0] < 500:
                        client.send_message(message.chat.id, f"Ваш рейтинг меньше допустимого значения!\n"
                                                             f"Сейчас он составляет "
                                                             f"{db.get_rating(message.chat.id)[0]:.4f}!\n"
                                                             f"Каждый день, пока ваш рейтинг не превысит 500, "
                                                             f"Вам будет добавляться 200 рейтинга 🤖")
                    else:
                        user_info = db.get_gender_chat('female')
                        chat_two = user_info[0]
                        if db.create_chat(message.chat.id, chat_two) is False:
                            db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                            client.send_message(message.chat.id, '🔎Поиск собеседника🔎 🤖', reply_markup=stop_search())
                        else:
                            mess = 'Собеседник найден! Чтобы остановить диалог, напишите /stop 🤖'

                            client.send_message(message.chat.id, mess, reply_markup=stop_dialog())
                            client.send_message(chat_two, mess, reply_markup=stop_dialog())
                            rating[str(message.chat.id)] = 0
                            rating[str(chat_two)] = 0
                            last_dialogs[str(message.chat.id)] = str(chat_two)
                            last_dialogs[str(chat_two)] = str(message.chat.id)

                elif message.text == 'Поиск среди всех🎲':
                    if db.get_rating(message.chat.id)[0] < 500:
                        client.send_message(message.chat.id, f"Ваш рейтинг меньше допустимого значения!\n"
                                                             f"Сейчас он составляет "
                                                             f"{db.get_rating(message.chat.id)[0]:.4f}!\n"
                                                             f"Каждый день, пока ваш рейтинг не превысит 500, "
                                                             f"Вам будет добавляться 200 рейтинга.🤖")
                    else:
                        user_info = db.get_chat()
                        chat_two = user_info[0]
                        if db.create_chat(message.chat.id, chat_two) is False:
                            db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                            client.send_message(message.chat.id, '🔎Поиск собеседника🔎🤖', reply_markup=stop_search())
                        else:
                            mess = 'Собеседник найден! Чтобы остановить диалог, напишите /stop'

                            client.send_message(message.chat.id, mess, reply_markup=stop_dialog())
                            client.send_message(chat_two, mess, reply_markup=stop_dialog())
                            rating[str(message.chat.id)] = 0
                            rating[str(chat_two)] = 0
                            last_dialogs[str(message.chat.id)] = str(chat_two)
                            last_dialogs[str(chat_two)] = str(message.chat.id)
            else:
                if message.text == 'Сказать свой профиль':
                    chat_info = db.get_active_chat(message.chat.id)
                    if message.from_user.username and chat_info is not False:
                        client.send_message(chat_info[1], '@' + message.from_user.username)
                        client.send_message(message.chat.id, 'Вы сказали свой профиль',
                                            reply_markup=stop_dialog_when_say())
                    else:
                        client.send_message(message.chat.id, 'В вашем аккаунте не указан username')
                else:
                    if "🤖" in message.text or message.chat.id in []:  # админы > обычные люди
                        client.send_message(message.chat.id, "Вы не можете использовать \"🤖\" в своих сообщениях!")
                    else:
                        if chat_info is not False:
                            chat_info = db.get_active_chat(message.chat.id)
                            client.send_message(chat_info[1], message.text)
                            try:
                                toxicity = GetToxicity(message.text, models=models_, vectorizers=vectorizers_)[1]
                                toxicity_score = 70 - (toxicity * 100) if toxicity < 0.6 else 40 - (toxicity * 100)
                                rating[str(message.chat.id)] += toxicity_score
                            except LangDetectException:
                                pass
                            except KeyError:
                                pass

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
            db.add_rating()
            with open('last_save.json', 'w+') as outfile:
                json.dump({
                    "day": day,
                    "month": month,
                }, outfile)


@ignore_exceptions
@client.message_handler(content_types=['sticker'])
def bot_stickers(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info is not False:
            client.send_sticker(chat_info[1], message.sticker.file_id)
        else:
            client.send_message(message.chat.id, '⛔Вы не начали диалог! Нажмите /menu для начала общения! 🤖')


@ignore_exceptions
@client.message_handler(content_types=['voice'])
def bot_voice(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info is not False:
            client.send_voice(chat_info[1], message.voice.file_id)
        else:
            client.send_message(message.chat.id, '⛔Вы не начали диалог! Нажмите /menu для начала общения! 🤖')


@ignore_exceptions
@client.message_handler(content_types=['document'])
def bot_document(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info is not False:
            client.send_document(chat_info[1], message.document.file_id)
        else:
            client.send_message(message.chat.id, '⛔Вы не начали диалог! Нажмите /menu для начала общения! 🤖')


@ignore_exceptions
@client.message_handler(content_types=['video'])
def bot_video(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info is not False:
            client.send_video(chat_info[1], message.video.file_id)
        else:
            client.send_message(message.chat.id, '⛔Вы не начали диалог! Нажмите /menu для начала общения! 🤖')


@ignore_exceptions
@client.message_handler(content_types=['photo'])
def bot_photo(message):
    with lock:
        if message.chat.type == 'private':
            chat_info = db.get_active_chat(message.chat.id)
            if chat_info is not False:
                client.send_photo(chat_info[1], message.photo[0].file_id)
                print(message)
            else:
                client.send_message(message.chat.id, '⛔Вы не начали диалог! Нажмите /menu для начала общения! 🤖')


@ignore_exceptions
@client.message_handler(content_types=['video_note'])
def bot_video_note(message):
    with lock:
        if message.chat.type == 'private':
            chat_info = db.get_active_chat(message.chat.id)
            if chat_info is not False:
                client.send_video_note(chat_info[1], message.video_note.file_id)
            else:
                client.send_message(message.chat.id, '⛔Вы не начали диалог! Нажмите /menu для начала общения! 🤖')


@ignore_exceptions
@client.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data != "search":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='Поиск собеседника', callback_data='search'))
        client.edit_message_text(chat_id=call.from_user.id, message_id=call.message.id, text="Жалоба отправлена",
                                 reply_markup=markup)
        db.add_report(call.data, int(last_dialogs[str(call.from_user.id)]))
    else:
        markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup2.add(types.KeyboardButton('Парень🙍‍♂'), types.KeyboardButton('Девушка🙍‍♀'),
                    types.KeyboardButton('Поиск среди всех🎲'))

        client.send_message(call.from_user.id, 'Кого искать? 🤖', reply_markup=markup2)
    client.answer_callback_query(callback_query_id=call.id)


if __name__ == "__main__":
    client.polling(non_stop=True, interval=0, skip_pending=True)
