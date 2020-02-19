import telebot

bot = telebot.TeleBot('1006756726:AAEjnh_9yROdhIss825lDjrizRXC1B7th6I')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')


bot.polling()
