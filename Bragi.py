# Bragi.py
import os
import random

from pickler import *
from randomOrg import *
from game import *

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='~',intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
            
@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}, welcome to my Discord server!')

@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
        'Nothings okay. Wuntch, circling me like a shark frenzied by chum. The task force turning into a career-threatening quagmire. An Internal Affairs investigation casting doubt upon my integrity. And you ask, is everything okay? I am buffeted by the winds of my foes enmity and cast about by the towering waves of cruel fate. Yet I, a Captain, am no longer able to command my vessel, my precinct, from my customary helm, my office. And you ask, is everything okay? Ive worked the better part of my years on earth overcoming every prejudice and fighting for the position I hold, and now I feel it being ripped from my grasp, and with it the very essence of what defines me as a man. And you ask, is everything okay?',
        'Nutrition bricks.',
        'Nutrition Bricks. I have original no flavor, and whole wheat no flavor.',
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

@bot.command(name='roll', help='Simulate rolling dice! Syntax: roll <Number of Dice> <Number of Sides>')
async def roll(ctx, Number_of_Dice:int = -1, Number_of_Sides:int = -1):
    if Number_of_Dice>=0 and Number_of_Sides>=0:
        dice = [
            str(random.choice(range(1,Number_of_Sides + 1)))
            for _ in range(Number_of_Dice)
        ]
    else:
        response = "```Error: Invalid Input. Please review the syntax of the command.\n" + bot.command_prefix + "roll <Number of Dice> <Number of Sides>```"
        await ctx.send(response)

    await ctx.send(', '.join(dice))

@bot.command(name='create', help = 'Create a channel with a unique name!')
@commands.has_role('admin')
async def create(ctx, channel_name='real-python'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)
        await ctx.send('```Creating a new channel: ' + channel_name + '```')
    else:
        print(f'```{channel_name} already exists! Please chose a unique channel name.```')
        await ctx.send('```' + channel_name + ' already exists! Please chose a unique channel name.```')

@bot.event
async def on_command_error(ctx, error):
    
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('```You do not have the correct role for this command.```')


bot.run(TOKEN)