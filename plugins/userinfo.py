import plugin
import database
import discord
from discord.ext import commands
import asyncio

class Me:
    names = ['я']
    desc = 'Моя информация'
    perm = 1

    async def execute(self, msg): 
        out = '[ Информация ]\n'
        out += f'• Имя - {msg.real_name}\n'
        out += f'• Уровень - {msg.user.level}\n'
        out += f'• Кол-во сообщений - {msg.user.counter}\n'
        out += f'• Права - {msg.user.perm}\n'
        
        await msg.sendMessage(out)

class UserEvent:
    roles = {
        'Роль2': 2,
        'Роль3': 3,
        'Роль4': 4,
    }
    guild_roles = None

    async def execute(self, msg):
        msg.user.counter += 1
        old_level = msg.user.level
        
        if msg.user.counter > 20: msg.user.level = 2
        if msg.user.counter > 22: msg.user.level = 3
        if msg.user.counter > 25: msg.user.level = 4

        if msg.user.level > old_level:
            await msg.sendMessage(f'Пользователь <@{msg.from_id}> получает уровень {msg.user.level}!')

            message: discord.Message = msg.message

            if self.guild_roles == None:
                self.guild_roles = message.guild.roles

            for role in self.guild_roles:
                if role.name in self.roles and self.roles[role.name] == msg.user.level:
                    await message.author.add_roles(role)
                    #Старые роли не пропадут от нижних лвлов!
                    break

        msg.user.update()

        
plugin.init_plugin(Me())