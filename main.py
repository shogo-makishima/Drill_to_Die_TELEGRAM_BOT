import os, telebot, logging, sys
from flask import Flask, request
from Classes.Main import Main, Bot

Main.Start(Main)

TOKEN = os.environ.get('TOKEN')

if (not TOKEN): sys.exit()

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['references'])
def start(message):
    bot.reply_to(message, "VK: https://vk.com/2point_games\n")
    bot.reply_to(message, "GameJolt: https://gamejolt.com/games/drilltodie/469250\n")


@bot.message_handler(commands=['materials'])
def start_message(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for i in Main.items.keys():
        key = telebot.types.InlineKeyboardButton(text=i, callback_data=f"i_{i}")
        keyboard.add(key)
    bot.send_message(message.chat.id, f"Choose the material:", reply_markup=keyboard)

@bot.message_handler(commands=['ships'])
def start_message(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for i in Main.ships.keys():
        key = telebot.types.InlineKeyboardButton(text=i, callback_data=f"s_{i}")
        keyboard.add(key)
    bot.send_message(message.chat.id, f"Choose the ships:", reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def main(message):
    pass

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    data, prefix = call.data[2:], call.data[:2]
    print(f"Data = {data}; Prefix = {prefix};")
    if (call.data in Main.items.keys() and prefix == "i"):
        item = Main.GetItem(Main, call.data)
        try: photo = open(f'/app/Images/{item.name}.png', 'rb')
        except: photo = open(f'/app/Images/Unknown.png', 'rb')
        bot.send_photo(call.message.chat.id, photo, caption=f"{item.name}:\nDescription: {item.description}\n\nPrice: {item.price};\n")
        Bot.isChosenMaterial = False
    if (call.data in Main.ships.keys() and prefix == "s"):
        ship = Main.GetShip(Main, call.data)
        photo = open(f'/app/Images/Unknown.png', 'rb')
        try: photo = open(f'/app/Images/{ship.name}.png', 'rb')
        except: pass
        try:
            bot.send_photo(call.message.chat.id, photo=photo)
            bot.send_message(call.message.chat.id, f"{ship.name}:\nDescription: {ship.description}\n\n\nUpgrades: \n{Main.GetUpgradesString(Main, ship)}\n")
        except: bot.send_message(call.message.chat.id, f"{ship.name}:\nDescription: {ship.description}\n\n\nUpgrades: \n{Main.GetUpgradesString(Main, ship)}\n")
        Bot.isChosenShip = False


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