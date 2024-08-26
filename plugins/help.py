import plugin as plugins
from config import config

class Help:
    names = ['помощь', 'help', 'хелп']
    desc = 'Помощь по командам бота'
    perm = 1

    async def execute(self, msg):
        out = '[ Помощь ]\n'
        
        for plugin in plugins.plugins_list:
            if msg.user.perm >= plugin.perm:
                out += f'• {config.names[0]} {plugin.names[0]} - {plugin.desc}\n'

        await msg.sendMessage(out) 

plugins.init_plugin(Help())