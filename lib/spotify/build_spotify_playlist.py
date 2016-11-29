import logging
import spotipy

logger = logging.getLogger(__name__)


BASE_SPOTIFY_URL = "https://embed.spotify.com/?uri=spotify:trackset:{title}:{tracks}"

class Track(object):
    def __init__(self, kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name'].encode('ascii', 'ignore').decode('ascii')
        self.popularity = kwargs['popularity']
        self.uri = kwargs['uri'].encode('ascii', 'ignore').decode('ascii')
        self.artists = ', '.join([a['name'].encode('ascii', 'ignore').decode('ascii') for a in kwargs['artists']])

    def __str__(self):
        return '{} - {}'.format(self.name, self.artists)

    def __repr__(self):
        return self.id + self.name + self.artists


def filter_search_terms(search_term):
    """Spotify API doesn't seem to like it when you search for a logical term
    see https://github.com/spotify/web-api/issues/368
    """
    badwords = ['not', 'and', 'or', 'if']
    return [word for word in search_term if word.lower() not in badwords]


def get_tracks_from_recommendations(recommendations):
    """get one spotify track per recommendation from a list of recommendations
    """
    sp = spotipy.Spotify()
    tracks = []
    for rec in recommendations:
        rec = filter_search_terms(rec)
        logger.info('searching for %s', rec)
        res = sp.search(rec, type='track')['tracks']['items']
        if res:
            tracks.append(Track(res[0]))
    return tracks
