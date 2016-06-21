import pprint
# import spotipy.util as util
import spotipy
from lib.find_reccomended_songs import get_recommendations

# birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
# spotify = spotipy.Spotify()

pp = pprint.PrettyPrinter(indent=4)

# def build_playlist_from_tracklist(username, track_ids):
#     if token:
#         sp = spotipy.Spotify(auth=token)
#         sp.trace = False
#         results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
#         print results
#     else:
#         print "Can't get token for", username


def filter_spotify_result(item):
    pp.pprint([a['name'] for a in item['artists']])
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
        print 'searching for {}'.format(rec)
        pp.pprint([filter_spotify_result(item) for item in res['tracks']['items'][:3]])
        print '============='
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
        u'Robert Rich - Somnium',
        'Liquid Mind',
        'Steve Roach',
        u'Popol Vuh - Hosianna Mantra',
        'Journey in Satchidananda',
        'Useless Creatures',
        "here's my favorite track from it",
        '"Music for Zen Meditation"'
    ]

    print get_tracks_from_recommendations(recs)
