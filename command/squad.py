# coding:utf-8
import discord
import configparser
import os
import random

current_dir = os.path.dirname(os.path.abspath(__file__))
client = discord.Client()
token = os.environ['token']
# if not len(token):
#     config = configparser.ConfigParser()
#     config.read(current_dir+'/token.ini')
#     token = config.get("token", 'token')
# platoon-lobby-VC "651979369702621196"

config = configparser.ConfigParser()
config.read(current_dir + "/../config.ini")

server_id = config['Server']['Server_ID']

def is_me(m):
    return m.user == client.user

squad_list = {}
emoji = []

@client.event
async def on_voice_state_update(member, before, after):
    server = client.get_guild(server_id)
    emoji.append(discord.utils.get(server.emojis, name='NC'))
    emoji.append(discord.utils.get(server.emojis, name='TR'))
    emoji.append(discord.utils.get(server.emojis, name='VS'))
    emoji.append(discord.utils.get(server.emojis, name='NS'))
    if "squad-lobby" in str(after.channel):
        vc_ch = await server.create_voice_channel("squad", category=after.channel.category)
        text_ch = await server.create_text_channel("squad", category=after.channel.category)
        squad_list.update({vc_ch.id:{"text_id":text_ch.id, "msg_id":"", "user":member}})
        body = f"{member.mention}\n 小隊が編成されました。\n勢力を選択してください\n"
        await member.move_to(vc_ch)
        text = await text_ch.send(body)
        text_id = text.id
        squad_list[vc_ch.id]["msg_id"] = text_id
        for i in emoji:
            await text.add_reaction(i)
    elif (after.channel == None or after.channel != before.channel) and len(before.channel.members) == 0:  #and str(before.channel) != "squad-lobby") and len(before.channel.members) == 0:
        text_ch = client.get_channel(squad_list[before.channel.id]["text_id"])
        vc_ch = client.get_channel(before.channel.id)
        squad_list.pop(before.channel.id)
        await vc_ch.delete()
        await text_ch.delete()


@client.event
async def on_raw_reaction_add(payload):
    server = client.get_guild(server_id)
    power_color = {"NC":"\U0001F7E6","TR":"\U0001F7E5","VS":"\U0001F7EA", "NS":"\u2B1C"}
    flg = False
    for x, y in squad_list.items():
        try:
            keys = [k for k, l in y.items() if l == payload.channel_id]
            flg = True
        except Exception as e:
            print(e)
        if flg:
            vc_id = x
            break
    user = server.get_member(payload.user_id)
    if payload.user_id != client.user.id and user == squad_list[vc_id]["user"]:
        power_name = payload.emoji.name.lower()
        name = "{}_squad{}".format(power_name,power_color[payload.emoji.name])
        vc_ch = client.get_channel(vc_id)
        text_ch  = client.get_channel(payload.channel_id)
        await text_ch.edit(name=name)
        await vc_ch.edit(name=name)
        
client.run(token)
