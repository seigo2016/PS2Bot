
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
current_dir = os.path.dirname(os.path.abspath(__file__))
token = os.environ['token']
# if not len(token):
#     config = configparser.ConfigParser()
#     config.read(current_dir+'/token.ini')
#     token = config.get("token", 'token')


@client.event
async def on_ready():
    # ---------Event Information Part START---------#
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
    event_body = ""
    for i, time in enumerate(event_time):
        time = time.astimezone(jst)
        if time > now and not("[END]" in event_titles[i]):
            event_body += "{} - {} {}\n{}\n{}\n----------------------------------------\n"\
                .format(event_titles[i][0], event_titles[i][1], event_titles[i][2], description[i], time)
    # ---------Event Information Part END---------#
    # ---------Get Population Part START---------#
    api_url = 'https://ps2.fisu.pw/api/population/?world=40'
    readObj = urllib.request.urlopen(api_url)
    response = readObj.read()
    response_json = json.loads(response)["result"][0]
    nc_pop = response_json["nc"]
    tr_pop = response_json["tr"]
    vs_pop = response_json["vs"]
    ns_pop = response_json["ns"]
    all_pop = nc_pop + tr_pop + vs_pop + ns_pop
    colorlist = ["b", "red", "purple", "gray"]
    updatetime = response_json["timestamp"]
    updatetime = datetime.datetime.fromtimestamp(updatetime).astimezone(jst)
    label = ["NC  " + str(nc_pop), "TR  " + str(tr_pop),
             "VS  " + str(vs_pop), "NS  " + str(ns_pop)]
    x = np.array([nc_pop, tr_pop, vs_pop, ns_pop])
    fig = plt.figure(figsize=(3, 3))
    fig.patch.set_alpha(0.0)
    plt.subplot(1, 1, 1)
    plt.pie(x, labels=label, colors=colorlist)
    plt.title(
        'Soltech Pop \nAll:{} {}'.format(all_pop, updatetime), fontsize=10)

    plt.savefig(current_dir+'pop.png')
    # ---------Get Population Part END---------#
    # ---------Send Message Part START---------#
    em = discord.Embed(
        title='Event Information',
        description=event_body,
        color=discord.Color.orange(),
    )
    await client.get_guild(344369434103906314).get_channel(387540823551639552).purge(limit=2)
    await client.get_guild(344369434103906314).get_channel(387540823551639552).send(embed=em)
    await client.get_guild(344369434103906314).get_channel(387540823551639552).send(file=discord.File(current_dir+'pop.png'))
    # ---------Send Message Part END---------#
client.run(token)
