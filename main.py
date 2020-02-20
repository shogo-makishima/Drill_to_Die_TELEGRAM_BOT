import os, telebot, logging
from flask import Flask, request
from Classes.Main import Main, Bot

Main.Start(Main)

TOKEN = '1006756726:AAEjnh_9yROdhIss825lDjrizRXC1B7th6I'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


@bot.message_handler(commands=['materials'])
def start_message(message):
    Bot.isChosenMaterial = True
    bot.send_message(message.chat.id, f"Materials:\n{Main.GetItemsString(Main)}\n\nChoose the material and write them name in message.")


@bot.message_handler(content_types=['text'])
def main(message):
    if (Bot.isChosenMaterial):
        item = Main.GetItem(Main, message.text)

        if (item is None):
            bot.send_message(message.chat.id, "Not found!")
            Bot.isChosenMaterial = False
            return

        bot.send_message(message.chat.id, f"{item.name}:\n{item.price}\n")
        bot.send_photo(message.chat.id, item.photo)
        Bot.isChosenMaterial = False


if ("HEROKU" in list(os.environ.keys())):
    logger = telebot.logger
    telebot.logger.setLevel(logging.INFO)

    bot.remove_webhook()
    bot.set_webhook(url="https://drill-to-die-bot.herokuapp.com/bot")  # этот url нужно заменить на url вашего Хероку приложения

    server = Flask(__name__)

    @server.route("/bot", methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200

    server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))
else:
    bot.remove_webhook()
    bot.polling(none_stop=True)