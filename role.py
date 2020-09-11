# coding:utf-8
from discord.ext import commands
import configparser
import os
import time
import asyncio
import discord

current_dir = os.path.dirname(os.path.abspath(__file__))

config = configparser.ConfigParser()
config.read(current_dir + "/config.ini")
server_id = int(config['Server']['Server_ID'])
role_channel_id = int(config['Channel']['Role_Channel_ID'])
message_id = int(config['Message']['Role_Message_ID'])

class ManageRole(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.emoji_nc_id = 384317676870303745
        self.emoji_tr_id = 384317719098425347
        self.emoji_vs_id = 384317750593585152
        self.emoji_ns_id = 653944468356988938
        self.emoji_jpc_id = 701436271410544660
        self.emoji_nc = self.bot.get_emoji(self.emoji_nc_id)
        self.emoji_tr = self.bot.get_emoji(self.emoji_tr_id)
        self.emoji_vs = self.bot.get_emoji(self.emoji_vs_id)
        self.emoji_ns = self.bot.get_emoji(self.emoji_ns_id)
        self.emoji_jpc = self.bot.get_emoji(self.emoji_jpc_id)
        self.emoji_role = {
            self.emoji_jpc: 'Mercenary', self.emoji_nc: 'MainNC', self.emoji_tr: 'MainTR', self.emoji_vs: 'MainVS', self.emoji_ns: 'NS', '🟦': 'NC', '🟥': 'TR', '🟪': 'VS',
                    '1️⃣': 'Soltech', '2️⃣': 'Connery', '3️⃣': 'Emerald', '4️⃣': 'Miller'}
        self.fixed_message = await self.bot.get_guild(server_id).get_channel(role_channel_id).fetch_message(message_id)
        for emoji_name in self.emoji_role.keys():
            await self.fixed_message.add_reaction(emoji_name)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        self.emoji_nc_id = 384317676870303745
        self.emoji_tr_id = 384317719098425347
        self.emoji_vs_id = 384317750593585152
        self.emoji_ns_id = 653944468356988938
        self.emoji_jpc_id = 701436271410544660
        if not payload.member.bot:
            if payload.message_id == message_id:
                rolelist = {}
                self.emoji_role = {self.emoji_jpc_id: 'Mercenary', self.emoji_nc_id: 'MainNC', self.emoji_tr_id: 'MainTR', self.emoji_vs_id: 'MainVS', self.emoji_ns_id: 'NS', '🟦': 'NC', '🟥': 'TR', '🟪': 'VS',
                    '1️⃣': 'Soltech', '2️⃣': 'Connery', '3️⃣': 'Emerald', '4️⃣': 'Miller'}
                for role_name in self.emoji_role.values():
                    rolelist[role_name] = discord.utils.get(self.bot.get_guild(server_id).roles, name=role_name)
                self.emoji_name = payload.emoji.name
                self.emoji_id = payload.emoji.id
                if self.emoji_id in self.emoji_role:
                    select_role = rolelist[self.emoji_role[self.emoji_id]]
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
                elif self.emoji_name in self.emoji_role:
                    select_role = rolelist[self.emoji_role[self.emoji_name]]
                    if select_role in payload.member.roles:
                        await payload.member.remove_roles(select_role)
                        body = f"`{payload.member}` さんの  `{select_role}` 役職を削除しました \n(このメッセージは一定時間で消去されます)"
                    else:
                        await payload.member.add_roles(select_role)
                        body = f"`{payload.member}` さんに  `{select_role}` 役職を追加しました \n(このメッセージは一定時間で消去されます)"
                    emoji = discord.utils.get(self.bot.get_guild(server_id).emojis, name=self.emoji_name)
                    if emoji:
                        await self.fixed_message.remove_reaction(emoji, payload.member)
                    else:
                        await self.fixed_message.remove_reaction(self.emoji_name, payload.member)
                    reply_message = await self.bot.get_guild(server_id).get_channel(role_channel_id).send(body)
                    await asyncio.sleep(30)
                    await reply_message.delete()

def setup(bot):
    bot.add_cog(ManageRole(bot))