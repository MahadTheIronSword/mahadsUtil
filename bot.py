import json
import random
import math
from itertools import islice

import discord
from discord.ext import commands

from exception import *
from api import *

botToken = '[REDACTED]'
botPrefix = 'm!'

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=botPrefix, intents=intents, help_command=None)

errorKey = json.load(open('errors.json'))
commandKey = json.load(open('commands.json'))
factKey = json.load(open('funfacts.json'))


@bot.event
async def on_ready():
    print('Bot is on')


@bot.event
async def process(command):
    await bot.process_commands(command)


@bot.event
async def on_member_join(member):
    joinEmbed = discord.Embed(title=f'Hello {member.name}!', color=discord.Color.from_rgb(236, 240, 241))
    joinEmbed.add_field(name='Welcome', value=f'Welcome to {member.guild}! We hope you have fun here!', inline=False)
    joinEmbed.add_field(name='Rules',
                        value=f'Please read the rules before participating. Breaking any of the rules will result in punishment, ranging from a mute to a ban!',
                        inline=False)
    joinEmbed.add_field(name='Have fun', value='Have fun and stay safe!', inline=False)
    channel = await member.create_dm()
    async for content in channel.history(limit=100):
        if content.author == bot.user:
            await content.delete()

    await member.dm_channel.send(embed=joinEmbed)


@bot.event
async def on_command_error(message, error):
    await message.send(errorKey[type(error).__name__])


@bot.command()
async def latency(message):
    await message.send(f'Latency is currently {bot.latency} milliseconds!')


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(message, user: discord.Member, *, reason=None):
    kickEmbed = discord.Embed(title=f'Kicked {user.name}', color=discord.Color.from_rgb(46, 204, 113))
    kickEmbed.add_field(name='Reason: ', value=reason, inline=False)
    await user.kick(reason=reason)
    await message.send(embed=kickEmbed)


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(message, user: discord.Member, delete_time=0, *, reason=None):
    banEmbed = discord.Embed(title=f'Banned {user.name}', color=discord.Color.from_rgb(46, 204, 113))
    banEmbed.add_field(name='Reason: ', value=reason, inline=False)
    banEmbed.add_field(name='Deleted message history: ', value=f'{delete_time} days', inline=False)
    await user.ban(reason=reason, delete_message_days=delete_time)
    await message.send(embed=banEmbed)


@bot.command()
async def coinflip(message, side: str):
    coinArray = ['heads', 'tails']

    side = side.lower()
    chosen = random.choice(coinArray)

    if side == chosen:
        output = f':coin: It is {chosen}! Congratulations on winning {message.author.mention}!'
        victory = 'You win!'
    elif not side == chosen and side in coinArray:
        output = f'*sad trombone noises* It is {chosen}! You lost {message.author.mention}!'
        victory = 'You lose!'
    else:
        raise IncorrectArguments

    coinflipEmbed = discord.Embed(title='Coinflip', color=discord.Color.from_rgb(211, 84, 0))
    coinflipEmbed.add_field(name=victory, value=output, inline=False)

    await message.send(embed=coinflipEmbed)


@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(message, limit: int):
    await message.channel.purge(limit=limit + 1)
    deleteEmbed = discord.Embed(title='Purge', color=discord.Color.from_rgb(155, 89, 182))
    deleteEmbed.add_field(name='Purge Results', value=f'Successfully deleted {limit} messages!')

    await message.send(embed=deleteEmbed)


@bot.command()
async def rosearch(message, *, username: str):
    userIdJSON = getIdFromUsername(username)

    if userIdJSON.status_code == '429':
        raise TooManyRequests

    userId = userIdJSON.json()['Id']
    results = []

    followersJSON = getUserFollowers(userId)
    results.append(followersJSON)
    friendsJSON = getFriends(userId)
    results.append(friendsJSON)
    statusJSON = getStatus(userId)
    results.append(statusJSON)

    for result in results:
        if result.status_code == '429':
            raise TooManyRequests

    followersJSON = followersJSON.json()['count']
    friendsJSON = len(friendsJSON.json()['data'])
    statusJSON = statusJSON.json()['description']

    robloxEmbed = discord.Embed(title=userIdJSON.json()['Username'], color=discord.Color.from_rgb(231, 76, 60))
    robloxEmbed.add_field(name='Status: ', value=statusJSON or 'User has no status', inline=False)
    robloxEmbed.add_field(name='Friends: ', value=friendsJSON, inline=False)
    robloxEmbed.add_field(name='Followers: ', value=followersJSON, inline=False)

    await message.send(embed=robloxEmbed)


