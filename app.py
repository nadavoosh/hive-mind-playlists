
import logging
import re
import requests
from flask import Flask
from flask import request
from flask import render_template
from lib.ask_me.question_model import AskMetafilterQuestion, BASE_ASKME_URL, RANDOM_ASKME_URL, ASKME_URL_PATTERN
from lib.spotify.build_spotify_playlist import get_tracks_from_recommendations, BASE_SPOTIFY_URL


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template('my_form.html')


@app.route('/', methods=['POST'])
def my_form_post():
    _url = request.form['ask_me_url'].lower()

    # check if we were given an ask metafilter question
    url_match = re.match(ASKME_URL_PATTERN, _url)
    if not url_match:
        sample_url = requests.get(RANDOM_ASKME_URL).url
        return render_template('sorry.html', url=_url, sample_url=sample_url)

    q = AskMetafilterQuestion(BASE_ASKME_URL.format(url_match.group(3)))
    tracks = get_tracks_from_recommendations(q.get_recommendations())
    srclink = BASE_SPOTIFY_URL.format(
        title=q.alphanumeric_posttitle,
        tracks=','.join([t.id for t in tracks])
    )
    return render_template('recs.html', items=tracks, question=q, srclink=srclink)


if __name__ == '__main__':
    app.run(debug=True)
