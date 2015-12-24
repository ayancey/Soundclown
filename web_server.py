import requests
from bs4 import BeautifulSoup
import webbrowser
import codecs
import json
from flask import Flask, render_template, request, Response
import os
from check_tracks import *
from tinydb import TinyDB, where

app = Flask(__name__)
app.debug = True

db = TinyDB('db.json')
songs = db.table('songs')


@app.route('/')
def index():
    return render_template('index.html', tracks=len(songs))


@app.route('/submit')
def submit():
    id = track_url_to_id(request.args.get('url'))

    info = track_info(id)
    d = is_downloadable(info)

    if d:
        return 'Track is already downloadable!'
    else:
        if songs.search(where('id') == id):
            emails = songs.search(where('id') == id)[0]['emails']
            if request.args.get('email') in emails:
                return 'You are already receiving emails about this track!'
            else:
                return 'Adding your email...'

        songs.insert({'id': id, 'downloadable': False, 'emails': [request.args.get('email')]})
        return 'Done.'

    return 'Track has been added to database.'

app.run(host='0.0.0.0', port=1337, threaded=True)
