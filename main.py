import telebot
from telebot import types

bot = telebot.TeleBot("8502245941:AAGTrvMkI0BEkVZWgARKYayfi9-hDQQZkkY")

user_data = "Данных нет"
# Информирующие сообщение
@bot.message_handler(commands=['start'])
def start_msg(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Я - ваш личный бот для записи на консалтинговую услугу. Используйте команды или меню для навигации')

# Основа, в виде меню
@bot.message_handler(commands=['help'])
def main(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Записаться на услугу', callback_data='sign up'))
    markup.add(types.InlineKeyboardButton('Ваша запись', callback_data='list'))
    markup.add(types.InlineKeyboardButton('Изменить запись', callback_data='edit'))
    markup.add(types.InlineKeyboardButton('Дашборд', callback_data='dashboard'))
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_msg(callback):
    if callback.data == 'sign up':
        msg = bot.send_message(callback.message.chat.id, 'Введите тему и контактные данные')
        bot.register_next_step_handler(msg, process_user_data)
    elif callback.data == 'list':
        bot.send_message(callback.message.chat.id, f'Запись: {user_data}')
    elif callback.data == 'edit':
        markup1 = types.InlineKeyboardMarkup()
        markup1.add(types.InlineKeyboardButton('Редактировать', callback_data='editing'))
        markup1.add(types.InlineKeyboardButton('Удалить', callback_data='removing'))
        bot.send_message(callback.message.chat.id, 'Выберите действие', reply_markup=markup1)

def on_click(callback):
    if callback.message.text == 'editing':
        bot.send_message(callback.message.chat.id, 'ffff')


#@bot.callback_query_handler(func=lambda callback: callback.data == 'editing')
#def callback_edit_msg(callback):
 #   if user_data != "Данных нет":
  #      msg = bot.send_message(callback.message.chat.id, 'Введите измененную тему и контактные данные')
   #     bot.register_next_step_handler(msg, process_user_data)
   # else: bot.send_message(callback.message.chat.id, 'Записи для изменеия нет (_*o*)_')



def process_user_data(message):
    global user_data # Теперь изменения в переменной в функции меняют глобальную переменную
    user_data = message.text
    bot.send_message(message.chat.id, f"Запись сохранена: '{user_data}' ")

bot.infinity_polling()