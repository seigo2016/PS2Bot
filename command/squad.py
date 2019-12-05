# coding:utf-8
import discord
import configparser
client = discord.Client()

config = configparser.ConfigParser()
config.read('setting.ini')
token = config.get("token", 'token')

typename = ""


def is_me(m):
    return m.author == client.user


allchat = {"platoon_textchat_1": ["未編成", "------"], "platoon_textchat_2": ["未編成", "------"], "platoon_textchat_3": [
    "未編成", "------"], "command_test": ["未編成", "------"]}
chat = {"platoon_textchat_1": "", "platoon_textchat_2": "",
        "platoon_textchat_3": "", "command_test": ""}


@client.event
async def on_message(message):
    if message.content.startswith('!PTR') or message.content.startswith('!PVS') or message.content.startswith('!PNC'):
        typename = message.content.split()
        typename[0] = typename[0].lstrip('!P')
        if len(typename) != 2:
            typename.append("------")
        if len(typename[1]) > 30:
            await message.channel.send("Message is too long")
        else:
            await message.channel.send("作成しました")
            allchat[str(message.channel)][0] = (typename[0])
            allchat[str(message.channel)][1] = (typename[1])

            await client.get_guild(344369434103906314).get_channel(383144743783104513).purge(limit=1, check=is_me)
            body = ('<#344401171919798273>    【勢力】   "{}"    コメント    {} \n<#344401275410186253>      【勢力】  "{}"     コメント    {}\n<#344401302169714688>     【勢力】   "{}"    コメント    {}\n').format(
                allchat["platoon_textchat_1"][0], allchat["platoon_textchat_1"][1], allchat["platoon_textchat_2"][0], allchat["platoon_textchat_2"][1], allchat["platoon_textchat_3"][0], allchat["platoon_textchat_3"][1])
            await client.get_guild(344369434103906314).get_channel(383144743783104513).send(body)

    if message.content.startswith('!B'):

        await message.channel.send("解散しました")
        await client.get_guild(344369434103906314).get_channel(383144743783104513).purge(limit=1, check=is_me)
        allchat[str(message.channel)][0] = "未編成"
        allchat[str(message.channel)][1] = "------"
        body = ('<#344401171919798273>    【勢力】   "{}"    コメント    {} \n<#344401275410186253>      【勢力】  "{}"     コメント    {}\n<#344401302169714688>     【勢力】   "{}"    コメント    {}\n').format(
            allchat["platoon_textchat_1"][0], allchat["platoon_textchat_1"][1], allchat["platoon_textchat_2"][0], allchat["platoon_textchat_2"][1], allchat["platoon_textchat_3"][0], allchat["platoon_textchat_3"][1])
        await client.get_guild(344369434103906314).get_channel(383144743783104513).send(body)
client.run(token)
