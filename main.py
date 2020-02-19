import telebot
from Classes.Main import Main

bot = telebot.TeleBot('1006756726:AAEjnh_9yROdhIss825lDjrizRXC1B7th6I')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')


@bot.message_handler(content_types=['text'])
def send_text(message):
    if (message.text == 'Привет'):
        bot.send_message(message.chat.id, "Привет")
    elif (message.text == 'Пока'):
        bot.send_message(message.chat.id, 'Прощай')
    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю')


bot.polling()
