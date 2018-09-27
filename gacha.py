import requests
from bs4 import BeautifulSoup
from pony.orm import *
from random import random
import urllib
import os

FATE_MAIN_URL = 'http://fate-go.cirnopedia.org/servant_all.php'
SERVANT_URL_FORMAT = 'http://fate-go.cirnopedia.org/servant_profile.php?servant=%s'
SERVANT_IMAGE_FORMAT = 'http://fate-go.cirnopedia.org/icons/servant_card/%s4.jpg'
SERVANT_RATING_FRAME_FORMAT = 'http://fate-go.cirnopedia.org/icons/frame/servant_card_0%s.png'

SERVANTS_FOLDER = r'C:\Users\Alexander\Desktop\PythonDev\PythonCourse\PythonCourse\servants'

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


load_servants_list()

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

        servant_image = os.path.join(path, 'image.png')
        servant_frame = os.path.join(path, 'frame.png')
        servant_class = os.path.join(path, 'class.png')

        urllib.request.urlretrieve(servant.image, servant_image)
        urllib.request.urlretrieve(servant.image_frame, servant_frame)
        urllib.request.urlretrieve(servant.class_image, servant_class)



load_servants_images()

# with db_session:
#     for servant in Servant.select().order_by(lambda x: random()).limit(10):
#         print(servant.name, servant.image, servant.class_image, servant.image_frame)


