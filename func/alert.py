
# coding:utf-8
import discord
from discord.ext import tasks, commands
import feedparser
import configparser
import time
from datetime import datetime, timedelta, timezone
import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
config = configparser.ConfigParser()
config.read(current_dir + "/../config.ini")

server_id = int(config['Server']['Server_ID'])
alert_channel_id = int(config['Channel']['Alert_Channel_ID'])


class Alert(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.notice_alert.start()

    @tasks.loop(minutes=5.0)
    async def notice_alert(self):
        # print("Start")
        # ---------Event Information Part START---------#
        alert_rss_url = "https://ps2.fisu.pw/alert/rss?type=CURRENT"
        alert_rss_dic = feedparser.parse(alert_rss_url)
        contents_list = alert_rss_dic["entries"]
        event_body = ""
        for content in contents_list:
            title = content["title"] # title
            summary = content["summary"] # summary
            published_parsed = content["published_parsed"]# published_parsed
            jst = timezone(timedelta(hours=+9), 'Asia/Tokyo')
            published_time = datetime(*published_parsed[:6], tzinfo=timezone.utc).astimezone(jst)
            event_body += f'**{title}**\n {summary}\n Start Time(JST): {published_time}\n'
            event_body += "----------------------------------------\n\n"
        # ---------Event Information Part END---------#
        # ---------Send Message Part START---------#
        em = discord.Embed(
            title='Event Information',
            description=event_body,
            color=discord.Color.orange(),
        )
        await self.bot.get_guild(server_id).get_channel(alert_channel_id).purge(limit=1)
        await self.bot.get_guild(server_id).get_channel(alert_channel_id).send(embed=em)
        # ---------Send Message Part END---------#

    @notice_alert.before_loop
    async def before_ready(self):
        print('waiting...')
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(Alert(bot))