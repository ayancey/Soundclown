import requests
from bs4 import BeautifulSoup
import webbrowser
import os
from tinydb import TinyDB, where
import json


def track_url_to_id(url):
    r = requests.get(url)
    r.raise_for_status()
    return str(r.text.split('soundcloud://sounds:')[1].split('">')[0])

def track_info(id):
    r = requests.get('https://api-v2.soundcloud.com/tracks?urns=soundcloud%3Atracks%3A' + str(id))
    r.raise_for_status()
    r = json.loads(r.text)
    if r:
        return r[0]
    else:
        raise ValueError('Invalid track ID')

def is_downloadable(info):
    if not info['downloadable']:
        return False

    if not info['has_downloads_left']:
        return False

    return True

#print track_url_to_id('https://soundcloud.com/thump/jx-cannon-cowbells-and-airhorns')



db = TinyDB('db.json')
settings = db.get(eid=1)
songs = db.table('songs')



#songs.insert({'id': '231553738', 'downloadable': False, 'emails': ['ameanberg@gmail.com']})

for i in songs.search(where('downloadable') == False):
    print i['id']

    info = track_info(i['id'])
    d = is_downloadable(info)
    d = True

    if d:
        print 'Is now downloadable'
        songs.update({'downloadable': True}, where('id') == i['id'])

        for email in i['emails']:
            print 'Emailing ' + email

            requests.post(
                "https://api.mailgun.net/v3/" + settings['domain'] + "/messages",
                auth=("api", settings['api_key']),
                data={"from": "Soundclown Mail Daemon <postmaster@" + settings['domain'] + ">",
                      "to": email,
                      "subject": info['title'] + " is now downloadable!",
                      "text": info['title'] + ' is now downloadable!',
                      "html": '<a href="' + info['permalink_url'] + '">' + info['title'] + '</a> is now downloadable!'})

    else:
        print 'Still not downloadable'