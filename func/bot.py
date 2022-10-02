# coding:utf-8
import discord
from discord.ext import commands

import os
import configparser

class JoinMember(commands.Cog):

    def __init__(self, bot, env):
        self.bot = bot
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        config = configparser.ConfigParser()
        if env == "dev":
            config.read(self.current_dir + "/../config-dev.ini")
        else:
            config.read(self.current_dir + "/../config.ini")
        self.server_id = int(config['Server']['Server_ID'])
        self.role_channel_id = int(config['Channel']['Role_Channel_ID'])
        self.readme_channel_id = int(config['Channel']['Readme_Channel_ID'])
        self.zatsudan_channel_id = int(config['Channel']['Zatsudan_Channel_ID'])
        self.irassyai_channel_id = int(config['Channel']['Irassyai_Channel_ID'])

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Game(name='PlanetSide 2'))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        readme_channnel = self.bot.get_guild(self.server_id).get_channel(self.readme_channel_id)
        zatsudan_channel = self.bot.get_guild(self.server_id).get_channel(self.zatsudan_channel_id)
        role_channel = self.bot.get_guild(self.server_id).get_channel(self.role_channel_id)
        with open(self.current_dir + "/../message_template/irassyai.txt", "r") as f:
            message_body = f.read()
        message_body = message_body.format(user=member.mention, readme=readme_channnel.mention, zatsudan=zatsudan_channel.mention, role_management=role_channel.mention)
        default_role = discord.utils.get(self.bot.get_guild(self.server_id).roles, name="参加者")
        await self.bot.get_guild(self.server_id).get_channel(self.irassyai_channel_id).send(message_body)
        await member.add_roles(default_role)


def setup(bot, env):
    bot.add_cog(JoinMember(bot, env))
