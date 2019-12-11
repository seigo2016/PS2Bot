# coding:utf-8
import discord
import configparser
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
client = discord.Client()
#token = ""
#token = os.environ['token']
#if not len(token):
config = configparser.ConfigParser()
config.read(current_dir+'/token.ini')
token = config.get("token", 'token')


# platoon-lobby-VC "651979369702621196"


def is_me(m):
    return m.user == client.user


lobby_message = {"platoon_textchat_1": ["未編成", "------"],
                 "platoon_textchat_2": ["未編成", "------"],
                 "platoon_textchat_3": ["未編成", "------"],
                 "command_test": ["未編成", "------"]}
chat = {"platoon_textchat_1": "",
        "platoon_textchat_2": "",
        "platoon_textchat_3": "",
        "command_test": ""}

platoon_vc_list = {}
platoon_text_list = {}
platoon_power_message = {}
emoji = []


# @client.event
# async def on_ready():
#     global emoji
#     server = client.get_guild(344369434103906314)


@client.event
async def on_voice_state_update(member, before, after):
    server = client.get_guild(344369434103906314)
    emoji.append(discord.utils.get(server.emojis, name='NC'))
    emoji.append(discord.utils.get(server.emojis, name='TR'))
    emoji.append(discord.utils.get(server.emojis, name='VS'))
    emoji.append(discord.utils.get(server.emojis, name='NS'))
    if "platoon-lobby" in str(after.channel):
        print(member)
        vc_ch = await server.create_voice_channel("platoon_1-test", category=after.channel.category)
        text_ch = await server.create_text_channel("platoon_1-test", category=after.channel.category)
        platoon_vc_list.update({"platoon_1-test": vc_ch})
        platoon_text_list.update({"platoon_1-test": text_ch})
        body = f"{member.mention}\n 小隊が編成されました。\n勢力を選択してください\n"
        await member.move_to(vc_ch)
        text = await text_ch.send(body)
        text_id = text.id
        platoon_power_message.update({"platoon_1-test": text_id})
        for i in emoji:
            await text.add_reaction(i)
    elif str(after.channel) == "None" and len(before.channel.members) == 0:
        vc_id = platoon_vc_list.pop(str(before.channel))
        text_id = platoon_text_list.pop(str(before.channel))
        await vc_id.delete()
        await text_id.delete()


@client.event
async def on_raw_reaction_add(payload):
    if payload.message_id in platoon_power_message.values() and payload.user_id != client.user.id:
        power_name = payload.emoji.name.lower()
        name = "platoon_{}_{}".format(power_name, len(platoon_vc_list))
        ch = client.get_channel(payload.channel_id)
        vc_ch = platoon_vc_list[ch.name]
        await ch.edit(name=name)
        await vc_ch.edit(name=name)
        value = platoon_text_list.pop("platoon_1-test")
        platoon_text_list.update({name: value})
        value = platoon_vc_list.pop("platoon_1-test")
        platoon_vc_list.update({name: value})


@client.event
async def on_message(message):
    if message.content.startswith('!PTR') or message.content.startswith('!PVS') or message.content.startswith('!PNC'):
        cmd = message.content.split()
        print(cmd)
        cmd[0] = cmd[0].lstrip('!P')
        if len(cmd) != 2:
            cmd.append("------")
        if len(cmd[1]) > 30:
            await message.channel.send("Message is too long")
        else:
            await message.channel.send("作成しました")
            lobby_message[str(message.channel)][0] = (cmd[0])
            lobby_message[str(message.channel)][1] = (cmd[1])

            await client.get_guild(344369434103906314).get_channel(383144743783104513).purge(limit=1, check=is_me)
            body = ('<#344401171919798273>    【勢力】   "{}"    コメント    {} \n<#344401275410186253>      【勢力】  "{}"     コメント    {}\n<#344401302169714688>     【勢力】   "{}"    コメント    {}\n').format(
                lobby_message["platoon_textchat_1"][0], lobby_message["platoon_textchat_1"][1], lobby_message["platoon_textchat_2"][0], lobby_message["platoon_textchat_2"][1], lobby_message["platoon_textchat_3"][0], lobby_message["platoon_textchat_3"][1])
            await client.get_guild(344369434103906314).get_channel(383144743783104513).send(body)

    if message.content.startswith('!B'):
        await message.channel.send("解散しました")
        await client.get_guild(344369434103906314).get_channel(383144743783104513).purge(limit=1, check=is_me)
        lobby_message[str(message.channel)][0] = "未編成"
        lobby_message[str(message.channel)][1] = "------"
        body = ('<#344401171919798273>    【勢力】   "{}"    コメント    {} \n<#344401275410186253>      【勢力】  "{}"     コメント    {}\n<#344401302169714688>     【勢力】   "{}"    コメント    {}\n').format(
            lobby_message["platoon_textchat_1"][0], lobby_message["platoon_textchat_1"][1], lobby_message["platoon_textchat_2"][0], lobby_message["platoon_textchat_2"][1], lobby_message["platoon_textchat_3"][0], lobby_message["platoon_textchat_3"][1])
        await client.get_guild(344369434103906314).get_channel(383144743783104513).send(body)
client.run(token)
