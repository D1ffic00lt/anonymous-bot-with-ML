from telebot import types


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('🔎Поиск собеседника🔎'))
    return markup


def stop_dialog():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Сказать свой профиль'),
               types.KeyboardButton('/stop'))
    return markup


def stop_dialog_when_say():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('/stop'))
    return markup


def next_dialog():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('🔎Следующий собеседник🔎'))
    return markup


def stop_search():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Остановить поиск'))
    return markup


def ignore_exceptions(func):
    def temp(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)

    return temp
