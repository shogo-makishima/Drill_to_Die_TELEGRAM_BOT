import os, telebot
from Classes.Main import Main

Main.Start(Main)

TOKEN = '1006756726:AAEjnh_9yROdhIss825lDjrizRXC1B7th6I'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)

@bot.message_handler(commands=['materials'])
def start_message(message):
    bot.send_message(message.chat.id, Main.GetItemsString(Main))

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


bot.polling()

