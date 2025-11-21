import telebot
from telebot import types
import webbrowser

bot = telebot.TeleBot("8502245941:AAGTrvMkI0BEkVZWgARKYayfi9-hDQQZkkY")

user_data = "Данных нет"


# Информирующие сообщение
@bot.message_handler(commands=["start"])
def start_msg(message):
    bot.send_message(
        message.chat.id,
        f"Привет, {message.from_user.first_name}! Я - ваш личный бот для записи на консалтинговую услугу.Используйте команды или меню для навигации",
    )
    main(message) 


def process_user_data(message):
    global user_data  # Теперь изменения в переменной в функции меняют глобальную переменную
    user_data = message.text # сохраняем запись
    bot.send_message(message.chat.id, f"Запись сохранена: '{user_data}' ")
    main(message)


# Основа, в виде меню
@bot.message_handler()
def main(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("Записаться на услугу", callback_data="sign up")
    )
    markup.add(types.InlineKeyboardButton("Ваша запись", callback_data="list"))
    markup.add(types.InlineKeyboardButton("Изменить запись", callback_data="edit"))
    markup.add(types.InlineKeyboardButton("Дашборд", callback_data="dashboard"))
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_msg(callback):
    global user_data
    if callback.data == "sign up":  # функционал кнопки "Записаться на услугу"
        msg = bot.send_message(
            callback.message.chat.id, "Введите тему и контактные данные"
        )
        bot.register_next_step_handler(msg, process_user_data)

    elif callback.data == "list":    # функционал кнопки "Ваша запись"
        bot.send_message(callback.message.chat.id, f"Запись: {user_data}")
        main(callback.message)

    elif callback.data == "edit":    # функционал кнопки "Изменить запись"
        markup1 = types.InlineKeyboardMarkup()
        button_edeting = types.InlineKeyboardButton(
            "Редактировать", callback_data="editing"
        )
        button_removing = types.InlineKeyboardButton(
            "Удалить", callback_data="removing"
        )
        markup1.add(button_edeting)
        markup1.add(button_removing)
        bot.send_message(
            callback.message.chat.id, "Выберите действие", reply_markup=markup1
        )

    elif callback.data == "dashboard":    # функционал кнопки "Дашборд"
        bot.send_message(callback.message.chat.id, "Открывается сайт, подождите...")
        webbrowser.open("http://127.0.0.1:8050/")

    elif callback.data == "editing":
        if user_data != "Данных нет":
            edit_msg = bot.send_message(
                callback.message.chat.id, "Введите измененную тему и контактные данные"
            )
            bot.register_next_step_handler(edit_msg, process_user_data)
        else:
            bot.send_message(
                callback.message.chat.id, "Записи для изменеия нет (_*o*)_"
            )

    elif callback.data == "removing":
        markup2 = types.InlineKeyboardMarkup()
        button_yes = types.InlineKeyboardButton("да", callback_data="yes")
        button_no = types.InlineKeyboardButton("нет", callback_data="no")
        markup2.add(button_yes)
        markup2.add(button_no)
        bot.send_message(callback.message.chat.id, "Уверены?", reply_markup=markup2)

    elif callback.data == "yes":
        user_data = "Данных нет"
        bot.send_message(callback.message.chat.id, "Запись удалена")
        main(callback.message)

    elif callback.data == "no":
        main(callback.message)


bot.infinity_polling()
