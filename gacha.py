import requests
from bs4 import BeautifulSoup
from pony.orm import *
from random import random
import urllib
import os
from PIL import Image

from settings import SERVANTS_FOLDER


FATE_MAIN_URL = 'http://fate-go.cirnopedia.org/servant_all.php'
SERVANT_URL_FORMAT = 'http://fate-go.cirnopedia.org/servant_profile.php?servant=%s'
SERVANT_IMAGE_FORMAT = 'http://fate-go.cirnopedia.org/icons/servant_card/%s4.jpg'
SERVANT_RATING_FRAME_FORMAT = 'http://fate-go.cirnopedia.org/icons/frame/servant_card_0%s.png'

FATE_CE_URL = 'http://fate-go.cirnopedia.org/craft_essence.php'
CE_URL_FORMAT = "http://fate-go.cirnopedia.org/craft_essence_profile.php?essence=%s"
CE_IMAGE_FORMAT = "http://fate-go.cirnopedia.org/icons/essence/craft_essence_%s.jpg"
CE_RATING_FRAME_FORMAT = "http://fate-go.cirnopedia.org/icons/frame/essence_card_0%d.png"


db = Database('sqlite', ':memory:')

class Servant(db.Entity):
    id = PrimaryKey(str)
    name = Required(str)
    stars = Required(int)
    cls = Required(str)

    @property
    def url(self):
        return SERVANT_URL_FORMAT % self.id

    @property
    def image(self):
        return SERVANT_IMAGE_FORMAT % self.id

    @property
    def image_frame(self):
        return SERVANT_RATING_FRAME_FORMAT % self.stars

    @property
    def class_image(self):
        return 'http://fate-go.cirnopedia.org/%s' % self.cls

class CraftEssence(db.Entity):
    id = PrimaryKey(str)
    name = Required(str)
    stars = Required(int)

    @property
    def url(self):
        return CE_URL_FORMAT % self.id

    @property
    def image(self):
        return CE_IMAGE_FORMAT % self.id

    @property
    def image_frame(self):
        return CE_RATING_FRAME_FORMAT % self.id

db.generate_mapping(create_tables=True)

class CirnopediaConnectionError(Exception):
    pass

@db_session
def load_servants_list():
    response = requests.get(FATE_MAIN_URL)
    if response.status_code != 200:
        raise CirnopediaConnectionError

    html = response.text
    tree = BeautifulSoup(html, 'lxml')  # may require to `pip install lxml`
    servants_data = tree.find('tbody')
    for x in servants_data.find_all('tr'):
        name = x.contents[4].contents[0].contents[2]
        id = x.attrs['id']
        stars = x.contents[2].contents[0][0]
        class_image_str = x.contents[3].contents[0].contents[1].attrs['style']
        st = 'icons/class/'
        end = '.png'
        start_pos = class_image_str.find(st)
        class_image_str = class_image_str[start_pos:]
        end_pos = class_image_str.find(end)
        class_image = class_image_str[:end_pos + len(end)]
        Servant(id=id, name=name, stars=stars, cls=class_image)


@db_session
def load_servants_images():
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)
    for servant in Servant.select().limit(10, offset=3):
        path = os.path.join(SERVANTS_FOLDER, servant.id)
        if not os.path.exists(path):
            os.makedirs(path)

        servant_art = os.path.join(path, 'art.png')
        servant_image = os.path.join(path, 'image.png')
        servant_frame = os.path.join(path, 'frame.png')
        servant_class = os.path.join(path, 'class.png')

        urllib.request.urlretrieve(servant.image, servant_art)
        urllib.request.urlretrieve(servant.image_frame, servant_frame)
        urllib.request.urlretrieve(servant.class_image, servant_class)

        img = Image.open(servant_art).convert("RGBA")
        frame = Image.open(servant_frame).convert("RGBA")
        out = Image.new('RGBA', (512, 874), color=255)
        class_i = Image.open(servant_class).convert("RGBA")
        x, y = out.size
        out.paste(img, (0, 30), img)
        out.paste(frame, (0, 0, x, y), frame)
        out.paste(class_i, (217, 770), class_i)
        out.save(servant_image, format="png")

        os.remove(servant_art)
        os.remove(servant_frame)
        os.remove(servant_class)


@db_session
def load_ce_list():
    response = requests.get(FATE_CE_URL)
    if response.status_code != 200:
        raise CirnopediaConnectionError

    html = response.text
    tree = BeautifulSoup(html, 'lxml')  # may require to `pip install lxml`
    ce_data = tree.find_all('tbody')[1]
    for x in ce_data.find_all('tr'):
        stars = int(x.contents[3].contents[0][:1])
        id = x.contents[1].contents[0]
        name = x.contents[7].contents[0].attrs['title']
        CraftEssence(id=id, name=name, stars=stars)

# load_servants_images()
# load_servants_list()
# load_ce_list()

# with db_session:
#     CraftEssence.select().show()

"""
Домашнее задание
1. Склеить картинки для эссенций
2. Добавить к сущностям БД описания
3. Добавить к сущностям флаги загруженности
4. Добавить флаги возможности выдачи в story гаче (для слуг и СЕ)
5. Убрать невозможных сервантов

"""



