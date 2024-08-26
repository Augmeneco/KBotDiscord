import plugin
import database
import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import io
import json

class Progress:
    names = ['прогресс']
    desc = 'Прогресс разработки'
    perm = 1
    font = ImageFont.truetype('data/Roboto-Regular.ttf', 88)
    progress = None
    progress_max = None

    def load_info(self):
        progress = database.db_cur.execute('SELECT * FROM registry WHERE name = "progress"').fetchall()
        if len(progress) == 0:
            self.progress = [0,0,0,0]
            database.db_cur.execute('INSERT INTO registry VALUES (?, ?)', ('progress', json.dumps(self.progress)))
            database.db.commit()
        else:
            self.progress = json.loads(progress[0][1])
            self.progress = [int(i) for i in self.progress]

        progress_max = database.db_cur.execute('SELECT * FROM registry WHERE name = "progress_max"').fetchall()
        if len(progress_max) == 0:
            self.progress_max = [1,1,1,1]
            database.db_cur.execute('INSERT INTO registry VALUES (?, ?)', ('progress_max', json.dumps(self.progress_max)))
            database.db.commit()
        else:
            self.progress_max = json.loads(progress_max[0][1])
            self.progress_max = [int(i) for i in self.progress_max]

    async def execute(self, msg): 
        if self.progress == None or self.progress_max == None:
            self.load_info()

        if len(msg.argv) > 0 and msg.argv[0] == 'готово':
            if msg.user.perm < 256:
                await msg.sendMessage("У вас не достаточно прав для ввода данных")
                return

            self.progress = msg.argv[1:]
            self.progress = [int(i) for i in self.progress]
            database.db_cur.execute('UPDATE registry SET data = ? WHERE name = ?', (json.dumps(self.progress), 'progress'))
            database.db.commit()

        if len(msg.argv) > 0 and msg.argv[0] == 'максимум':
            if msg.user.perm < 256:
                await msg.sendMessage("У вас не достаточно прав для ввода данных")
                return

            self.progress_max = msg.argv[1:]
            self.progress_max = [int(i) for i in self.progress_max]
            database.db_cur.execute('UPDATE registry SET data = ? WHERE name = ?', (json.dumps(self.progress_max), 'progress_max'))
            database.db.commit()

        image = self.draw_image(self.progress)

        with io.BytesIO() as image_binary:
            image.save(image_binary, 'PNG')
            image_binary.seek(0)
            await msg.message.channel.send(file=discord.File(fp=image_binary, filename='image.png'))

    def draw_image(self, progress):
        image = Image.new("RGB", (2000, 1085), (131, 83, 159))
        draw = ImageDraw.Draw(image)

        padding = 48
        boxsize = int((1064-padding*2)/4-10)
        offset_x = padding
        offset_y = padding
        box_colors = [
            (211, 35, 35),
            (88, 96, 219),
            (174, 179, 46),
            (68, 153, 50)
        ]
        text_info = [
            ["Art", self.progress_max[0]], ["Code", self.progress_max[1]], 
            ["Writing", self.progress_max[2]], ["Translation", self.progress_max[3]]
        ]

        font = ImageFont.truetype('data/Roboto-Regular.ttf', 88)

        def get_text_dimensions(text_string, font):
            ascent, descent = font.getmetrics()

            text_width = font.getmask(text_string).getbbox()[2]
            text_height = font.getmask(text_string).getbbox()[3] + descent

            return (text_width, text_height)
        
        #Рисуем градиент в оперативку
        p_image = Image.new("RGB", (1, 2), (0,0,0))
        pixel_map = p_image.load()
        pixel_map[0,0] = (240,211,119)
        pixel_map[0,1] = (191,133,69)

        #Рисуем 4 прямоугольника
        for i in range(4):
            #Основная черная заливка
            draw.rectangle(
                [
                    padding, offset_x, 
                    2000-padding, offset_y+boxsize
                ],
                fill=(0,0,0)
            )

            #Черная рамка
            draw.rectangle(
                [
                    padding+20, offset_x+20,
                    2000-padding-20, offset_y+boxsize-20
                ],
                fill=(131, 83, 159)
            )

            #Черная заливка для будущего прогресса
            draw.rectangle(
                [
                    padding+40, offset_x+40,
                    2000-padding-40, offset_y+boxsize-40
                ],
                fill=(0,0,0)
            )

            #Цветная заливка 
            #Вычисляем процент заливки
            box_length = 2000-88*2
            box_fill_length = int(box_length * progress[i]/text_info[i][1])
            if box_fill_length > box_length: box_fill_length = box_length
            
            #Вставляем градиент прогрессбара

            #Градиент плавный
            p_image = p_image.resize((box_fill_length, 153)) 

            #Градиент с резким переходом
            #p_image = p_image.resize((box_fill_length, 153), Image.Resampling.NEAREST)
            image.paste(p_image, (padding+40, offset_x+40))

            #Рисуем название прогресса
            draw.text(
                (88+20, offset_x+40+20), 
                text_info[i][0], font=font, fill=(255,255,255,255)
            )

            #Рисуем статы прогресса
            text = f"[{int( progress[i] )}/{ text_info[i][1] }] {int( progress[i]/text_info[i][1]*100 )}%"
            text_dim = get_text_dimensions(text, font)

            draw.text(
                (2000-88-20-text_dim[0], offset_x+40+20),
                text, font=font, fill=(255,255,255,255)
            )

            offset_y += 20+boxsize
            offset_x += 20+boxsize

        return image

plugin.init_plugin(Progress())
