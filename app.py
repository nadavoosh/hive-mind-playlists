
import logging
from flask import Flask
from flask import request
from flask import render_template
from lib.ask_me.question_model import AskMetafilterQuestion
from lib.spotify.build_spotify_playlist import get_tracks_from_recommendations


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('my_form.html')

@app.route('/', methods=['POST'])
def my_form_post():
    q = AskMetafilterQuestion(request.form['ask_me_url'])
    recs = q.get_recommendations()
    tracks = get_tracks_from_recommendations(recs)
    return render_template('recs.html', items=tracks, question=q)

if __name__ == '__main__':
    app.run()
