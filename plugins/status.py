import psutil
import plugin
import re
import subprocess
import os

class Status:
	names = ['стат','статус','stat','status']
	desc = 'Информация о сервере'
	perm = 1

	async def execute(self, msg):
		counter = 1
		text = '[ Статистика ]\nСистема:\n  Процессор:\n'

		for idx, cpu in enumerate(psutil.cpu_percent(interval=1, percpu=True)):
			if counter == 1:
				text += '    #'+str(idx+1)+': '+str(round(cpu,1))+'%'
				counter = 2
			elif counter == 2:
				if len(str(idx+1)) < 3: text += ' '
				text += ' | #'+str(idx+1)+': '+str(round(cpu,1))+'%\n'
				counter = 1

		mem = psutil.virtual_memory()
		MB = 1024 * 1024

		text += '\n  ОЗУ:\n    Всего: '+str(int(mem.total / MB))+'MB\n'
		text += '    Использовано: '+str(int((mem.total - mem.available) / MB))+'MB\n'
		text += '    Свободно: '+str(int(mem.available / MB))+'MB\n'
		text += '    Использовано ботом: '+str(int(psutil.Process().memory_info().rss / MB))+'MB\n\n'

		if os.path.exists('/usr/bin/nvidia-smi'):
			vram = subprocess.run('nvidia-smi', shell=True, capture_output=True).stdout.decode()
			vram = re.findall('W\s.+?(\d+).+?(\d+)', vram)[0]

			text += f'  Видеопамять:\n    Всего: {vram[1]} MB\n'
			text += f'    Использовано: {vram[0]} MB\n'
			text += f'    Свободно: {int(vram[1])-int(vram[0])} MB\n'

		await msg.sendMessage(text)

plugin.init_plugin(Status())
