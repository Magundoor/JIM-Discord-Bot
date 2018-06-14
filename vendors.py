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

vendor_shops_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'lootbox\\vendor_shops')
lootbox_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'lootbox')
vendors = TinyDB(os.path.join(lootbox_path, 'vendors.json'))

stores = vendors.all()

#for shop in stores:
#    store_items = TinyDB(os.path.join(vendor_shops_path,'{}.json'.format(shop['shop_file'])))
#    print('\n')
#    print(shop['name'])
#    print(shop['discription'])
#    for item in store_items:
#        print(item['name'])

while True:
    #store_items = TinyDB(os.path.join(vendor_shops_path,'{}.json'.format(shop['shop_file'])))
    Look = Query()
    stores = vendors.all()

    space = convert(input('\n-Enter command: '))

    if space == "buy":
        for shop in stores:
            print("\n",shop['name'])
            print(shop['discription'])
        store_buy = convert(input('\n-what store would you like to buy from?: '))
        current_store = ""
        found = False
        for shop in stores:
            if convert(shop['name']) == convert(store_buy):
                found = True
                # Do something
                current_store = shop['shop_file']
                break
        if found == False:
            print('\n-No store found called',store_buy)
        else:
            store_items = TinyDB(os.path.join(vendor_shops_path,'{}.json'.format(current_store)))
            print("\n-This store sells:\n")
            for item in store_items:
                print(item['name'])
            buy = convert(input('\n-what would you like to buy?: '))
            found = False
            for item in store_items:
                if convert(item['name']) == convert(buy):
                    found = True
                    # Do something
                    
                    addItemToInventory("MagunDongle",item)
                    print("\nyou bought: {} for {} credits".format(item['name'],item['value']))
                    break
            if found == False:
                print("\n-this store doesn't sell an item called",buy)

    elif space == "help":
        print('buy- buy an item from a shop')

    else:
        print(' ')
        print("error")
        print(' ')
