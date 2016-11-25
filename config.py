import os

# https://console.developers.google.com/apis/dashboard
YOUTUBE_KEY = os.getenv('YOUTUBE_API_KEY')
if not YOUTUBE_KEY:
    raise Exception('YOUTUBE_API_KEY required')
