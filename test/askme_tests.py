import unittest
from lib.ask_me.find_reccomended_songs import AskMetafilterQuestion, get_recommendations

class TestAskMeQuestions(unittest.TestCase):
    """Unit tests for askmetafilter questions"""
    def setUp(self):
        self.url = 'http://ask.metafilter.com/296503/Meditation-Music-like-Kay-Gardners-A-Rainbow-Path'
        self.question = AskMetafilterQuestion(self.url)

    def test_reccomendations(self):
        """test the reccomendations for the sample question"""
        self.assertEqual(get_recommendations(self.question), 1)


if __name__ == '__main__':
    unittest.main()
