# coding:utf-8
import discord
from discord.ext import commands

import datetime
from datetime import datetime as dt
from datetime import date
from pytz import timezone
import time

import os
import configparser

current_dir = os.path.dirname(os.path.abspath(__file__))

config = configparser.ConfigParser()
config.read(current_dir + "/../config.ini")
server_id = int(config['Server']['Server_ID'])
role_channel_id = int(config['Channel']['Role_Channel_ID'])
readme_channel_id = int(config['Channel']['Readme_Channel_ID'])
zatsudan_channel_id = int(config['Channel']['Zatsudan_Channel_ID'])
irassyai_channel_id = int(config['Channel']['Irassyai_Channel_ID'])

class JoinMember(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        readme_channnel = self.bot.get_guild(server_id).get_channel(readme_channel_id)
        zatsudan_channel = self.bot.get_guild(server_id).get_channel(zatsudan_channel_id)
        role_channel = self.bot.get_guild(server_id).get_channel(role_channel_id)
        with open(current_dir + "/../message_template/irassyai.txt", "r") as f:
            message_body = f.read()
        message_body = message_body.format(user=member.mention, readme=readme_channnel.mention, zatsudan=zatsudan_channel.mention, role_management=role_channel.mention)
        default_role = discord.utils.get(self.bot.get_guild(server_id).roles, name="参加者")
        await self.bot.get_guild(server_id).get_channel(irassyai_channel_id).send(message_body)
        await member.add_roles(default_role)

    @commands.command()
    async def now(self, ctx, *, member: discord.Member = None):
        utc = timezone('UTC')
        pst = timezone('America/Los_Angeles')
        now_time_jst = datetime.datetime.now()
        now_time_pst = now_time_jst.astimezone(pst)
        now_time_utc = now_time_jst.astimezone(utc)
        body = (":flag_jp:(JP)JST   {}\n:flag_us:(US)PST  {}\n:flag_gb:(UK)UTC {}")\
            .format(now_time_jst.strftime('%X'), now_time_pst.strftime('%X'), now_time_utc.strftime('%X'))
        await ctx.send(body)

def setup(bot):
    bot.add_cog(JoinMember(bot))