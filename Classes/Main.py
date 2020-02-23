import json, os, math

class Bot:
    isChosenMaterial = False
    isChosenShip = False


class Main:
    data = {}
    items = {}
    ships = {}

    def Start(self):
        print(os.getcwd())

        with open("/app/Files/data.json") as file:
            self.data = json.load(file)

        self.items = self.__ParseItems(self)
        self.ships = self.__ParseShips(self)

    def __ParseItems(self):
        items = {}

        for item in self.data["items"]:
            items[item["name"]] = Item(item["name"], item["price"], item["destription"])

        return items

    def __ParseShips(self):
        ships = {}

        for ship in self.data["ships"]:
            upgrades = self.__ParseUpgrades(self, ship["upgrades"])
            ships[ship["name"]] = Ship(ship["name"], upgrades, ship["description"])

        return ships

    def __ParseUpgrades(self, shipData):
        upgrades = []
        for upgrade in shipData:
            upgrades.append(Upgrade(upgrade["name"], self.__ParseLevelUpgrades(self, upgrade["levelUpgrades"])))

        return upgrades

    def __ParseLevelUpgrades(self, levelData):
        levels = []

        for level in levelData:
            levels.append(LevelUpgrade(level["level"], level["price"], level["variable"]))

        return levels

    def GetItemsString(self):
        string = ""

        newlist = list()
        for i in self.items.keys():
            newlist.append(i)

        for i in newlist:
            string += f"    {i};\n" if (i != newlist[-1]) else f"    {i};"

        return string

    def GetShipsString(self):
        string = ""

        newlist = list()
        for i in self.ships.keys():
            newlist.append(i)

        for i in newlist:
            string += f"    {i};\n" if (i != newlist[-1]) else f"    {i};"

        return string

    def GetUpgradesString(self, ship):
        string = ""

        newlist = list()
        for i in ship.upgrades:
            newlist.append(i)

        for i in newlist:
            string += f"  {i.name}:\n"
            for j in i.levelUpgrades:
                string += f"    {j.level}:\n      Price = {j.price};\n      Variable = {round(j.variable, 1)};\n"

        return string

    def GetItem(self, name):
        item = None
        if (self.items.get(name)):
            item = self.items[name]
        return item

    def GetShip(self, name):
        return self.ships[name]

    def GetUpgrade(self, name, nameShip):
        upgrade = None

        for i in self.GetShip(self, nameShip).upgrades:
            if (i.name == name):
                upgrade = i
                break

        return upgrade



class Item:
    def __init__(self, getName, getPrice, getDescription):
        self.name = getName
        self.price = getPrice
        self.description = getDescription



class Ship:
    def __init__(self, getName, getUpgardes, getDescription):
        self.name = getName
        self.upgrades = getUpgardes
        self.description = getDescription

class Upgrade:
    def __init__(self, getName, getLevelsUpgades):
        self.name = getName
        self.levelUpgrades = getLevelsUpgades

class LevelUpgrade:
    def __init__(self, getLevel, getPrice, getVariabel):
        self.level = getLevel
        self.price = getPrice
        self.variable = getVariabel


