# coding:utf-8
import discord
import datetime
import requests
from bs4 import BeautifulSoup
import urllib
import dateutil.parser
import pytz
import configparser
import matplotlib.pyplot as plt
import numpy as np
import json
import os

client = discord.Client()

alltitles = {1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "s", 8: "", 9: ""}

token = os.environ['token']
if not len(token):
    config = configparser.ConfigParser()
    config.read('setting.ini')
    token = config.get("token", 'token')


def is_me(m):
    return m.author == client.user


@client.event
async def on_ready():
    # ---------Event Information part END---------#
    event_page = "http://ps2.fisu.pw/alert/rss"
    event_ret = requests.get(event_page)
    event_titles = []
    description = []
    event_time = []
    alertsoup = BeautifulSoup(event_ret.content, "html.parser")
    for alertitem in alertsoup.find_all("item"):
        event_titles.append(alertitem.find("title").string.split())
        description.append(alertitem.find("description").string)
        time_tmp = alertitem.find("pubdate").string
        time_tmp = dateutil.parser.parse(time_tmp) + \
            datetime.timedelta(minutes=30)
        event_time.append(time_tmp)
    jst = pytz.timezone('Asia/Tokyo')
    now = datetime.datetime.now(jst)
    event_body = "Event Information\n 現在調整中"
    almessage = '\n'
    for i, time in enumerate(event_time):
        time = time.astimezone(jst)
        if time > now and not("[END]" in event_titles[i]):
            event_body += "{} - {} {}\n{}\n{}\n----------------------------------------\n"\
                .format(event_titles[i][0], event_titles[i][1], event_titles[i][2], description[i], time)
    # ---------Event Information part END---------#
    api_url = 'https://ps2.fisu.pw/api/population/?world=40'
    readObj = urllib.request.urlopen(api_url)
    response = readObj.read()
    response_json = json.loads(response)["result"]
    print(response_json)
    # label = ["NC  " + text7, "TR  " + text8, "VS  " + text6, "VS  " + ]
    # x = np.array([int(text7), int(text8), int(text6)])
    # fig = plt.figure(figsize=(3, 3))
    # fig.patch.set_alpha(0.0)
    # plt.subplot(1, 1, 1)
    # plt.pie(x, labels=label, colors=colorlist)
    # plt.title('Soltech Pop \n(All:' + str(text4) + 'Last Updated' + str(now.hour) +
    #           ':' + str(now.minute) + ':' + str(now.second) + ')', fontsize=10)

    # plt.savefig('pop.png')
    em = discord.Embed(
        title='Event Information',
        description=almessage,
        color=discord.Color.orange(),
    )
    await client.get_guild(344369434103906314).get_channel(387540823551639552).purge(limit=2)
    await client.get_guild(344369434103906314).get_channel(387540823551639552).send(embed=em)
    # await client.get_guild(344369434103906314).get_channel(387540823551639552).send(file=discord.File('pop.png'))
client.run(token)
