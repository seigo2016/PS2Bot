# coding:utf-8
import discord
import datetime
import configparser
import os
from datetime import datetime as dt
from datetime import date
from pytz import timezone
import time

client = discord.Client()
current_dir = os.path.dirname(os.path.abspath(__file__))
token = os.environ['token']
# if not len(token):
#     config = configparser.ConfigParser()
#     config.read(current_dir+'/token.ini')
#     token = config.get("token", 'token')


@client.event
async def on_message(message):
    jst = timezone('Japan')
    utc = timezone('UTC')
    pst = timezone('America/Los_Angeles')
    if message.content.startswith('!Help'):
        with open(current_dir+"/../help.txt", "r") as f:
            data = f.read()
        color = discord.Color.blue()
        em = discord.Embed(title='Help', description="\n\n" + data, colour=color)
        await message.channel.send(embed=em)
    elif message.content.startswith('J2PST') or message.content.startswith('P2JST'):
        try:
            commandText = message.content.split()
            today = date.today().strftime('%Y/%m/%d')
            strCurrentTime = commandText[1]
            if message.content.startswith('J2PST'):
                currentTimeJST = dt.strptime(today + ' ' + strCurrentTime, '%Y/%m/%d %H:%M:%S')
                currentTimeUTC = currentTimeJST.astimezone(utc)
                currentTimePST = currentTimeUTC.astimezone(pst)
                resultTime = currentTimePST
            elif message.content.startswith('P2JST'):
                currentTimePST = dt.strptime(today + ' ' + strCurrentTime, '%Y/%m/%d %H:%M:%S')
                currentTimeUTC = currentTimePST.astimezone(utc)
                currentTimeJST = currentTimeUTC.astimezone(jst)
                resultTime = currentTimeJST
            await message.channel.send(resultTime.strftime('%H:%M:%S'))
        except Exception as e:
            print(e)
            message.channel.send("正しい値を入力してください")

    elif message.content.startswith('NOW'):
        nowTimeJST = datetime.datetime.now()
        nowTimePST = nowTimeJST.astimezone(pst)
        nowTimeUTC = nowTimeJST.astimezone(utc)
        body = (":flag_jp:(JP)JDT   {}\n:flag_us:(US)PST  {}\n:flag_gb:(UK)UTC {}")\
            .format(nowTimeJST.strftime('%X'), nowTimePST.strftime('%X'), nowTimeUTC.strftime('%X'))
        await message.channel.send(body)

client.run(token)
