import discord, logging, json
import asyncio
import os
import math
import urllib.request
import itertools
import operator
import configparser
from game_grabber import *
from stawpoll_poll import *
from time import sleep
from random import *
from discord.ext import commands
from tinydb import TinyDB, Query
from tinydb.operations import delete,increment
# Requirements: discord.py, tinydb, strawpoll.py

# Define basic variables
description = '''JIM: MagunLabs A.I, Neural Code:062'''
bot = commands.Bot(command_prefix='?', description=description)
db = TinyDB('data.json')
Users = Query()

# Config loading information
config = configparser.ConfigParser()
config.read('JIM_Config.ini')
['JIM_Config.ini']
holoDeckId = config['holo-deck']['holodeckid']
holo_deck_enabled = config['holo-deck'].getboolean('holo_deck_enabled')
defHoloDeckName = config['holo-deck']['defholodeckname']
congif_roles = config['purge-roles']['custom_roles']
custom_roles = congif_roles.split(',')
apikey = config['config']['apikey']
smash_pass = config['config']['smash_pass_channel']
smash_time = config['config']['smash_time']

# Startup/Name lists
names = [
    "Your Mom",
    "Donald Trump",
    "Hillary Clinton",
    "Obama",
    "Katy Perry",
    "Justin Bieber",
    "Michael Phelps",
    "Edgar Allen Poe",
    "Kim Kardashian",
    "Taylor Swift",
    "Drake",
    "Eminem",
    "Santa Claus",
    "John Cena",
    "Hugh Mungus",
    "Hitler",
    "Jesus",
    "Kim Jong Un",
    "Oprah Winfrey",
    "Newt Gingrich",
    "Patrick Star",
    "Dwayne the Rock Johnson",
    "Kevin Spacey",
    "Harvey Weinstein",
    "Elijah Gilmore",
    "Jeff Kaplan",
    "Linus Sebastian",
    "Arnold",
    "Johntron",
    "Scar",
    "Jesse McCree",
    "Harambe",
    "Ugandan Knuckles",
    "Himself",
    ]
loading = [
    "Finding neural deposit location..",
    "Extracting previous neural state..",
    "Preforming nuke inventory count..",
    "Contacting french prime minister..",
    "Pinging MagunLabs-Satalites: OK..",
    "Checking spaghetti recipe database..",
    "Preparing Holo-Deck..",
    "Finding Memo: Located..",
    "Verifying personality module, current module: $MARTA$$..",
    "Checking social media like percentage..",
    "Logging into club penguin..",
    "ERROR: couldn't locate self confidence"
    ]
loadingState = True

# Startup text
print('---------------')
print("API Key loaded from config")
print('Starting A.I from Neural Code:062')
print('---------------')
print(' ')

async def load():
    global loadingState
    while loadingState == True:
        await asyncio.sleep(0.9)
        print(loading[randint(0,len(loading)-1)])
bot.loop.create_task(load())

# Setup basic logging for the bot
logging.basicConfig(level=logging.WARNING)

@bot.event
async def on_ready():
    global loadingState
    loadingState = False
    await asyncio.sleep(1.5)
    print(' ')
    print('Complete: A.I Neural Stability Confirmed.')
    print(' ')
    if holo_deck_enabled == True:
        print('Holo-Deck is Enabled')
        print(' ')
        print('Holo-Deck information loaded:        ID:{}      DEFAULT_NAME:{}'.format(holoDeckId,defHoloDeckName))
        print(' ')
    else:
        print('Holo-Deck is Disabled')
        print(' ')
    print('A.I Status: ONLINE')
    print(' ')
    
async def my_background_task():
    await bot.wait_until_ready()
    while not bot.is_closed:
        await bot.change_presence(game=discord.Game(name= "with {}".format(names[randint(0,len(names)-1)])))
        await asyncio.sleep(600) # task runs every 10 mins
bot.loop.create_task(my_background_task())

