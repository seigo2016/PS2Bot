# coding:utf-8
from discord.ext import commands
import discord
import configparser
from datetime import datetime, timedelta, timezone
import os
import websockets
import requests
import json

class Event(commands.Cog):
    def __init__(self, bot, env):
        self.bot = bot
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config = configparser.ConfigParser(interpolation=None)
        if env == "dev":
            config.read(current_dir + "/../config-dev.ini")
        else:
            config.read(current_dir + "/../config.ini")

        self.server_id = int(config['Server']['Server_ID'])
        self.outfit_event_channel_id = int(config['Channel']['Outfit_Event_Channel_ID'])
        self.JST = timezone(timedelta(hours=+9), 'JST')
        
    @commands.Cog.listener()
    async def on_ready(self):
        await self.stream()

    async def stream(self):
        self.path = "wss://push.planetside2.com/streaming?environment=ps2&service-id=s:seigo2016"
        async with websockets.connect(self.path) as websocket:
            message = '{"service":"event","action":"subscribe","worlds":["40"],"eventNames":["FacilityControl"]}'
            await websocket.send(message)
            while True:
                msg = await websocket.recv()
                resp = json.loads(msg)
                if "type" in resp:
                    if resp["type"] == "heartbeat":
                        continue
                if "payload" in resp:
                    outfit_id = "37554038458832678"
                    body = resp["payload"]
                    if body["outfit_id"] == "0":
                        continue
                    elif body["outfit_id"] == outfit_id:
                        if body["new_faction_id"] == ["old_faction_id"]:
                            continue
                        elif body["new_faction_id"] != "1":
                            continue
                        self.status_api_url = "https://census.daybreakgames.com/get/ps2:v2/map_region"
                        params ={
                            "facility_id": body["facility_id"],
                        }
                        status_result = requests.get(self.status_api_url, params=params)
                        status_result_body = status_result.json()['map_region_list'][0]
                        event_time = datetime.utcfromtimestamp(int(body["timestamp"]))
                        em = discord.Embed(
                            title='Facility Capture Event (NJPC)',
                            description=f"**Facility Name**: {status_result_body['facility_name']}",
                            color=discord.Color.blue(),
                            timestamp=event_time
                        )
                        print(resp)
                        await self.bot.get_guild(self.server_id).get_channel(self.outfit_event_channel_id).send(embed=em)
                    continue
                
                print(resp)
                
                

def setup(bot, env):
    bot.add_cog(Event(bot, env))
