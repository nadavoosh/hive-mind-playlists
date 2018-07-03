BASE_SPOTIFY_URL = "https://embed.spotify.com/?uri=spotify:trackset:{title}:{tracks}"


class SpotifyPlaylist(object):
    def __init__(self, title, tracks):
        self.spotify = None
        self.tracks = tracks
        self.embed_link = BASE_SPOTIFY_URL.format(
            title=title,
            tracks=','.join([t.id for t in self.tracks])
        )
