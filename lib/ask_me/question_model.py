"""
a model for an askMe question, with answers and comments
"""

import logging
import re
from lxml import html

import requests
import lib.ask_me.parsing_utils as pu

logger = logging.getLogger(__name__)


RANDOM_ASKME_URL = 'http://ask.metafilter.com/random'
BASE_ASKME_URL = 'http://ask.metafilter.com/{}/'
ASKME_URL_PATTERN = r'^((http|https):\/\/|)ask\.metafilter\.com\/([0-9]+)'


class Reccomendation(object):
    def __init__(self, text, source):
        self.text = text
        self.source = source

    def __str__(self):
        return self.text


class AskMetafilterQuestion(object):
    def __init__(self, url):
        self.url = url
        self.page = requests.get(self.url)
        self.tree = html.fromstring(self.page.content)
        self.posttitle = self.tree.xpath('//h1[@class="posttitle"]/text()')[0]
        self.alphanumeric_posttitle = re.sub(r'\W+', '', self.posttitle)
        self.recommendations = []  # this will hold the recommendations

    def get_comments(self):
        regular = self.tree.xpath('//div[@class="comments"]/text()')
        best = self.tree.xpath('//div[@class="comments best"]/text()')
        return regular + best

    def get_links(self):
        regular = self.tree.xpath('//div[@class="comments"]/a')
        best = self.tree.xpath('//div[@class="comments best"]/a')
        return regular + best

    def process_comments(self):
        """process text comments"""
        for c in self.get_comments():
            c = c.replace('\t', '').strip('\r\n').strip()
            for phrase in pu.split_comment_into_phrases(c):
                useful_words = pu.identify_proper_nouns(phrase)
                if useful_words:
                    self.recommendations.append(Reccomendation(useful_words, 'comment'))

    def process_links(self):
        """process <a href> links"""
        for link in self.get_links():
            link_text, link_url = pu.get_link_info(link)
            yt_id = pu.extract_yt_video_id(link_url)
            linked_video_title = pu.get_title_from_yt_id(yt_id)
            if linked_video_title:
                self.recommendations.append(Reccomendation(linked_video_title, 'youtube'))
            elif len(link_text) > pu.word_len_cutoff:
                self.recommendations.append(Reccomendation(link_text, 'link_text'))

    def get_recommendations(self):
        """end-to-end process"""
        self.process_comments()
        self.process_links()
        useful_search_terms = [pu.scrub_search_term(r.text) for r in self.recommendations]
        logger.info("%s total recommendations from %s", len(self.recommendations), self.url)
        logger.info("%s recommendations directly from comments", len([r for r in self.recommendations if r.source == 'comment']))
        logger.info("%s recommendations from YouTube video titles", len([r for r in self.recommendations if r.source == 'youtube']))
        logger.info("%s recommendations links to elsewhere on the web", len([r for r in self.recommendations if r.source == 'link_text']))
        return [u for u in useful_search_terms if u]
