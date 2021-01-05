# coding:utf-8
from discord.ext import commands
import discord

import configparser
import os

import time
import asyncio

current_dir = os.path.dirname(os.path.abspath(__file__))

config = configparser.ConfigParser()
config.read(current_dir + "/../config.ini")
server_id = int(config['Server']['Server_ID'])
role_channel_id = int(config['Channel']['Role_Channel_ID'])
message_id = int(config['Message']['Role_Message_ID'])

class ManageRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        emoji_main_nc = self.bot.get_emoji(384317676870303745)
        emoji_main_tr = self.bot.get_emoji(384317719098425347)
        emoji_main_vs = self.bot.get_emoji(384317750593585152)
        emoji_main_ns = self.bot.get_emoji(653944468356988938)
        emoji_main_jpc = self.bot.get_emoji(701436271410544660)
        self.emoji_role = {
            emoji_main_jpc: 'Mercenary', emoji_main_nc: 'MainNC', emoji_main_tr: 'MainTR', emoji_main_vs: 'MainVS',\
            emoji_main_ns: 'NS', '🟦': 'NC', '🟥': 'TR', '🟪': 'VS',\
            '1️⃣': 'Soltech', '2️⃣': 'Connery', '3️⃣': 'Emerald', '4️⃣': 'Miller'}
        self.fixed_message = await self.bot.get_guild(server_id).get_channel(role_channel_id).fetch_message(message_id)
        for emoji_name in self.emoji_role.keys():
            await self.fixed_message.add_reaction(emoji_name)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            pass
        elif payload.message_id == message_id:
            role_list = {}
            for role_name in self.emoji_role.values():
                role_list[role_name] = discord.utils.get(self.bot.get_guild(server_id).roles, name=role_name)
            reaction_emoji = self.bot.get_emoji(payload.emoji.id)
            if reaction_emoji in self.emoji_role:
                select_role = role_list[self.emoji_role[reaction_emoji]]
                complete_add_role = True
            elif payload.emoji.name in self.emoji_role:
                select_role = role_list[self.emoji_role[payload.emoji.name]]
                complete_add_role = True
            else:
                complete_add_role = False
            if complete_add_role:
                if select_role in payload.member.roles:
                    await payload.member.remove_roles(select_role)
                    body = f"`{payload.member}` さんの  `{select_role}` 役職を削除しました \n(このメッセージは一定時間で消去されます)"
                else:
                    await payload.member.add_roles(select_role)
                    body = f"`{payload.member}` さんに  `{select_role}` 役職を追加しました \n(このメッセージは一定時間で消去されます)"
                await self.fixed_message.remove_reaction(payload.emoji, payload.member)
                reply_message = await self.bot.get_guild(server_id).get_channel(role_channel_id).send(body)
                await asyncio.sleep(30)
                await reply_message.delete()

def setup(bot):
    bot.add_cog(ManageRole(bot))
