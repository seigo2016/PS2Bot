# coding:utf-8
import discord
import datetime
import configparser
import os
from discord.ext import tasks

client = discord.Client()
print("test")
token = os.environ['token']
if not len(token):
    config = configparser.ConfigParser()
    config.read('setting.ini')
    token = config.get("token", 'token')


@tasks.loop(seconds=1)
async def loop():
    now = datetime.now().strftime('%H:%M:%S')
    print(now)
    if now == '00:00:00' or now == '00:00:01':
        body = "あけましておめでとうございます。\n 今年もPlanetSide2JPコミュニティを宜しくお願いします"
        await client.get_guild(344369434103906314).get_channel(385401705975513093).send(body)

loop.start()
client.run(token)
