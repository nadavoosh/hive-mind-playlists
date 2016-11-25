import unittest
import mock
from lib.ask_me.question_model import AskMetafilterQuestion


class TestAskMeQuestions(unittest.TestCase):
    """Unit tests for askmetafilter questions"""
    def setUp(self):
        self.url = 'http://ask.metafilter.com/296503/Meditation-Music-like-Kay-Gardners-A-Rainbow-Path'
        self.question = AskMetafilterQuestion(self.url)

    def test_reccomendations(self):
        """get recommendations for the sample question"""
        expected = [
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
        self.assertEqual(self.question.get_recommendations(), expected)
