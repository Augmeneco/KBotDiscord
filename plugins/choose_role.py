import plugin
import database
import discord
from discord.ext import commands

from plugins.roles import Roles

class ChooseRole:
    names = ['роль', 'role']
    desc = 'Выбрать роль'
    perm = 256

    role_watcher = {111:0}
    emoji_to_role = {
        '🇿': 'Роль1', 
        '🇴': 'Роль2', 
        '🇻': 'Роль3', 
        '🇷🇺': 'Роль4', 
    }

    async def execute(self, msg):
        embedVar = discord.Embed(title="Выберите себе дополнительные роли, нажав на соответствующие реакции под сообщением:", description="Desc", color=0xFF0000)
        message: discord.Message = await msg.message.channel.send(embed=embedVar)
        
        for key in self.emoji_to_role:
            await message.add_reaction(key)

        self.role_watcher[message.id] = msg.user.id

    async def reaction(self, client: commands.Bot, payload: discord.RawReactionActionEvent, add=True):
        if payload.message_id not in self.role_watcher: return

        guild = client.get_guild(payload.guild_id)
        if guild is None: return

        roles = {}
        for role in guild.roles:
            roles[role.name] = role

        try:
            role_name = self.emoji_to_role[payload.emoji.name]
            role = roles[role_name]
        except KeyError: return

        try:
            if add:
                await payload.member.add_roles(role)
            else:
                member = guild.get_member(payload.user_id)
                if member is None: return
                await member.remove_roles(role)
            
            #await Roles().update_roles(client)

        except discord.HTTPException: pass

        #del self.role_watcher[payload.message_id]

plugin.init_plugin(ChooseRole())
