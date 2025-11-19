import telebot

bot = telebot.TeleBot('8502245941:AAGyezJe6PSOS1wYqlFulX7s_c2D0cy8Sx0')

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, message.from_user.first_name)


bot.infinity_polling()