# coding:utf-8
import os
from discord.ext import commands

client = commands.Bot(command_prefix='')
# client.load_extension('func.bot')
# client.load_extension('func.role')
# client.load_extension('func.squad')
client.load_extension('func.alert')

token = os.environ['token']

@client.event
async def on_ready():
    print('Bot Start')

client.run(token)