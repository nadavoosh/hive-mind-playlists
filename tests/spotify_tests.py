import unittest
import mock
from lib.spotify.build_spotify_playlist import get_tracks_from_recommendations



class TestAskMeQuestions(unittest.TestCase):
    """Unit tests for askmetafilter questions"""
    def setUp(self):
        self.recs = [
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
        'Leonard Cohen',
        'asdf'
    ]

    def test_tracklist(self):
        """get tracks from the sample recs"""
        print get_tracks_from_recommendations(self.recs)
