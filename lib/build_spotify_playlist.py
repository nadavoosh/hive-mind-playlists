import spotipy
# import spotipy.util as util
import pprint
from find_reccomended_songs import get_recommendations

# birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
# spotify = spotipy.Spotify()
# scope = 'playlist-modify-public'
# token = util.prompt_for_user_token('nadavoosh', scope)

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

def get_tracks_from_recommendations(recs):
    sp = spotipy.Spotify()
    tracks = []
    for rec in recs:
        res = sp.search(rec, type='track')
        print 'searching for {}'.format(rec)
        pp.pprint([filter_spotify_result(item) for item in res['tracks']['items'][:3]])
        print '============='
        # tracks.append(res[0])
    return tracks


if __name__ == '__main__':
    # recs = get_recommendations('http://ask.metafilter.com/297135/Finger-Picken')
    recs = [
        'A few personal contemporary favorites:',
        'Give',
        'a shot.',
        'Kaki King.',
        'Just saw Leo recently. He still has it! Here are some other finger-pickers who are virtuosos, though mostly older folks, too. RIP where applicable. Styles range from the Blues to Jazz to Country:',
        'Pierre Bensusan; John Fahey; Chris Smither; Michael Hedges; Tuck Andress; Rory Block; Stephan Grossman; Tommy Emmanuel; Pete Huttlinger; Jorma Kaukonen; Jerry Reed; Chet Atkins; Merle Travis; Don Ross; Adam Rafferty; Mike Russo; Buster Jones.',
        'Hope some of these players appeal to you!',
        'I came in to post  the list zchrys did. Good stuff. Also see The Black Twig Pickers.',
        'Definitely check out Don Ross.',
        'Also check out',
        '(the label Ross is on). Very fingerstyle-heavy',
        ', including',
        ", who's had a few viral youtube hits.",
        'Would also recommend giving',
        'a listen as well to see if his playing is of interest - I rather enjoy it:',
        'William Tyler, Cian Nugent, Daniel Bachman, The',
        'series of compilations that Tompkins Square released (infact a lot of Tompkins Square releases would be relevant), James Blackshaw, Nathan Bowles (Banjo)',
        'Harry Tausig on Tompkins Square.',
        'Oh! Almost forgot...check out',
        '. He does both slide and non-slide fingerpicking:',
        'Glenn Jones - Flower Turned Inside-Out (Official Audio)',
        'Song for the Setting Sun I',
        'Jack Rose - Kensington Blues',
        'Days of Blue by Laura Baird',
        'Six Organs of Admittance - Hold But Let Go',
        'Tallest Man on Earth: NPR Music Tiny Desk Concert',
        'Candy Rat Records',
        'lineup of players',
        'Andy McKee - Guitar - Drifting - www.candyrat.com',
        'Boubacar Traore - Minuit',
        'Imaginational Anthem',
        'Kelly Joe Phelps',
        'Country Blues',
        'Kelly Joe Phelps - Go There'
    ]
    print get_tracks_from_recommendations(recs)
