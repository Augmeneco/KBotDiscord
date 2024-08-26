from config import config

import database
import plugin

import json
import requests
import re
import discord
from discord.ext import commands

class Msg:
    text: str = ""
    user_text: str
    chat_id: int
    msg_id: int
    from_id: int
    user: database.User
    username: str = None
    reply_id: int = None
    reply_msg = None
    attachments: list
    real_name: str
    skip: bool = False
    command: str = ""
    argv: list
    is_command: bool = False
    has_prefix: bool = False

    message: discord.Message = None
    client: commands.Bot = None

    is_cmd_regex = re.compile(f'^/?\\s?(?P<bot_name>{"|".join(config.names)})?\\s?', re.IGNORECASE)

    def parse_msg(self, update: discord.Message):
        self.text = update.clean_content
        self.chat_id = update.channel.id
        self.msg_id = update.id
        self.from_id = update.author.id
        self.user = database.users.get(self.from_id)
        self.username = update.author.name
        self.real_name = update.author.global_name
        self.attachments = update.attachments
        self.message = update

    def parse_command(self):
        self.is_cmd_regex = re.compile(f'^/?!?\\s?(?P<bot_name>{"|".join(config.names)})?\\s?', re.IGNORECASE)

        if self.is_cmd_regex.search(self.text).group(0) == '': return
        self.has_prefix = True
        
        argv = []
        argv = self.is_cmd_regex.sub('', self.text).split(' ')
        command = argv[0].lower()

        if command not in plugin.plugins_map:
            self.argv = argv
            self.user_text = ' '.join(argv)
            return
        del argv[0]

        self.command = command
        self.is_command = True
        self.argv = argv
        self.user_text = ' '.join(argv)

    async def sendMessage(self, text, **parameters):
        await self.message.channel.send(text, reference=self.message, **parameters)

