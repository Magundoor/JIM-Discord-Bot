import os
import bisect
import tinydb
import math
import logging
import urllib.request, json 
from LevelSystem import level, levelUp
from time import sleep
from random import *
from tinydb import TinyDB, Query
from tinydb.operations import delete,increment

#logging.basicConfig(filename='Leveling.log',level=logging.DEBUG)

lootboxes_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'lootbox\lootbox_Items')
lootbox_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'lootbox')

LootBoxes = TinyDB(os.path.join(lootbox_path, 'LootBoxes.json'))
db = TinyDB(os.path.join(lootbox_path, 'person.json'))

#LootBoxes = TinyDB('LootBoxes.json')
#db = TinyDB('person.json')

Search = Query()

# Base item rarity scale.
Raritys = {
    "Junk" : "Grey, 100",
    "Very Common" : "White, 90",
    "Common" : "Green, 80",
    "Uncommon" : "Pink, 70",
    "Rare" : "Blue, 60",
    "Very Rare" : "Yellow, 50",
    "Epic" : "Orange, 40",
    "Mythical" : "Purple, 30",
    "Legendary" : "Rainbow, 20",
    "Special" : "White, 10",
    }

# Gather's information from Json item database and splits it into items to use later.
def randLootBox():
    LB = LootBoxes.get(doc_id=randint(1,len(LootBoxes)))
    ItemPool = TinyDB(os.path.join(lootboxes_path, '{}.json'.format(LB['itemPool'])))

    Items = ItemPool.all()

    print('Name :',LB['name'])
    print('Rarity: ', LB['rarity'])
    print('Discription: ', LB['discription'])
    print('IconFile: ',LB['icon'])
    print("Items Placeholder")
    print('---------')

# Chooses an item from a list using provided weights.
class WeightedChoice(object):
    def __init__(self, weights):
        self.totals = []
        self.weights = weights
        running_total = 0

        for w in weights:
            running_total += w[1]
            self.totals.append(running_total)

    def next(self):
        rnd = randint(0, self.totals[-1])
        i = bisect.bisect_right(self.totals, rnd)
        return self.weights[i][0]

# Grabs an item based on it's doc_id from the appropriate database/lootbox.
def GetItemInfo(Item,lootbox):
    Box = LootBoxes.get(doc_id=lootbox)
    ItemPool = TinyDB(os.path.join(lootboxes_path, '{}.json'.format(Box['itemPool'])))

    Item = ItemPool.get(doc_id=Item)

    # Color/Rarity picker.
    Rarity = Item['rarity']
    Color = GetRarity(Rarity)

    #print('Container: ',Box['name'])
    #print('Item Name: ',Item['name'])
    #print('Item Description: ',Item['discription'])
    #print('Item Rarity: ',Item['rarity'])
    #print('Rarity Class: ',Color)
    #print('-------------')

    obj = {"name": Item['name'],"discription": Item['discription'],"value": Item['value'],"rarity": Item['rarity'],"lootboxKey": Item['lootboxKey'],"itemKey": Item['itemKey']}
    return obj

# Grabs the information from an item using a lootbox doc_id
def GetRandItem(lootbox):
    Box = LootBoxes.get(doc_id=lootbox)
    ItemPool = TinyDB(os.path.join(lootboxes_path, '{}.json'.format(Box['itemPool'])))

    # Creates the item list to be used by the WeightedChoice algorithm.
    monsterlist = ()
    TempItem=[]
    for i in ItemPool:
        #print(i.doc_id)
        name = i.doc_id
        rare = i['rarity']
        obj = (name,int(rare))
        TempItem.insert(0,(obj))
    itemlist=TempItem

    # Set's which list to use for the WeightedChoice algorithm .
    weightedChoice = WeightedChoice(itemlist);

    Item = GetItemInfo(weightedChoice.next(), lootbox)
    return Item

# Grabs the info from a lootbox
def GetLootboxInfo(Item):
    Lootboxes = TinyDB(os.path.join(lootbox_path, 'LootBoxes.json'))
    Item = Lootboxes.get(doc_id=Item)

    # Color/Rarity picker.
    Rarity = Item['rarity']
    Color = GetRarity(Rarity)

    #print('Container: ',Item['name'])
    #print('Item Description: ',Item['discription'])
    #print('Item Rarity: ',Item['rarity'])
    #print('Rarity Class: ',Color)
    #print('-------------')

    obj = {"name": Item['name'],"rarity": Item['rarity'],"itemPool": Item['itemPool'],"discription": Item['discription'],"icon": Item['icon'],"key": Item['key']}
    return obj

