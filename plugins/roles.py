import database
import discord
from discord.ext import commands
import asyncio

class Roles:
    guild: discord.Guild = None
    online_channel = None

    async def daemon(self, client: commands.Bot):
        while True:
            await self.update_roles(client)
            await asyncio.sleep(30)

    async def update_roles(self, client: commands.Bot):
        if self.guild == None:
            self.guild = client.get_guild(662479827147816964)

        #Онлайн
        count = 0

        for member in self.guild.members:
            if member.bot: continue
            if member.status == discord.Status.online: 
                count += 1

        try:
            if self.online_channel == None:
                self.online_channel = self.guild.get_channel(1274457561164419206)        
            name = f"Онлайн: {count}"
            if self.online_channel.name != name:
                await self.online_channel.edit(name=f"Онлайн: {count}")
        except: pass

        #Уровни пользователей
        ids = [
            [662479827881951245, "Уровень 1", "Роль1", 0],
            [1274433640629272727, "Уровень 2", "Роль2", 0],
            [1274433980019511408, "Уровень 3", "Роль3", 0],
            [1274441801025065052, "Уровень 4", "Роль4", 0]
        ]

        members = client.get_all_members()
        for member in members:
            if member.bot: continue
            member_roles = member.roles

            for id in ids:
                for role in member_roles:
                    if id[2] == role.name:
                        id[3] += 1

        for id in ids:
            try:
                if id[4] == None:
                    id[4] = self.guild.get_channel(id[0])
                channel = id[4]
                name = f"{id[1]} {id[3]}"
                if channel.name != name:
                    await channel.edit(name=name)
            except: pass
