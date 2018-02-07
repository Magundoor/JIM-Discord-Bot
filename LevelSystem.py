import asyncio
import os
import tinydb
import math
import logging
import urllib.request, json
from time import sleep
from random import *
from tinydb import TinyDB, Query
from tinydb.operations import delete,increment

#logging.basicConfig(filename='Leveling.log',level=logging.DEBUG)

lootbox_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'lootbox')

db = TinyDB(os.path.join(lootbox_path, 'person.json'))
Users = Query()

## Sets the test user for database testing.
TestName = 'Alynzos'
lootboxPerLevel = 10

## Defines User atributes.
char = {
    'name' : 'MagunDongle',
    'lvl' : 1,
    'xp' : 0,
    'lvlNext' : 25,
    'stats' : {'str' : 1,
               'dex' : 1,
               'int' : 1},
    'lootboxCount' : 0,
    'needsLevelup' : 0,
    'plvl' : 0
    }

## Levels up User and sets the xp for other atributes.
def level(User):
    user = db.search(Users.name == User)
    nStr, nDex, nInt = 0, 0, 0
    while user[0]['xp'] >= user[0]['lvlNext']:

        #! Don't forget to set up a way to only update one person at a time #! Already fixed this LOL ECKS DEE
        db.update({'needsLevelup' : True}, Users.name == TestName)

        plvl = user[0]['lvl']
        plvl += 1
        db.update({'lvl' : plvl}, Users.name == TestName)

        pXp = user[0]['xp']
        pXp = user[0]['xp'] - user[0]['lvlNext']
        db.update({'xp' : pXp}, Users.name == TestName)

        plvlNext = user[0]['lvlNext']
        plvlNext = round(user[0]['lvlNext'] * 1.5)
        db.update({'lvlNext': plvlNext}, Users.name == TestName)

        nStr += 1
        nDex += 1
        nInt += 1
        break

    pStr = char['stats']['str']
    pDex = char['stats']['dex']
    pInt = char['stats']['int']

    pStr += nStr
    pDex += nDex
    pInt += nInt

## Adds Lootbox's to user based on lootboxPerLevel, also compensates for multiple levelups.
def levelUp(User):
    user = db.search(Users.name == User)
    if user[0]['lvl'] > user[0]['plvl']+1:
        lootboxes = user[0]['lootboxCount']
        lootboxes += (user[0]['lvl'] - user[0]['plvl'])*lootboxPerLevel
        db.update({'lootboxCount' : lootboxes}, Users.name == TestName)

        print('Congrats {} you have leveled up! {} lootboxes have been added to your inventory'.format(user[0]['name'],(user[0]['lvl'] - user[0]['plvl'])*lootboxPerLevel))
    else:
        lootboxes = user[0]['lootboxCount']
        lootboxes += lootboxPerLevel
        db.update({'lootboxCount' : lootboxes}, Users.name == TestName)

        print('Congrats {} you have leveled up! {} lootboxes have been added to your inventory'.format(user[0]['name'],lootboxPerLevel))
    
    nlev = user[0]['lvl']
    db.update({'plvl' : nlev}, Users.name == TestName)

    print('Level: {}'.format(user[0]['lvl']))
    print('You have gained a total of {} XP'.format(round(user[0]['lvlNext'] * 1.5)))
    print('Lootboxes in inventory: ',user[0]['lootboxCount'])
    print('You should have {} loot boxes for your level'.format(user[0]['lvl']*10))
    print(' ')

## Checks all users in db if they require a level up
def check_levelup():
    for u in db:
        TestName = u[0]['name']
        user = db.search(Users.name == TestName)
        if user[0]['needsLevelup'] == True:
            levelUp(TestName)
            db.update({'needsLevelup' : False}, Users.name == TestName)

## Adds levels for testing.
while False :
    user = db.search(Users.name == TestName)
    sleep(0.5)
    addedXp = randint(10,500)

    exp = user[0]['xp']
    exp += addedXp
    db.update({'xp' : exp}, Users.name == TestName)

    if user[0]['needsLevelup'] == True:
        levelUp(TestName)
        db.update({'needsLevelup' : False}, Users.name == TestName)
    if user[0]['lvl'] == 10:
        user[0]['xp'] += 40000
    level(TestName)
