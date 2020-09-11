# coding:utf-8
#!/usr/bin/python3
import os
from discord.ext import commands
# if not len(token):
#     config = configparser.ConfigParser()
#     config.read(current_dir+'/token.ini')
#     token = config.get("token", 'token')
client = commands.Bot(command_prefix='')
# client.load_extension('bot')
# client.load_extension('role')
client.load_extension('squad')
token = os.environ['token']

@client.event
async def on_ready():
    print('Bot Start')

client.run(token)