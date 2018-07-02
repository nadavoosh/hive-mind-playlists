import logging
import requests
logger = logging.getLogger(__name__)
from track import SpotifyTrack


class SpotifyConnection(object):
    def __init__(self, client_id, client_secret):
        self.token = None
        self.spotify = None

    def refresh_token(self):
        logger.warn('Refreshing Spotify Token')
        auth_url = 'https://accounts.spotify.com'
        r = requests.post(auth_url + '/api/token',
                          data={'grant_type': 'client_credentials'},
                          auth=(self.client_id, self.client_secret)
                          )
        if r.status_code != 200:
            raise Exception(
                'Got status code {} for refresh token: {}'.format(
                    r.status_code, r.text))
        self.token = r.json()['access_token']

    def search_for_track(self, search_term):
        logger.info('Searching for %s', search_term)
        if not self.token:
            self.refresh_token()
        search_url = 'https://api.spotify.com/v1/search'
        params = {
            "type": "track",
            "q": search_term
        }
        headers = {"Authorization": "Bearer {}".format(self.token)}
        r = requests.get(search_url, headers=headers, params=params)
        return r.json()['tracks']['items']

    def get_tracks_from_recommendations(self, recommendations):
        """get one spotify track per recommendation from a list of recommendations
        """
        tracks = []
        for rec in recommendations:
            res = self.search_for_track(rec)
            existing_track_ids = [t.id for t in tracks]
            new_tracks = [song for song in res if song['id']
                          not in existing_track_ids]
            if new_tracks:
                logger.debug('found %s tracks', len(new_tracks))
                track_to_add = SpotifyTrack(new_tracks[0])
                logger.debug('Adding %s to playlist', track_to_add)
                tracks.append(track_to_add)
        return tracks