# Grabs a lootbox based on it's doc_id from the appropriate database.
def GetRandLootbox():

    Lootboxes = TinyDB(os.path.join(lootbox_path, 'LootBoxes.json'))

    # Creates the item list to be used by the WeightedChoice algorithm.
    itemlist = ()
    TempItem=[]
    for i in Lootboxes:
        #print(i.doc_id)
        name = i.doc_id
        rare = i['rarity']
        obj = (name,int(rare))
        TempItem.insert(0,(obj))

    itemlist=TempItem
    # Set's which list to use for the WeightedChoice algorithm .
    weightedChoice = WeightedChoice(itemlist);

    Item = GetLootboxInfo(weightedChoice.next())
    return Item

# Returns the rarity values with an input
def GetRarity(Rarity):
    if Rarity == 100:
        Color = "Trash/Grey"
    elif Rarity == 90:
        Color = "Very/Common White"
    elif Rarity == 80:
        Color = "Common/Green"
    elif Rarity == 70:
        Color = "Uncommon/Pink"
    elif Rarity == 60:
        Color = "Rare/Blue"
    elif Rarity == 50:
        Color = "Very Rare/Yellow"
    elif Rarity == 40:
        Color = "Epic/Orange"
    elif Rarity == 30:
        Color = "Mythical/Purple"
    elif Rarity == 20:
        Color = "Legendary/Rainbow"
    elif Rarity == 10:
        Color = "Special/White"
    else:
        Color = "Nothing"
    return Color

# Converts content to usable strings 
def convert(string):
    nstring = string.lower().replace(" ", "")
    return nstring

# Grabs an items key from a users inventorty using the items name
def GetLootboxKey(User, Thing):
    user = db.search(Search.name == User)
    Item = convert(Thing)
    Inventory = user[0]['lootboxInventory']
    for i in Inventory:
        if Item == convert(i['name']):
            key = i['key']
            return key
        break

# Grabs a lootboxes key from a users inventory using the items name
def GetItemKey(User, Thing):
    user = db.search(Search.name == User)
    Item = convert(Thing)
    Inventory = user[0]['inventory']
    for i in Inventory:
        if Item == convert(i['name']):
            key = i['itemKey']
            return key
        break

# Deletes an item from the users inventory using a name
def deleteItemFromInventory(User, Thing):
    user = db.search(Search.name == User)
    Inventory = user[0]['inventory']
    print(Inventory)
    new_inventory = []
    #print("Before",Inventory)
    for i in Inventory:
        for x in range(0,1):
            if convert(i['name']) == convert(Thing):
                Inventory.remove(i)
                new_inventory = Inventory
                db.update({'inventory': new_inventory}, Search.name == User)
                #print("After",new_inventory)
            break

# Deletes an item from the users inventory using a name
def deleteFromLootBoxInventory(User, Thing):
    user = db.search(Search.name == User)
    Inventory = user[0]['lootboxInventory']
    new_inventory = []
    #print("Before",Inventory)
    for i in Inventory:
        for x in range(0,1):
            if convert(i['name']) == convert(Thing):
                Inventory.remove(i)
                new_inventory = Inventory
                db.update({'lootboxInventory': new_inventory}, Search.name == User)
                #print("After",new_inventory)
            break

# Adds an item to a users inventory
def addItemToInventory(User,Thing):
    user = db.search(Search.name == User)
    Inventory = user[0]['inventory']
    Item = Thing
    Inventory.append(Item)
    db.update({'inventory': Inventory}, Search.name == User)
  
# Adds lootbox to inventory
def addLootboxToInventory(User, Thing):
    # Goddamit, I lost some code from a crash, I had a much more elegant method of doing this before
    user = db.search(Search.name == User)
    Inventory = user[0]['lootboxInventory']
    Item = Thing
    Inventory.append(Item)
    db.update({'lootboxInventory': Inventory}, Search.name == User)