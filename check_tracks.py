import requests
from bs4 import BeautifulSoup
import webbrowser
import codecs
import json
import os


def track_url_to_id(url):
    r = requests.get(url)
    r.raise_for_status()
    return str(r.text.split('soundcloud://sounds:')[1].split('">')[0])

def track_info(id):
    r = requests.get('https://api-v2.soundcloud.com/tracks?urns=soundcloud%3Atracks%3A' + id)
    r.raise_for_status()
    return json.loads(r.text)[0]

track_ids = []

if os.path.isfile('ids.json'):
    with open('ids.json') as f:
       track_ids = json.loads(f.read())

for id in track_ids:
    print id
    i = track_info(id)
    d = i['downloadable']
    print i['title']

    if d:
        print 'New track downloadable'

        requests.post(
            "https://api.mailgun.net/v3/sandbox814fb387f48c4effa5bdba4e88793789.mailgun.org/messages",
            auth=("api", "key-708e520b2f3eb75ebeb6d663b8b648f0"),
            data={"from": "Soundclown <postmaster@mg.mykachow.com>",
                  "to": "Alex Meanberg <ameanberg@gmail.som>",
                  "subject": 'New track is now downloadable',
                  "text": i['permalink_url'] + ' is now downloadable'})

        requests.post(
            "https://api.mailgun.net/v3/sandbox814fb387f48c4effa5bdba4e88793789.mailgun.org/messages",
            auth=("api", "key-708e520b2f3eb75ebeb6d663b8b648f0"),
            data={"from": "Soundclown <postmaster@mg.mykachow.com>",
                  "to": "   Ellis Hammond-Pereira <ellis_hp@me.com>",
                  "subject": 'New track is now downloadable',
                  "text": i['permalink_url'] + ' is now downloadable'})

        track_ids.remove(id)
        with open('ids.json', 'w') as f:
            f.write(json.dumps(track_ids))
