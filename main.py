# coding:utf-8
import os
from discord.ext import commands
import argparse
import func.role as role
import func.squad as squad
import func.alert as alert
import func.bot as bot

parser = argparse.ArgumentParser()

parser.add_argument('--dev', action='store_true')
args = parser.parse_args()

if args.dev:
    env = "dev"
else:
    env = "prod"

client = commands.Bot(command_prefix='')

token = os.environ['token']
# role.setup(client, env)
squad.setup(client, env)
# bot.setup(client, env)
# alert.setup(client, env)

@client.event
async def on_ready():
    print('Bot Start')

client.run(token)
