import unittest
from lib.spotify.build_spotify_playlist import get_tracks_from_recommendations
from .askme_tests import expected


class TestAskMeQuestions(unittest.TestCase):
    """Unit tests for askmetafilter questions"""

    def setUp(self):
        self.recs = expected

    def test_tracklist(self):
        """get tracks from the sample recs"""
        print get_tracks_from_recommendations(self.recs)
