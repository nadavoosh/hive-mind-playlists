import logging

logger = logging.getLogger(__name__)


class SpotifyTrack(object):
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