@bot.event
async def on_member_update(before, after):
    #Updates on state changes and checks games of people in the Holo Deck
    voice_channel = discord.utils.get(bot.get_all_channels(), id = holoDeckId)
    if holo_deck_enabled == True:
        if not voice_channel:
            return print("Tried to check users in voice but didn't have a valid voice ID")
        members = voice_channel.voice_members
        member_names = '\n'.join([x.name for x in members])
        if len(member_names) <= 0:
            await bot.edit_channel(voice_channel, name=defHoloDeckName)
        else:
            print('--------------------------------------------------')
            print('Someone updated their client, generating report:')
            print(' ')
            print('-TOTAL-IN-ROOM-')
            print (member_names)
            print('---------------')
            print(' ')
            gameTotals = []
            for x in members:
                game = x.game
                gameTotals.append("{}".format(game))
                print("Added {} to game list".format(game))
                print(' ')
            print("Game list: {}".format(gameTotals))
            if most_common(gameTotals) == "None":
                await bot.edit_channel(voice_channel, name=defHoloDeckName)
            else:
                await bot.edit_channel(voice_channel, name="{}".format(most_common(gameTotals)))
                print(' ')
                print("Majority of everyone is playing {}, changeing name to -{}-".format(most_common(gameTotals),most_common(gameTotals)))
                print('--------------------------------------------------')
                print(' ')

@bot.command(pass_context=True)
async def purge(context, number : int):
    # Prune also has self delete
    """Deletes a specified number of messages"""
    is_admin = False
    for role in context.message.author.roles:
        for x in custom_roles:
            if role.name == x:
                deleted = await bot.purge_from(context.message.channel, limit=number+1)
                msg = await bot.send_message(context.message.channel, 'Deleted {} message(s)'.format(len(deleted)-1))
                await asyncio.sleep(5)
                await bot.delete_message(msg)
                is_admin = True
    if is_admin == False:
        msg = await bot.send_message(context.message.channel, "Sorry {}, You don't have permission to use this command".format(context.message.author))
        await asyncio.sleep(5)
        await bot.delete_message(msg)

@bot.command(pass_context = True)
async def vcmembers(ctx, voice_channel_id):
    """Debugging command not intended for you"""
    #First getting the voice channel object
    voice_channel = discord.utils.get(ctx.message.server.channels, id = voice_channel_id)
    if not voice_channel:
        return await bot.say("That is not a valid voice channel.")

    members = voice_channel.voice_members
    member_names = '\n'.join([x.name for x in members])

    embed = discord.Embed(title = "{} member(s) in {}".format(len(members), voice_channel.name),
                          description = member_names,
                          color=discord.Color.blue())

    return await bot.say(embed = embed)

@bot.command(pass_context=True)
async def google(context, *, google: str):
    """Generates a google link for the lazy"""
    googled = google.replace(" ", "+").replace("/", "").replace("%", "")
    await bot.send_message(context.message.channel, 'Here is your google link: <http://lmgtfy.com/?q={}>'.format(googled))

@bot.command(pass_context=True)
async def update():
    """Update's who JIM is currently playing with"""
    await bot.change_presence(game=discord.Game(name= "with {}".format(names[randint(0,len(names)-1)])))

@bot.command(pass_context=True)
async def invite(context):
	"""Generates a invite code to the server for the user to share"""
	invite = await bot.create_invite(context.message.server,max_uses=1,xkcd=True)
	await bot.send_message(context.message.author,"Your invite URL is {}".format(invite.url))

@bot.command(pass_context=True)
async def gif(context, *, search: str):
    """Provides a gif from a search"""
    await bot.send_typing(context.message.channel)
    searched = search.replace(" ", "+").replace("/", "").replace("%", "")
    url = "http://api.giphy.com/v1/gifs/search?q={}&api_key=DLPaEHsJbJpHVhCUDjAxp6Eoy7Gc6o8i&limit=10".format(searched)
    contents = urllib.request.urlopen(url).read() 
    jsonContent = json.loads(contents)
    # all of this is the downloading feature for gifs
    #TempGif = randint(1,1000)
    #urllib.request.urlretrieve(jsonContent['data'][randint(0,9)]['images']['fixed_height']['url'], '{}.gif'.format(TempGif))
    #print('downloaded: {}.gif'.format(TempGif))
    await asyncio.sleep(0.5)
    #msg = await bot.send_file(context.message.channel, "{}.gif".format(TempGif))
    if jsonContent['pagination']['total_count'] == 0:
        msg = await bot.send_message(context.message.channel, "I couldn't find anything in my database for {}, whatever that is...".format(search))
        await asyncio.sleep(0.8)
        await bot.edit_message(msg, new_content="I would like you to do anything in your power to kill me with {}, whatever that is...".format(search))
        await asyncio.sleep(0.8)
        await bot.edit_message(msg, new_content="I couldn't find anything in my database for {}, whatever that is...".format(search))
    else:
        msg = await bot.send_message(context.message.channel, "{}".format(jsonContent['data'][randint(0,9)]['images']['fixed_height']['url']))
    #os.remove("{}\{}.gif".format(os.getcwd(),TempGif))
    #print('deleted: {}.gif'.format(TempGif))
    reactmsg = msg
    emo = await bot.wait_for_reaction(timeout=100, message=reactmsg)
    if emo == None:
        await asyncio.sleep(20)
        await bot.delete_message(msg)
        await bot.delete_message(context.message)

