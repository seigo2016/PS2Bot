# coding:utf-8
import discord
import configparser
import os

client = discord.Client()

token = os.environ['token']
if not len(token):
    config = configparser.ConfigParser()
    config.read('setting.ini')
    token = config.get("token", 'token')


@client.event
async def on_message(message):
    addmsg = '\n'
    rmmsg = '\n'
    add_role = {'NS': 'NS', 'NC': 'NC', 'TR': 'TR', 'VS': 'VS', 'MALL': 'Mercenary', 'MNC': 'MainNC', 'MTR': 'MainTR', 'MVS': 'MainVS',
                'CONNERY': 'Connery', 'BRIGGS': 'Briggs', 'EMERALD': 'Emerald', 'SOLTECH': 'Soltech', 'MILLER': 'Miller'}
    rm_role = {'DNC': 'NC', 'DTR': 'TR', 'DVS': 'VS', 'DMNC': 'MNC', 'DMTR': 'MTR', 'DMVS': 'MVS',
               'DCONNERY': 'Connery', 'DBRIGGS': 'Briggs', 'DEMERALD': 'Emerald', 'DSOLTECH': 'Soltech', 'DMILLER': 'Miller', 'DMALL': 'MALL', 'DNS': 'NS'}
    rolelist = {}
    addrolelist = []
    rmrolelist = []
    is_rolech = False
    for key, val in add_role.items():
        rolelist[key] = discord.utils.get(
            client.get_guild(344369434103906314).roles, name=val)
    if str(message.channel).find('irassyai-channel') != -1:
        is_rolech = True
    elif str(message.channel).find('test') != -1:
        is_rolech = True
    if not message.author.bot and is_rolech:
        text = message.content.upper()
        text = text.split()
        for i in text:
            for j in range(len(add_role)):
                if i == list(add_role.keys())[j]:
                    addrolelist.append(rolelist[i])
                if i == list(rm_role.keys())[j]:
                    rmrolelist.append(rolelist[rm_role[i].upper()])
        if len(addrolelist):
            await message.author.add_roles(*addrolelist)
        if len(rmrolelist):
            await message.author.remove_roles(*rmrolelist)
        for j in addrolelist:
            await message.author.add_roles(j)
            addmsg += str(j) + '\n'
        for k in rmrolelist:
            rmmsg += str(k) + '\n'
        if len(addmsg) != 1 or len(rmmsg) != 1:
            if len(addmsg) == 1:
                addmsg = '\nNone\n'
            if len(rmmsg) == 1:
                rmmsg = '\nNone\n'
            em = discord.Embed(title='Changed role', description='__**Add**__' + addmsg + '__**Remove**__' +
                               rmmsg + '\n\n__**To**__\n' + str(message.author), color=discord.Color.green())
            await message.channel.send(embed=em)
client.run(token)
