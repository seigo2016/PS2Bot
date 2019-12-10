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


# platoon-lobby-VC "651979369702621196"


def is_me(m):
    return m.author == client.user


lobby_message = {"platoon_textchat_1": ["未編成", "------"],
                 "platoon_textchat_2": ["未編成", "------"],
                 "platoon_textchat_3": ["未編成", "------"],
                 "command_test": ["未編成", "------"]}
chat = {"platoon_textchat_1": "",
        "platoon_textchat_2": "",
        "platoon_textchat_3": "",
        "command_test": ""}


@client.event
async def on_voice_state_update(member, before, after):
    if "platoon-lobby" in str(after.channel):
        print(member)
        newch = await client.get_guild(344369434103906314).create_voice_channel(
            "Platoon_1-Test", category=360673207356751873)
        await member.move_to(newch)
        # await client.get_guild(344369434103906314).get_channel(383144743783104513).send(body)


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