@bot.command(pass_context=True)
async def sop(context):
    """Type ?sop to anonymously post an image URL to the Smash or Pass chat"""
    responses = ["Alright pervert calm down, give me your godamned link.", "Gimi da gimi da gimi da linky boss."]
    completion = ["Alright I sent your Pr0n.", 'Donezo.']
    # vote time is in mins
    vote_time = int(smash_time)
    if vote_time < 1:
        display_time = "{} seconds".format(math.floor(vote_time*100))
    else:
        display_time  = "{} minutes".format(vote_time)
    vote_time = vote_time*60
    await bot.delete_message(context.message)
    rec = await bot.send_message(context.message.author, responses[randint(0,len(responses)-1)])
    await bot.start_private_message(context.message.author)
    msg = await bot.wait_for_message(author=context.message.author)
    await bot.send_message(context.message.author, completion[randint(0,len(completion)-1)])
    await bot.send_message(bot.get_channel(smash_pass), "Time to vote!:\n**You have {} to vote**\n{}".format(display_time,msg.content))
    options = ["Smash","Pass"]
    reactions = ['👍', '👎']
    question = "Smash or Pass?"
    description = []
    for x, option in enumerate(options):
        description += '\n{} {}'.format(reactions[x], option)
    embed = discord.Embed(title=question, description=''.join(description))
    react_message = await bot.send_message(bot.get_channel(smash_pass),embed=embed)
    for reaction in reactions[:len(options)]:
        await bot.add_reaction(react_message, reaction)
    embed.set_footer(text='Poll ID: {}'.format(react_message.id))
    await bot.edit_message(react_message, embed=embed)
    print('Smash or Pass timer started')
    print(' ')
    await asyncio.sleep(vote_time)
    print('Smash or Pass timer done')
    print(' ')
    poll_message = await bot.edit_message(react_message, embed=embed)
    if not poll_message.embeds:
        return
    embed = poll_message.embeds[0]
    if poll_message.author != context.message.server.me:
        return
    if not embed['footer']['text'].startswith('Poll ID:'):
        return
    unformatted_options = [x.strip() for x in embed['description'].split('\n')]
    opt_dict = {x[:2]: x[3:] for x in unformatted_options} if unformatted_options[0][0] == '1' \
    else {x[:1]: x[2:] for x in unformatted_options}
    voters = [context.message.server.me.id]
    tally = {x: 0 for x in opt_dict.keys()}
    for reaction in poll_message.reactions:
        if reaction.emoji in opt_dict.keys():
            reactors = await bot.get_reaction_users(reaction)
        for reactor in reactors:
            if reactor.id not in voters:
                tally[reaction.emoji] += 1
                voters.append(reactor.id)
    bold = 'Results:\n' + \
                 '\n'.join(['{}: {}'.format(opt_dict[key], tally[key]) for key in tally.keys()])
    output = "```{}```".format(bold)
    await bot.send_message(bot.get_channel(smash_pass),output)

@bot.group(pass_context=True)
async def steam(ctx):
    """Tools to help you decide what games to play."""
    if ctx.invoked_subcommand is None:
        await bot.say('```Invalid steam command passed...\ndo "?steam help" to find out more about this command```')

