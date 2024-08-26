import discord
from discord.ext import commands

from config import config
import utils
import plugin

from plugins.roles import Roles
from plugins.userinfo import UserEvent

import asyncio
import traceback

class KBot(commands.Bot):
    async def on_ready(self):
        print('Logged on as', self.user)

        asyncio.create_task(Roles().daemon(self))

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
        
        msg = utils.Msg()
        msg.parse_msg(message)
        msg.client = self
        msg.parse_command()
        
        if msg.skip: return
        if msg.is_command:
            if msg.user.perm < plugin.plugins_map[msg.command].perm:
                await msg.sendMessage("У вас не достаточно прав для этой команды")
                return
            
            await plugin.plugins_map[msg.command].execute(msg)

        await UserEvent().execute(msg)

        await message.delete()

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        await plugin.plugins_map["роль"].reaction(self, payload)

    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        await plugin.plugins_map["роль"].reaction(self, payload, add=False)
        
intents = discord.Intents.all()

client = KBot(command_prefix="", intents=intents)
client.run(config.discord_token)