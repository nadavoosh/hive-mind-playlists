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
        self.artists = ', '.join([a['name'].encode(
            'ascii', 'ignore').decode('ascii') for a in kwargs['artists']])

    def __str__(self):
        return '{} - {}'.format(self.name, self.artists)

    def __repr__(self):
        return self.id + self.name + self.artists


def get_tracks_from_recommendations(recommendations):
    """get one spotify track per recommendation from a list of recommendations
    """
    sp = spotipy.Spotify()
    tracks = []
    for rec in recommendations:
        logger.info('searching spotify for %s', rec)
        res = sp.search(rec, type='track')['tracks']['items']
        existing_track_ids = [t.id for t in tracks]
        new_tracks = [song for song in res if song['id']
                      not in existing_track_ids]
        if new_tracks:
            logger.info('found %s tracks', len(new_tracks))
            track_to_add = Track(new_tracks[0])
            logger.info('Adding %s to playlist', track_to_add)
            tracks.append(track_to_add)
    return tracks
