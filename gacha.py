import requests
from bs4 import BeautifulSoup
from pony.orm import *

FATE_MAIN_URL = 'http://fate-go.cirnopedia.org/servant_all.php'
SERVANT_URL_FORMAT = 'http://fate-go.cirnopedia.org/servant_profile.php?servant=%s'
SERVANT_IMAGE_FORMAT = 'http://fate-go.cirnopedia.org/icons/servant_card/%s1.jpg'
SERVANT_RATING_FRAME_FORMAT = 'http://fate-go.cirnopedia.org/icons/frame/servant_card_0%d.png'

db = Database('sqlite', ':memory:')


class Servant(db.Entity):
    id = PrimaryKey(str)
    name = Required(str)

    @property
    def url(self):
        return SERVANT_URL_FORMAT % self.id

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
        Servant(id=id, name=name)


load_servants_list()


with db_session:
    Servant.select().limit(10).show()


