import requests
from bs4 import BeautifulSoup
import webbrowser
import codecs
import json
from flask import Flask, render_template, request, Response
import os

app = Flask(__name__)
app.debug = True

def track_url_to_id(url):
    r = requests.get(url)
    r.raise_for_status()
    return str(r.text.split('soundcloud://sounds:')[1].split('">')[0])

def track_is_downloadable(id):
    r = requests.get('https://api-v2.soundcloud.com/tracks?urns=soundcloud%3Atracks%3A' + id)
    r.raise_for_status()
    return json.loads(r.text)[0]['downloadable']


@app.route('/')
def index():
    track_ids = []

    if os.path.isfile('ids.json'):
        with open('ids.json') as f:
           track_ids = json.loads(f.read())
    return render_template('index.html', tracks=len(track_ids))

@app.route('/submit')
def submit():
    track_ids = []

    if os.path.isfile('ids.json'):
        with open('ids.json') as f:
           track_ids = json.loads(f.read())

    id = track_url_to_id(request.args.get('url'))
    if id in track_ids:
        return 'Track already in database!'

    downloadable = track_is_downloadable(id)
    if downloadable:
        return 'Track already downloadable!'

    track_ids.append(id)
    with open('ids.json', 'w') as f:
        f.write(json.dumps(track_ids))

    return 'Track has been added to database.'

app.run(host='0.0.0.0', port=1337, threaded=True)


# requests.post(
#     "https://api.mailgun.net/v3/sandbox814fb387f48c4effa5bdba4e88793789.mailgun.org/messages",
#     auth=("api", "key-708e520b2f3eb75ebeb6d663b8b648f0"),
#     data={"from": "Soundclown <postmaster@mg.mykachow.com>",
#           "to": "Alex Yancey <alexyancey3@gmail.com>",
#           "subject": 'New track is now downloadable',
#           "text": 'blank is now downloadable'})
