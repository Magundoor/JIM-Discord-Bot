import asyncio
import os
import tinydb
import math
import time
import logging
import urllib.request, json
from LootBox_Core import *
from LevelSystem import *
from random import *
from time import sleep
from tinydb import TinyDB, Query
from tinydb.operations import delete,increment

lootboxes_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'lootbox\lootbox_Items')
lootbox_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'lootbox')

LootBoxes = TinyDB(os.path.join(lootbox_path, 'LootBoxes.json'))

Items = LootBoxes.all()


def check_items(x):
    ItemPool = TinyDB(os.path.join(lootboxes_path,'{}.json'.format(x['itemPool'])))
    Items = ItemPool.all()
    item_count_key = 1
    print('checking items in', x['name'])
    for i in Items:
        if i['itemKey'] != item_count_key:
            print(" {} has bad key needs to be {} was {}".format(i['name'],count_key,i['itemKey']))
        else:
            print(" {} is good".format(i['name']))
        item_count_key += 1
        if i['lootboxKey'] != x['key']:
                 print(" {} has bad lootbox key needs to be {} was {}".format(i['name'],x['key'],i['lootboxKey']))
    print("---done with {}---\n".format(x['name']))
	
print("Running key_checker on lootboxes:")
print(" ")
LBS = LootBoxes.all()
count_key = 1
for x in LBS:
    if x['key'] != count_key:
        print('---checking {}---'.format(x['name']))
        print(" {} has bad key needs to be {} was {}\n".format(x['name'],count_key,x['key']))
        check_items(x)
    else:
        print('---checking {}---'.format(x['name']))
        print(" {} is good\n".format(x['name']))
        check_items(x)
    count_key += 1
x = input('Press Enter to exit ')