@bot.command()
async def funfact(message):
    fact = random.choice(factKey)
    factEmbed = discord.Embed(title='Fun Fact', color=discord.Color.from_rgb(26, 188, 156))
    factEmbed.add_field(name='Fact: ', value=fact, inline=False)
    await message.send(embed=factEmbed)


@bot.command()
async def add(message, x: float, y: float):
    addEmbed = discord.Embed(title='Addition', color=discord.Color.from_rgb(243, 156, 18))
    addEmbed.add_field(name='Answer: ', value=f'The answer is {x + y}', inline=False)
    await message.send(embed=addEmbed)


@bot.command()
async def subtract(message, x: float, y: float):
    subtractEmbed = discord.Embed(title='Subtraction', color=discord.Color.from_rgb(243, 156, 18))
    subtractEmbed.add_field(name='Answer: ', value=f'The answer is {x - y}', inline=False)
    await message.send(embed=subtractEmbed)


@bot.command()
async def multiply(message, x: float, y: float):
    multiplyEmbed = discord.Embed(title='Multiply', color=discord.Color.from_rgb(243, 156, 18))
    multiplyEmbed.add_field(name='Answer: ', value=f'The answer is {x * y}', inline=False)
    await message.send(embed=multiplyEmbed)


@bot.command()
async def divide(message, x: float, y: float):
    divideEmbed = discord.Embed(title='Divide', color=discord.Color.from_rgb(243, 156, 18))
    divideEmbed.add_field(name='Answer: ', value=f'The answer is {x / y}', inline=False)
    await message.send(embed=divideEmbed)


@bot.command()
async def exponent(message, x: float, y: float):
    exponentEmbed = discord.Embed(title='Exponent', color=discord.Color.from_rgb(243, 156, 18))
    exponentEmbed.add_field(name='Answer: ', value=f'The answer is {x ** y}')
    await message.send(embed=exponentEmbed)


@bot.command()
async def wikipedia(message):
    wikipediaJSON = getWikipediaArticle()
    wikipediaEmbed = discord.Embed(title='Wikipedia', color=discord.Color.from_rgb(192, 57, 43))
    wikipediaEmbed.set_thumbnail(url=wikipediaJSON['thumbnail']['source'])
    wikipediaEmbed.add_field(name=wikipediaJSON['title'], value=wikipediaJSON['content_urls']['desktop']['page'])
    await message.send(embed=wikipediaEmbed)


@bot.command()
@commands.has_permissions(administrator=True)
async def dm(message, user: discord.Member, *, content: str):
    await user.create_dm()
    await user.dm_channel.send(content)
    dmEmbed = discord.Embed(title='DM', color=discord.Color.from_rgb(127, 140, 141))
    dmEmbed.add_field(name='''DM result''', value=f'''Successfully DM'd {user.name}''')
    await message.send(embed=dmEmbed)


@bot.command()
async def pi(message):
    piEmbed = discord.Embed(title=f'Pi', color=discord.Color.from_rgb(22, 160, 133))
    piEmbed.add_field(name='Pi is', value=math.pi)
    await message.send(embed=piEmbed)


@bot.command()
async def cmdlist(message, page: int):
    maxPage = math.ceil(len(commandKey) / 10)

    if page > maxPage:
        raise PageOverflow

    commandEmbed = discord.Embed(title=f'Command list(Page {page}/{maxPage})', color=discord.Color.from_rgb(241, 196, 15))
    items = commandKey.items()
    for i, v in islice(items, page * 10 - 10, page * 10 - 1, 1):
        commandEmbed.add_field(name=i, value=v['description'], inline=False)

    await message.send(embed=commandEmbed)


@bot.command()
async def cmdhelp(message, *, command: str):
    commandInfo = commandKey.get(command)
    if commandInfo:
        helpEmbed = discord.Embed(title=commandInfo['title'], color=discord.Color.from_rgb(52, 152, 219))
        helpEmbed.add_field(name='Description: ', value=commandInfo['description'], inline=False)
        helpEmbed.add_field(name='Format: ', value=commandInfo['format'], inline=False)
        helpEmbed.add_field(name='Example: ', value=commandInfo['example'], inline=False)
        await message.send(embed=helpEmbed)
    else:
        raise IndexError


bot.run(botToken)