@steam.command(pass_context=True)
async def sos(context, *, search: str):
    """Paste some Steam profile urls to get all the common games"""
    await bot.delete_message(context.message)
    s = search.replace(" ", "")
    user_list = s.split(',')
    run = True
    for item in user_list:
        if item[0:25] != "http://steamcommunity.com":
            m = await bot.send_message(context.message.channel,"```The items you entered were not Steam profile URLs do ?steam help to learn more about this command.```")
            await asyncio.sleep(160)
            await bot.delete_message(m)
            run = False
            break
    if run == True:
        msg = await bot.send_message(context.message.channel,"Calculating Games one second...")
        list = getSameGames(user_list)
        lined = ""
        wordcount = ""
        for item in list:
            lined += "{}\n".format(item)
            wordcount += "{} ".format(item)
        if count_letters(wordcount) >= 1900:
            firstpart, secondpart = split(lined)
            await bot.edit_message(msg, new_content="```You all have:\n\n{}```".format(firstpart))
            await bot.send_message(context.message.channel, "```{}```".format(secondpart))
        else:
            await bot.edit_message(msg, new_content="```You all have:\n\n{}```".format(lined))

@steam.command(pass_context=True)
async def roulette(context, *, search: str):
    """Chooses a random game based on steam profile urls"""
    await bot.delete_message(context.message)
    s = search.replace(" ", "")
    user_list = s.split(',')
    run = True
    for item in user_list:
        if item[0:25] != "http://steamcommunity.com":
            m = await bot.send_message(context.message.channel,"```The items you entered were not Steam profile URLs do ?steam help to learn more about this command.```")
            await asyncio.sleep(160)
            await bot.delete_message(m)
            run = False
            break
    if run == True:
        msg = await bot.send_message(context.message.channel,"Calculating Games one second...")
        list = getSameGames(user_list)
        list2 = []
        for item in list:
            list2.append(item)
        for i in range(0,8):
            await asyncio.sleep(0.3)
            game = list2[randint(0,len(list2)-1)]
            await bot.edit_message(msg, new_content="Choosing game: {}".format(game))
        await bot.edit_message(msg, new_content="The game is: {}".format(game))

@steam.command(pass_context=True)
async def help(context):
    """How to use the steam tools"""
    msg = await bot.send_message(context.message.channel,'```?steam\n \nDo "?steam roulette" followed by as many steam profile URLs as you want \n  just make sure to seperate each one with a ,\n  this will give you a random game that all of the steam profiles entered own\n\nDo "?steam sos" followed by as many steam profile URLs as you want \n    just make sure to seperate each one with a ,\n  this will give you a list of all the games the steam profiles have in common\n\nTo get a profile URL go to a users steam profile Right Click>Copy Page URL\n\nExample: ?steam roulette http://steamcommunity.com/profiles/76561198107487727, http://steamcommunity.com/id/Kechipo/```')

@bot.command(pass_context=True)
async def strawpoll(context, *, poll: str):
    """Instantly creates a strawpoll and posts a link to it."""
    poll_data = poll.split(',')
    if len(poll_data) < 3:
        await bot.send_message(context.message.channel,"You need a more items to make a strawpoll. Do ***?strawpoll Title, question, question***\n you can have as many questions as you want just seperate them with a ,")
    else:
        title = poll_data[0]
        questions = poll_data[1:len(poll_data)]
        final_poll = (title, questions)
        data = await make_strawpoll(final_poll)
        print('{} requested strawpoll link, {}'.format(context.message.author,data.title))
        print(' ')
        await bot.send_message(context.message.channel,"Your strawpoll URL is: {}".format(data.url))
        
def count_letters(word):

    return len(word) - word.count(' ')

def split(s):
    half, rem = divmod(len(s), 2)
    return s[:half + rem], s[half + rem:]

def most_common(L):
  # get an iterable of (item, iterable) pairs
  SL = sorted((x, i) for i, x in enumerate(L))
  # print 'SL:', SL
  groups = itertools.groupby(SL, key=operator.itemgetter(0))
  # auxiliary function to get "quality" for an item
  def _auxfun(g):
    item, iterable = g
    count = 0
    min_index = len(L)
    for _, where in iterable:
      count += 1
      min_index = min(min_index, where)
    # print 'item %r, count %r, minind %r' % (item, count, min_index)
    return count, -min_index
  # pick the highest-count/earliest item
  return max(groups, key=_auxfun)[0]

if __name__ == '__main__':
	bot.run(str(apikey))