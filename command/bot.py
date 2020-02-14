# coding:utf-8
import discord
import datetime
import configparser
import os

client = discord.Client()
current_dir = os.path.dirname(os.path.abspath(__file__))
token = os.environ['token']
# if not len(token):
#     config = configparser.ConfigParser()
#     config.read(current_dir+'/token.ini')
#     token = config.get("token", 'token')


@client.event
async def on_message(message):
    if message.content.startswith('!Help'):
        with open(current_dir+"/../help.txt", "r") as f:
            data = f.read()
        co = discord.Color.blue()
        em = discord.Embed(title='Help', description="\n\n" + data, colour=co)
        await message.channel.send(embed=em)
    elif message.content.startswith('PDT') or message.content.startswith('PST') or message.content.startswith('JPDT') or message.content.startswith('JPST'):
        timec = message.content.split()
        chtime2 = timec[1]
        timec2 = chtime2.split(':')
        chhour = int(timec2[0])
        if message.content.startswith('JPDT'):
            chhour = chhour - 16
        elif message.content.startswith('JPST'):
            chhour = chhour - 17
        elif message.content.startswith('PST'):
            chhour = chhour + 17
        elif message.content.startswith('PDT'):
            chhour = chhour + 16
        mi = int(timec2[1])
        if(chhour < 0):
            chhour = chhour + 24
        elif(chhour > 24 and chhour < 49):
            chhour = chhour - 24
        else:
            chhour = chhour
        if (mi < 10 and chhour < 10 and chhour <= 24):
            chhour = str(chhour)
            mi = str(mi)
            await message.channel.send("0" + chhour + ":0" + mi)
        elif (mi >= 10 and chhour < 10 and chhour <= 24):
            chhour = str(chhour)
            mi = str(mi)
            await message.channel.send("0" + chhour + ":" + mi)
        elif (mi < 10 and chhour >= 10 and chhour <= 24):
            chhour = str(chhour)
            mi = str(mi)
            await message.channel.send(chhour + ":0" + mi)
        elif(mi <= 59 and chhour <= 24):
            chhour = str(chhour)
            mi = str(mi)
            await message.channel.send(chhour + ":" + mi)
        else:
            await message.channel.send("正しく入力してください")
    elif message.content.startswith('NOW'):
        dtime = datetime.datetime.now()
        pdtime = dtime + datetime.timedelta(hours=- 16)
        pstime = dtime + datetime.timedelta(hours=- 17)
        body = (":flag_jp:(JP)JDT   {}\n:flag_us:(US)PDT  {}\n:flag_us:(US)PST {}")\
            .format(dtime.strftime('%X'), pdtime.strftime('%X'), pstime.strftime('%X'))
        await message.channel.send(body)

client.run(token)
