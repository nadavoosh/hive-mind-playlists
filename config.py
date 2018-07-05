import os

# https://console.developers.google.com/apis/dashboard
YOUTUBE_KEY = os.getenv('YOUTUBE_API_KEY')
if not YOUTUBE_KEY:
    raise Exception('YOUTUBE_API_KEY required')

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
if not SPOTIFY_CLIENT_ID:
    raise Exception('SPOTIFY_CLIENT_ID required')

SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
if not SPOTIFY_CLIENT_SECRET:
    raise Exception('SPOTIFY_CLIENT_SECRET required')
