import configparser
import os

import dill
from discord.ext import commands


class ManageSquad(commands.Cog):
    # State constants
    STATE_FACTION_SELECTION = "faction_selection"
    STATE_SERVER_SELECTION = "server_selection"
    STATE_COMPLETED = "completed"

    def __init__(self, bot, env):
        self.env = env
        self.bot = bot
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        config = configparser.ConfigParser()
        if env == "dev":
            config.read(self.current_dir + "/../config-dev.ini")
        else:
            config.read(self.current_dir + "/../config.ini")
        self.server_id = int(config["Server"]["Server_ID"])
        self.channel_id = int(config["Channel"]["Squad_Role_Channel_ID"])
        self.role_message_id = int(config["Message"]["Squad_Role_Message_ID"])

    @commands.Cog.listener()
    async def on_ready(self):
        self.squad_status_bin = self.current_dir + "/../data/squad_status.dill"
        self.server = self.bot.get_guild(self.server_id)
        self.squad_list = {}
        if os.path.isfile(self.squad_status_bin):
            with open(self.squad_status_bin, "rb") as d:
                self.squad_list = dill.load(d)
        self.mention_message = {}
        self.emoji = {}
        self.emoji_id = {
            "NC": 384317676870303745,
            "TR": 384317719098425347,
            "VS": 384317750593585152,
            "NS": 653944468356988938,
        }
        self.emoji["NC"] = self.bot.get_emoji(self.emoji_id["NC"])
        self.emoji["TR"] = self.bot.get_emoji(self.emoji_id["TR"])
        self.emoji["VS"] = self.bot.get_emoji(self.emoji_id["VS"])
        self.emoji["NS"] = self.bot.get_emoji(self.emoji_id["NS"])
        # Server selection emojis (using Unicode emojis)
        self.server_emoji = {"1️⃣": "Soltech", "2️⃣": "Osprey", "3️⃣": "Wainwright"}
        self.role = {}
        self.role["NC"] = self.server.get_role(762872826331136020)
        self.role["TR"] = self.server.get_role(762873053541433368)
        self.role["VS"] = self.server.get_role(762873057064648735)
        self.role["NS"] = self.server.get_role(762874007926079488)
        if self.env == "prod":
            channel = self.bot.get_guild(self.server_id).get_channel(self.channel_id)
            self.role_message = await channel.fetch_message(self.role_message_id)
            for i in self.emoji.values():
                await self.role_message.add_reaction(i)

    async def _update_channels_name(self, vc_id, text_id, name):
        """Helper method to update both voice and text channel names"""
        vc_ch = self.bot.get_channel(vc_id)
        text_ch = self.bot.get_channel(text_id)
        await text_ch.edit(name=name)
        await vc_ch.edit(name=name)

    async def _setup_server_selection(self, text_ch):
        """Helper method to setup server selection message and reactions"""
        await text_ch.send("サーバーを選択してください\n1️⃣: Soltech\n2️⃣: Osprey\n3️⃣: Wainwright")
        server_message = await text_ch.fetch_message(text_ch.last_message_id)
        for emoji in self.server_emoji.keys():
            await server_message.add_reaction(emoji)
        return server_message.id

    async def _setup_mention_selection(self, text_ch, faction):
        """Helper method to setup mention selection message and reactions"""
        mention_text = await text_ch.send("メンションを送りますか？")
        await mention_text.add_reaction("🇾")
        await mention_text.add_reaction("🇳")
        self.mention_message.update({mention_text.id: faction})

    async def _handle_faction_selection(self, vc_id, payload, power_emoji):
        """Handle faction selection logic"""
        power_name = power_emoji[payload.emoji.id]

        # Update squad info with selected faction
        self.squad_list[vc_id]["faction"] = power_name
        self.squad_list[vc_id]["state"] = self.STATE_SERVER_SELECTION

        text_ch = self.bot.get_channel(payload.channel_id)
        server_msg_id = await self._setup_server_selection(text_ch)

        # Update message ID to track server selection message
        self.squad_list[vc_id]["server_msg_id"] = server_msg_id

    async def _handle_server_selection(self, vc_id, payload, power_color):
        """Handle server selection logic"""
        server_name = self.server_emoji[payload.emoji.name]
        faction = self.squad_list[vc_id]["faction"]
        power_color_emoji = power_color[faction]

        # Update squad info with selected server
        self.squad_list[vc_id]["server"] = server_name
        self.squad_list[vc_id]["state"] = self.STATE_COMPLETED

        # Create final channel name with faction and server
        name = f"{faction}_{server_name}_squad{power_color_emoji}"
        await self._update_channels_name(vc_id, payload.channel_id, name)

        # Ask about mention functionality
        text_ch = self.bot.get_channel(payload.channel_id)
        await self._setup_mention_selection(text_ch, faction)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if "squad-lobby" in str(after.channel):
            vc_ch = await self.server.create_voice_channel("squad", category=after.channel.category)
            text_ch = await self.server.create_text_channel("squad", category=after.channel.category)
            self.squad_list.update(
                {
                    vc_ch.id: {
                        "text_id": text_ch.id,
                        "msg_id": "",
                        "user_id": member.id,
                        "state": self.STATE_FACTION_SELECTION,
                        "faction": "",
                        "server": "",
                    }
                }
            )
            body = f"{member.mention}\n 小隊が編成されました。\n勢力を選択してください\n"
            await member.move_to(vc_ch)
            text = await text_ch.send(body)
            text_id = text.id
            self.squad_list[vc_ch.id]["msg_id"] = text_id
            for i in self.emoji.values():
                await text.add_reaction(i)
            with open(self.squad_status_bin, "wb") as d:
                dill.dump(self.squad_list, d)

        if before.channel is not None and before.channel.id in self.squad_list:
            if len(before.channel.members) == 0:
                text_ch = self.bot.get_channel(self.squad_list[before.channel.id]["text_id"])
                vc_ch = self.bot.get_channel(before.channel.id)
                self.squad_list.pop(before.channel.id)
                await vc_ch.delete()
                await text_ch.delete()
            with open(self.squad_status_bin, "wb") as d:
                dill.dump(self.squad_list, d)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        power_emoji = {
            self.emoji_id["NC"]: "NC",
            self.emoji_id["TR"]: "TR",
            self.emoji_id["VS"]: "VS",
            self.emoji_id["NS"]: "NS",
        }
        power_color = {"NC": "\U0001f7e6", "TR": "\U0001f7e5", "VS": "\U0001f7ea", "NS": "\u2b1c"}
        if payload.member.bot:
            pass
        elif payload.message_id == self.role_message_id:
            if payload.emoji.id in power_emoji:
                squad_role_ch = self.bot.get_channel(payload.channel_id)
                select_emoji = power_emoji[payload.emoji.id]
                select_role = self.role[select_emoji]
                if select_role in payload.member.roles:
                    await payload.member.remove_roles(select_role)
                    body = (
                        f"`{payload.member}` さんの  `{select_role}` 役職を削除しました \n"
                        "(このメッセージは一定時間で消去されます)"
                    )
                else:
                    await payload.member.add_roles(select_role)
                    body = (
                        f"`{payload.member}` さんに  `{select_role}` 役職を追加しました \n"
                        "(このメッセージは一定時間で消去されます)"
                    )
                await squad_role_ch.send(body, delete_after=20)
                await self.role_message.remove_reaction(payload.emoji, payload.member)
        elif payload.message_id in self.mention_message:
            if payload.emoji.name == "🇾":
                text_ch = self.bot.get_channel(payload.channel_id)
                mention_role = self.role[self.mention_message[payload.message_id]]
                await text_ch.send(mention_role.mention)
                del self.mention_message[payload.message_id]
            elif payload.emoji.name == "🇳":
                del self.mention_message[payload.message_id]
        else:
            for vc_id, squad in self.squad_list.items():
                if squad["text_id"] == payload.channel_id:
                    user = self.server.get_member(payload.user_id)
                    if user.id == squad["user_id"]:
                        # Handle faction selection
                        if squad["state"] == self.STATE_FACTION_SELECTION and payload.emoji.id in power_emoji:
                            await self._handle_faction_selection(vc_id, payload, power_emoji)

                        # Handle server selection
                        elif squad["state"] == self.STATE_SERVER_SELECTION and payload.emoji.name in self.server_emoji:
                            await self._handle_server_selection(vc_id, payload, power_color)

                        # Save updated squad list
                        with open(self.squad_status_bin, "wb") as d:
                            dill.dump(self.squad_list, d)


def setup(bot, env):
    bot.add_cog(ManageSquad(bot, env))
