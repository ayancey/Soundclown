import requests
from bs4 import BeautifulSoup
import webbrowser
import os
from tinydb import TinyDB, Query


def track_url_to_id(url):
    r = requests.get(url)
    r.raise_for_status()
    return str(r.text.split('soundcloud://sounds:')[1].split('">')[0])

def track_info(id):
    r = requests.get('https://api-v2.soundcloud.com/tracks?urns=soundcloud%3Atracks%3A' + str(id))
    r.raise_for_status()
    return json.loads(r.text)[0]

def downloadable(info):
    if not info['downloadable']:
        return False

    if not info['has_downloads_left']:
        return False

    return True


# requests.post(
#     "https://api.mailgun.net/v3/mg.mykachow.com/messages",
#     auth=("api", "key-708e520b2f3eb75ebeb6d663b8b648f0"),
#     data={"from": "Soundclown Mail Daemon <postmaster@mg.mykachow.com>",
#           "to": "ameanberg@gmail.com",
#           "subject": "Hello",
#           "text": "Testing some Mailgun awesomness!"})

db = TinyDB('db.json')

