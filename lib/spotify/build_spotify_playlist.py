import logging
# import spotipy.util as util
import spotipy


logger = logging.getLogger(__name__)
# birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
# spotify = spotipy.Spotify()

# def build_playlist_from_tracklist(username, track_ids):
#     if token:
#         sp = spotipy.Spotify(auth=token)
#         sp.trace = False
#         results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
#         print results
#     else:
#         print "Can't get token for", username


def filter_spotify_result(item):
    logger.info(([a['name'] for a in item['artists']]))
    return {
        'id': item.get('id'),
        'name': item.get('name'),
        'popularity': item.get('popularity'),
        # 'artist': item.get('artist'),
    }


def get_tracks_from_recommendations(recommendations):
    sp = spotipy.Spotify()
    tracks = []
    for rec in recommendations:
        res = sp.search(rec, type='track')
        logger.info('searching for %s', rec)
        logger.info([filter_spotify_result(item) for item in res['tracks']['items'][:3]]
                   )
        # tracks.append(res[0])
    return tracks


if __name__ == '__main__':
    # recs = get_recommendations('http://ask.metafilter.com/297135/Finger-Picken')
    recs = [
        'Robert Rich',
        'You Popol Vuh',
        'Have Alice Coltrane',
        'Andrew Bird',
        'Tony Scott',
        'Moby just did a thing.',
        'What We Left Behind',
        'Robert Rich - Somnium',
        'Liquid Mind',
        'Steve Roach',
        'Popol Vuh - Hosianna Mantra',
        'Journey in Satchidananda',
        'Useless Creatures',
        "here's my favorite track from it",
        '"Music for Zen Meditation"'
    ]

    print get_tracks_from_recommendations(recs)
