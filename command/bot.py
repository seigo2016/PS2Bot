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

config = configparser.ConfigParser()
config.read(current_dir + "/../config.ini")
server_id = int(config['Server']['Server_ID'])
role_channel_id = int(config['Channel']['Role_Channel_ID'])
readme_channel_id = int(config['Channel']['Readme_Channel_ID'])
zatsudan_channel_id = int(config['Channel']['Zatsudan_Channel_ID'])
irassyai_channel_id = int(config['Channel']['Irassyai_Channel_ID'])

@client.event
async def on_member_join(member):
    readme_channnel = client.get_guild(server_id).get_channel(readme_channel_id)
    zatsudan_channel = client.get_guild(server_id).get_channel(zatsudan_channel_id)
    role_channel = client.get_guild(server_id).get_channel(role_channel_id)
    with open(current_dir+"/../message_template/irassyai.txt", "r") as f:
        message_body = f.read()
    message_body = message_body.format(user=member.mention, readme=readme_channnel.mention, zatsudan=zatsudan_channel.mention, role_management=role_channel.mention)
    await client.get_guild(server_id).get_channel(irassyai_channel_id).send(message_body)

@client.event
async def on_message(message):
    jst = timezone('Japan')
    utc = timezone('UTC')
    pst = timezone('America/Los_Angeles')
    if message.content.startswith('!Help'):
        with open(current_dir+"/../message_template/help.txt", "r") as f:
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
