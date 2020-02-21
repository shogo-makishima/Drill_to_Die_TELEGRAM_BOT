import os, telebot, logging, sys
from flask import Flask, request
from Classes.Main import Main, Bot

Main.Start(Main)

TOKEN = os.environ.get('TOKEN')

if (not TOKEN): sys.exit()

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['references'])
def start(message):
    bot.reply_to(message, "VK: https://vk.com/2point_games\nGameJolt: https://gamejolt.com/games/drilltodie/469250\n")


@bot.message_handler(commands=['materials'])
def start_message(message):
    Bot.isChosenMaterial = True
    Bot.isChosenShip = False
    bot.send_message(message.chat.id, f"Materials:\n{Main.GetItemsString(Main)}\n\nChoose the material and write them name in message.")

@bot.message_handler(commands=['ships'])
def start_message(message):
    Bot.isChosenMaterial = False
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

        try: photo = open(f'/app/Images/{item.name}.png', 'rb')
        except: photo = open(f'/app/Images/Unknown.png', 'rb')
        bot.send_photo(message.chat.id, photo, caption=f"{item.name}:\nDescription: {item.description}\n\nPrice: {item.price};\n")

        Bot.isChosenMaterial = False
    elif (Bot.isChosenShip):
        ship = Main.GetShip(Main, message.text)

        if (ship is None):
            bot.send_message(message.chat.id, "Not found!")
            Bot.isChosenMaterial = False
            return
        
        photo = open(f'/app/Images/Unknown.png', 'rb')
        try: photo = open(f'/app/Images/{ship.name}.png', 'rb')
        except: pass

        try:
            bot.send_photo(message.chat.id, photo=photo)
            bot.send_message(message.chat.id, f"{ship.name}:\nDescription: {ship.description}\n\n\nUpgrades: \n{Main.GetUpgradesString(Main, ship)}\n")
        except: bot.send_message(message.chat.id, f"{ship.name}:\nDescription: {ship.description}\n\n\nUpgrades: \n{Main.GetUpgradesString(Main, ship)}\n")

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