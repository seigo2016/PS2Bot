# coding:utf-8
import discord
import configparser
import os
import time
import asyncio

client = discord.Client()
current_dir = os.path.dirname(os.path.abspath(__file__))
token = os.environ['token']

# if not len(token):
#     config = configparser.ConfigParser()
#     config.read(current_dir+'/token.ini')
#     token = config.get("token", 'token')

message_channel_id = 697084660773027880
message_server_id = 344369434103906314
message_id = 697085942779084841

@client.event
async def on_ready():
    global fixed_message
    emoji_role = {'NS': 'NS', 'NC': 'NC', 'TR': 'TR', 'VS': 'VS', 'JPC': 'Mercenary', '🟦': 'MainNC', '🟥': 'MainTR', '🟪': 'MainVS',
                '1️⃣': 'Soltech', '2️⃣': 'Connery', '3️⃣': 'Emerald', '4️⃣': 'Miller'}
    fixed_message = await client.get_guild(message_server_id).get_channel(message_channel_id).fetch_message(message_id)
    for emoji_name in emoji_role.keys():
        emoji = discord.utils.get(client.get_guild(message_server_id).emojis, name=emoji_name)
        if emoji:
            await fixed_message.add_reaction(emoji)
        else:
            await fixed_message.add_reaction(emoji_name)

@client.event
async def on_raw_reaction_add(payload):
    if not payload.member.bot:
        if payload.message_id == message_id:
            rolelist = {}
            emoji_role = {'NS': 'NS', 'NC': 'NC', 'TR': 'TR', 'VS': 'VS', 'JPC': 'Mercenary', '🟦': 'MainNC', '🟥': 'MainTR', '🟪': 'MainVS',
                    '2️⃣': 'Connery', '3️⃣': 'Emerald', '1️⃣': 'Soltech', '4️⃣': 'Miller'}
            for role_name in emoji_role.values():
                rolelist[role_name] = discord.utils.get(client.get_guild(message_server_id).roles, name=role_name)
            emoji_name = payload.emoji.name
            if emoji_name in emoji_role:
                select_role = rolelist[emoji_role[emoji_name]]
                if select_role in payload.member.roles:
                    await payload.member.remove_roles(select_role)
                    body = f"`{payload.member}` さんの  `{select_role}` 役職を削除しました \n(このメッセージは一定時間で消去されます)"
                else:
                    await payload.member.add_roles(select_role)
                    body = f"`{payload.member}` さんに  `{select_role}` 役職を追加しました \n(このメッセージは一定時間で消去されます)"
                emoji = discord.utils.get(client.get_guild(message_server_id).emojis, name=emoji_name)
                if emoji:
                    await fixed_message.remove_reaction(emoji, payload.member)
                else:
                    await fixed_message.remove_reaction(emoji_name, payload.member)
                reply_message = await client.get_guild(message_server_id).get_channel(message_channel_id).send(body)
                await asyncio.sleep(30)
                await reply_message.delete()



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
        rolelist[key] = discord.utils.get(client.get_guild(message_server_id).roles, name=val)
    if 'irassyai-channel' in str(message.channel):
        is_rolech = True
    elif 'test' in str(message.channel):
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
