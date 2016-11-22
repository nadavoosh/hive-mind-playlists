import logging
# import spotipy.util as util
import spotipy


logger = logging.getLogger(__name__)

# def build_playlist_from_tracklist(username, track_ids):
#     if token:
#         sp = spotipy.Spotify(auth=token)
#         sp.trace = False
#         results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
#         print results
#     else:
#         print "Can't get token for", username


class Track(object):
    def __init__(self, kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.popularity = kwargs['popularity']
        self.uri = kwargs['uri']
        self.artists = ', '.join([a['name'] for a in kwargs['artists']])

    def __str__(self):
        return '{} - {}'.format(self.name, self.artists)

    def __repr__(self):
        return self.id + self.name + self.artists


def get_tracks_from_recommendations(recommendations):
    sp = spotipy.Spotify()
    tracks = []
    for rec in recommendations:
        logger.info('searching for %s', rec)
        res = sp.search(rec, type='track')['tracks']['items']
        if res:
            tracks.append(Track(res[0]))
    return tracks
