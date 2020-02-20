import os, telebot, logging
from flask import Flask, request
from Classes.Main import Main, Bot

Main.Start(Main)

# print(Main.GetUpgradesString(Main, "Betty"))

TOKEN = '1006756726:AAEjnh_9yROdhIss825lDjrizRXC1B7th6I'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


@bot.message_handler(commands=['materials'])
def start_message(message):
    Bot.isChosenMaterial = True
    bot.send_message(message.chat.id, f"Materials:\n{Main.GetItemsString(Main)}\n\nChoose the material and write them name in message.")

@bot.message_handler(commands=['ships'])
def start_message(message):
    Bot.isChosenShip = True
    bot.send_message(message.chat.id, f"Ships:\n{Main.GetShipsString(Main)}\n\nChoose the ship and write them name in message.")


@bot.message_handler(content_types=['text'])
def main(message):
    if (Bot.isChosenMaterial):
        item = Main.GetItem(Main, message.text)

        if (item is None):
            bot.send_message(message.chat.id, "Not found!")
            Bot.isChosenMaterial = False
            return

        try:
            photo = open(f'/app/Images/{item.name}.jpg', 'rb')
        except:
            photo = open(f'/app/Images/Unknown.png', 'rb')
        bot.send_photo(message.chat.id, photo, caption=f"{item.name}:\nPrice: {item.price};\n")

        Bot.isChosenMaterial = False
    elif (Bot.isChosenShip):
        ship = Main.GetShip(Main, message.text)

        if (ship is None):
            bot.send_message(message.chat.id, "Not found!")
            Bot.isChosenMaterial = False
            return

        photo = open(f'/app/Images/Unknown.png', 'rb')
        try: photo = open(f'/app/Images/{ship.name}.jpg', 'rb')
        except: pass

        print(f"{ship.name}:\nUpgrades: \n{Main.GetUpgradesString(Main, ship)}\n")
        bot.send_photo(message.chat.id, photo=photo, caption=f"{ship.name}:\nUpgrades: \n{Main.GetUpgradesString(Main, ship)}\n")

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
