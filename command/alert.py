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
    # text2 = [[0 for i in range(30)] for j in range(1500)]
    # text3 = [[0 for i in range(2)] for j in range(2)]
    # html = urllib.request.urlopen('http://ps2.fisu.pw/control/?world=40')
    # soup = BeautifulSoup(html, "html.parser")
    # soup_body = soup.find_all("body")
    # soup2 = []
    # soup3 = []
    # for bd in soup_body:
    #     soup_wrapper = bd.find_all(class_="wrapper")
    #     for j in soup_wrapper:
    #         soup3.append(j.find_all(class_="content"))
    # for i in soup3:
    #     soup.append(i.find('script', type="text/javascript").text)
    # print(soup3)
    # text = soup3
    # text = text.replace('var _population = [', "")
    # text = str(text).split("var _control = ")
    # text1 = text[0].split("},{")
    # for t in text1:
    #     text2[i] = t.split(",")
    # while(1):
    #     if i == len(text2):
    #         break
    #     if str(text2[i][0]).split(":")[0] == '"timestamp"':
    #         text3.append(text2[i])

    # text0 = str(text3[len(text3) - 1]).replace('"',
    #                                            "").replace('[', "").replace(']', "").split(",")
    # text6 = str(text0[1]).split(":")[1].replace("'", "")
    # text7 = str(text0[2]).split(":")[1].replace("'", "")
    # text8 = str(text0[3]).split(":")[1].replace(
    #     "'", "").replace("}", "").replace(";", "")
    # text4 = int(text6) + int(text7) + int(text8)

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
    almessage = "Event Information\n 現在調整中"
    almessage = '\n'
    for i, time in enumerate(event_time):
        if time > now and not("[END]" in event_titles[i]):
            almessage += "{}\n{}\n{}\n"\
                .format(event_titles[i], description[i], time)
            # ---------Event Information part END---------#

    # colorlist = ["b", "red", "purple"]
    # label = ["NC  " + text7, "TR  " + text8, "VS  " + text6]
    # x = np.array([int(text7), int(text8), int(text6)])
    # fig = plt.figure(figsize=(3, 3))
    # fig.patch.set_alpha(0.0)
    # plt.subplot(1, 1, 1)
    # plt.pie(x, labels=label, colors=colorlist)
    # plt.title('Soltech Pop \n(All:' + str(text4) + 'Last Updated' + str(now.hour) +
    #           ':' + str(now.minute) + ':' + str(now.second) + ')', fontsize=10)

    # plt.savefig('pop.png')
    em = discord.Embed(title='Event Information',
                       description=almessage, color=discord.Color.orange())
    await client.get_guild(344369434103906314).get_channel(387540823551639552).purge(limit=2)
    await client.get_guild(344369434103906314).get_channel(387540823551639552).send(embed=em)
    await client.get_guild(344369434103906314).get_channel(387540823551639552).send(file=discord.File('pop.png'))
client.run(token)
