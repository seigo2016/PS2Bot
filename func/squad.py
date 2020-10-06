# coding:utf-8
import discord
import configparser
import os
from discord.ext import commands

current_dir = os.path.dirname(os.path.abspath(__file__))

config = configparser.ConfigParser()
config.read(current_dir + "/../config.ini")
server_id = int(config['Server']['Server_ID'])


class ManageSquad(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.squad_list = {}
        self.mention_message = {}
        self.emoji = {}
        self.emoji_id = {"NC":384317676870303745, "TR": 384317719098425347, "VS": 384317750593585152, "NS": 653944468356988938}
        self.emoji["NC"] = self.bot.get_emoji(self.emoji_id["NC"])
        self.emoji["TR"] = self.bot.get_emoji(self.emoji_id["TR"])
        self.emoji["VS"] = self.bot.get_emoji(self.emoji_id["VS"])
        self.emoji["NS"] = self.bot.get_emoji(self.emoji_id["NS"])
        self.server = self.bot.get_guild(server_id)
        self.role = {}
        self.role["NC"] = self.server.get_role(762872826331136020)
        self.role["TR"] =  self.server.get_role(762873053541433368)
        self.role["VS"] =  self.server.get_role(762873057064648735)
        self.role["NS"] =  self.server.get_role(762874007926079488)


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if "squad-lobby" in str(after.channel):
            vc_ch = await self.server.create_voice_channel("squad", category=after.channel.category)
            text_ch = await self.server.create_text_channel("squad", category=after.channel.category)
            self.squad_list.update({vc_ch.id:{"text_id":text_ch.id, "msg_id":"", "user":member}})
            body = f"{member.mention}\n 小隊が編成されました。\n勢力を選択してください\n"
            await member.move_to(vc_ch)
            text = await text_ch.send(body)
            text_id = text.id
            self.squad_list[vc_ch.id]["msg_id"] = text_id
            for i in self.emoji.values():
                await text.add_reaction(i)

        if before.channel and before.channel.id in self.squad_list:
            if len(before.channel.members) == 0:
                text_ch = self.bot.get_channel(self.squad_list[before.channel.id]["text_id"])
                vc_ch = self.bot.get_channel(before.channel.id)
                self.squad_list.pop(before.channel.id)
                await vc_ch.delete()
                await text_ch.delete()


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        power_emoji = {self.emoji_id["NC"]:"NC", self.emoji_id["TR"]:"TR", self.emoji_id["VS"]: "VS", self.emoji_id["NS"]:"NS"}
        power_color = {"NC":"\U0001F7E6","TR":"\U0001F7E5","VS":"\U0001F7EA", "NS":"\u2B1C"}
        if payload.member == self.bot.user:
            pass
        elif payload.message_id in self.mention_message:
            if payload.emoji.name == "🇾":
                text_ch  = self.bot.get_channel(payload.channel_id)
                mention_role = self.role[self.mention_message[payload.message_id]]
                await text_ch.send(mention_role.mention)
                del self.mention_message[payload.message_id]
            elif payload.emoji.name == "🇳":
                del self.mention_message[payload.message_id]
        else:
            for vc_id, squad in self.squad_list.items():
                if squad["text_id"] == payload.channel_id:
                    user = self.server.get_member(payload.user_id)
                    if payload.user_id != self.bot.user.id and user == squad["user"]:
                        power_name = power_emoji[payload.emoji.id]
                        name = "{}_squad{}".format(power_name, power_color[power_name])
                        vc_ch = self.bot.get_channel(vc_id)
                        text_ch  = self.bot.get_channel(payload.channel_id)
                        await text_ch.edit(name=name)
                        await vc_ch.edit(name=name)
                        mention_text = await text_ch.send("メンションを送りますか？")
                        await mention_text.add_reaction("🇾")
                        await mention_text.add_reaction("🇳")
                        self.mention_message.update({mention_text.id: power_name})
            
                    

def setup(bot):
    bot.add_cog(ManageSquad(bot))