# coding:utf-8
import discord
import datetime
import requests
from bs4 import BeautifulSoup
import urllib
import dateutil.parser
import pytz
import matplotlib.pyplot as plt
import numpy as np
client = discord.Client()
msg = ""

l = 0
messageid = ""
titles = []
links = []
linksr = []
descriptions = []
json_str = {}
pubdate = []
alltitles = {1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "s", 8: "", 9: ""}


def is_me(m):
    return m.author == client.user


@client.event
async def on_ready():
    text2 = [[0 for i in range(30)] for j in range(1500)]
    text3 = [[0 for i in range(2)] for j in range(2)]
    html = urllib.request.urlopen('http://ps2.fisu.pw/control/?world=40')
    soup = BeautifulSoup(html, "html.parser")
    soup2 = soup.find_all("body")
    a = 0
    for i in soup2:
        soup3 = i.find_all(class_="wrapper")
        a += 1
    a = 0
    for j in soup3:
        soup4 = j.find_all(class_="content")
        a += 1
    a = 0
    for j in soup4:
        soup5 = j.find('script', type="text/javascript").text
        a += 1
    i = 0

    text = soup5
    text = text.replace('var _population = [', "")
    text = str(text).split("var _control = ")
    text1 = text[0].split("},{")
    for t in text1:
        text2[i] = t.split(",")
        i += 1
    i = 0
    while(1):
        if i == len(text2):
            break
        if str(text2[i][0]).split(":")[0] == '"timestamp"':
            text3.append(text2[i])
        i += 1

    text0 = str(text3[len(text3) - 1]).replace('"',
                                               "").replace('[', "").replace(']', "").split(",")
    text6 = str(text0[1]).split(":")[1].replace("'", "")
    text7 = str(text0[2]).split(":")[1].replace("'", "")
    text8 = str(text0[3]).split(":")[1].replace(
        "'", "").replace("}", "").replace(";", "")
    text4 = int(text6) + int(text7) + int(text8)

    alerturl = "http://ps2.fisu.pw/alert/rss"
    alertret = ""
    alertret = requests.get(alerturl)
    alerttitles = ["" for i in range(100)]
    legion = ["" for i in range(100)]
    description = ["" for i in range(100)]
    pubdate = ["" for i in range(100)]
    alerttime = ["" for i in range(100)]
    now = datetime.datetime.now()
    alertsoup = BeautifulSoup(alertret.content, "html.parser")
    i = 0
    for alertitem in alertsoup.find_all("item"):
        alerttitles[i] = (alertitem.find("title").string)
        legion[i] = (alertitem.find("fisupw:starter_faction").string)
        description[i] = (alertitem.find("description").string)
        pubdate[i] = (alertitem.find("pubdate").string)
        i += 1
    m = 0
    jst = pytz.timezone('Asia/Tokyo')
    now = jst.localize(now)
    while(m != 5):
        alerttime[m] = dateutil.parser.parse(pubdate[m])
        alerttime[m] = alerttime[m].astimezone(pytz.timezone('Asia/Tokyo'))
        alerttime[m] = alerttime[m] + datetime.timedelta(minutes=45)
        alltitles[m] = alerttitles[m].split()
        m += 1
    a = 0
    s = 0
    now = datetime.datetime.now(jst)
    almessage = "Event Information\n"
    almessage = '\n'
    if alerttime[0] > now or alerttime[1] > now or alerttime[2] > now:
        if len(alltitles[0]) == 3 or len(alltitles[1]) == 3 or len(alltitles[2]) == 3:
            while(1):
                if (alerttime[a] > now) is True and len(alltitles[a]) == 3:
                    alerttime[a] = alerttime[a] - \
                        datetime.timedelta(minutes=30)
                    almessage += '\n--------------------\n'
                    almessage += '**' + legion[a] + '**'
                    almessage += '\n'
                    almessage += alerttitles[a]
                    almessage += '\n'
                    almessage += description[a]
                    almessage += '\n'
                    almessage += str(alerttime[a])
                else:
                    s += 1
                if a == 4:
                    break
                a += 1
        else:
            almessage = "alert is none"
    else:
        almessage = "alert is none"
    if s == 5:
        almessage = "alert is none"
    if not almessage or almessage == "":
        almessage = "alert is none"

    colorlist = ["b", "red", "purple"]
    label = ["NC  " + text7, "TR  " + text8, "VS  " + text6]
    x = np.array([int(text7), int(text8), int(text6)])
    fig = plt.figure(figsize=(3, 3))
    fig.patch.set_alpha(0.0)
    plt.subplot(1, 1, 1)
    plt.pie(x, labels=label, colors=colorlist)
    plt.title('Soltech Pop \n(All:' + str(text4) + 'Last Updated' + str(now.hour) +
              ':' + str(now.minute) + ':' + str(now.second) + ')', fontsize=10)

    plt.savefig('pop.png')
    em = discord.Embed(title='Alert Information',
                       description=almessage, color=discord.Color.orange())
    await client.get_guild(344369434103906314).get_channel(387540823551639552).purge(limit=2)
    await client.get_guild(344369434103906314).get_channel(387540823551639552).send(embed=em)
    await client.get_guild(344369434103906314).get_channel(387540823551639552).send(file=discord.File('pop.png'))
client.run(token)
