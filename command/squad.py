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

server_id = int(config['Server']['Server_ID'])

def is_me(m):
    return m.user == client.user

squad_list = {}
emoji = []

@client.event
async def on_voice_state_update(member, before, after):
    print(squad_list)
    global squad_list
    server = client.get_guild(server_id)
    emoji.append(client.get_emoji(384317676870303745))
    emoji.append(client.get_emoji(384317719098425347))
    emoji.append(client.get_emoji(384317750593585152))
    emoji.append(client.get_emoji(653944468356988938))
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
    # if (after.channel == None or after.channel != before.channel) and str(before.channel) != "squad-lobby":
    if before.channel in squad_list:
        print("test")
        if before.channel and len(before.channel.members) == 0:
            text_ch = client.get_channel(squad_list[before.channel.id]["text_id"])
            vc_ch = client.get_channel(before.channel.id)
            squad_list.pop(before.channel.id)
            await vc_ch.delete()
            await text_ch.delete()


@client.event
async def on_raw_reaction_add(payload):
    # print("reaction " + str(squad_list))
    emoji_nc_id = 384317676870303745
    emoji_tr_id = 384317719098425347
    emoji_vs_id = 384317750593585152
    emoji_ns_id = 653944468356988938
    power_emoji = {emoji_nc_id:"NC", emoji_tr_id:"TR", emoji_vs_id: "VS", emoji_ns_id:"NS"}
    server = client.get_guild(server_id)
    power_color = {"NC":"\U0001F7E6","TR":"\U0001F7E5","VS":"\U0001F7EA", "NS":"\u2B1C"}
    flg = False
    for vc_id, squad in squad_list.items():
        if squad["text_id"] == payload.channel_id:
            user = server.get_member(payload.user_id)
            if payload.user_id != client.user.id and user == squad["user"]:
                power_name = power_emoji[payload.emoji.id]
                name = "{}_squad{}".format(power_name,power_color[power_name])
                vc_ch = client.get_channel(vc_id)
                text_ch  = client.get_channel(payload.channel_id)
                await text_ch.edit(name=name)
                await vc_ch.edit(name=name)

client.run(token)
