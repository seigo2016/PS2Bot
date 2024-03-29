# coding:utf-8
import discord
from discord.ext import tasks, commands
import configparser
from datetime import datetime
import os
import requests
import matplotlib.pyplot as plt
import numpy as np
import io

class Alert(commands.Cog):
    def __init__(self, bot, env):
        self.bot = bot
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config = configparser.ConfigParser(interpolation=None)
        if env == "dev":
            config.read(current_dir + "/../config-dev.ini")
        else:
            config.read(current_dir + "/../config.ini")

        self.server_id = int(config['Server']['Server_ID'])
        self.alert_channel_id = int(config['Channel']['Alert_Channel_ID'])
        self.population_url = config['API']['FISU_API_ENDPOINT']
        self.status_api_url = config['API']['CENSUS_API_ENDPOINT']

    @commands.Cog.listener()
    async def on_ready(self):  
        self.notice_alert.start()

    @tasks.loop(minutes=5.0)
    async def notice_alert(self):
        params = {
            "game_code": "ps2",
            "name": "SolTech (Asia)"
        }
        status_result = requests.get(self.status_api_url, params=params)
        if not 'json' in status_result.headers.get('content-type'):
            exit()
        status_json_data = status_result.json()["game_server_status_list"][0]
        server_status = status_json_data["last_reported_state"]
        status_emoji = ""
        if server_status != "down":
            status_emoji = ":blue_circle:"
        elif server_status == "down":
            status_emoji = ":red_circle:"
        pop_result = requests.get(self.population_url)
        pop_json_data = pop_result.json()["result"][0]
        
        data = np.array([[pop_json_data['vs'], pop_json_data['nc'], pop_json_data['tr'], pop_json_data['ns']]])
        pop_time = datetime.utcfromtimestamp(pop_json_data['timestamp'])
        data_cum=data.cumsum(axis=1)
        category_names = ["VS", "NC", "TR", "NS"]
        color = ["#612597", "#1d4698", "#961100", "#d3d3d3"]
        lavel_color = ["#ffffff", "#ffffff", "#ffffff","#333333"]
        plt.figure()
        fig, ax = plt.subplots(figsize=(8, 1))
        ax.invert_yaxis()
        ax.xaxis.set_visible(False)
        ax.set_xlim(0, np.sum(data, axis=1).max())

        for i in range(4):
            widths = data[:, i]
            starts = data_cum[:, i] - widths
            rects = ax.barh("Soltech", widths, height=0.5, left=starts, label=category_names[i], color=color[i])
            ax.bar_label(rects, label_type='center', color=lavel_color[i])
        ax.legend(ncol=len(category_names), bbox_to_anchor=(1.2, 1), loc='upper right', borderaxespad=0, fontsize='small')
        ax.get_legend().remove()
        with io.BytesIO() as sio:
            plt.savefig(sio, format="png")
            plt.close('all')
            sio.seek(0)
            em = discord.Embed(
                title='Current Population (soltech)',
                description=f"**Soltech**:  {server_status.upper()} {status_emoji}",
                color=discord.Color.orange(),
                timestamp=pop_time
            )
            em.set_image(
                url="attachment://image.png"
            )
            await self.bot.get_guild(self.server_id).get_channel(self.alert_channel_id).purge(limit=1)
            await self.bot.get_guild(self.server_id).get_channel(self.alert_channel_id).send(embed=em, file=discord.File(sio, filename='image.png'))

def setup(bot, env):
    bot.add_cog(Alert(bot, env))
