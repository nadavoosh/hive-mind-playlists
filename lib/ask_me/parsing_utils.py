"""
functions for parsing metafilter comments
"""

import re
import logging
import requests
import nltk
from nltk.tokenize import word_tokenize
from lib.ask_me.blacklist import BLACKLIST
from config import YOUTUBE_KEY


logger = logging.getLogger(__name__)

word_len_cutoff = 1


def split_comment_into_phrases(comment):
    """split on commas and semicolons, since they probably separate recommendations.
    newlines should already be split before this function is called.
    """
    # replace semicolons with commas
    comment = comment.replace(';', ', ').replace('. ', ', ')
    # split on commas, since they might represent different recommendations:
    return comment.split(',')


def approve_word(word):
    """Should we include this word as a search term?"""
    return word[0].isupper() and len(word) > word_len_cutoff


def identify_proper_nouns(phrase):
    """given a phrase, return ~the NNP words and~ those starting with upper case, since those
    have a better chance of being the names of musicians/bands/songs,
    and a lower chance of cluttering up search results
    """
    text = word_tokenize(phrase)
    # return ' '.join([w for w, pos in nltk.pos_tag(text) if pos == 'NNP' or approve_word(w)])
    return ' '.join([w for w in text if approve_word(w)])


def get_link_info(a_tag):
    """get the link text and URL from an <a href> tag"""
    return a_tag.text or '', a_tag.get('href') or ''


def extract_yt_video_id(url):
    """if the URL is to a YouTube video, return the video's id"""
    video_url_format = r'www.youtube.com\/watch\?v=(\w+)'
    shortened_url_format = r'http://youtu.be/(\w+)'
    v = re.search(video_url_format, url)
    if v:
        return v.group(1)
    else:
        v2 = re.search(shortened_url_format, url)
        if v2:
            return v2.group(1)


def scrub_years(text):
    """we don't care about years in song titles"""
    year_format = r'[1|2]\d\d\d'
    v = re.search(year_format, text)
    if v:
        return text.replace(v.group(0), '')
    return text


def get_title_from_yt_id(video_id):
    """Given a YouTube video ID, return the video title"""
    if not video_id:
        return None
    url = 'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={}&key={}'.format(video_id, YOUTUBE_KEY)
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception('Got a {} error when trying to GET the title of {}: {}'
                        .format(r.status_code, video_id, r.text))
    video_data = r.json()
    if video_data['items']:
        return video_data['items'][0]['snippet']['title']


def scrub_search_term(title):
    """remove common terms that wont be helpful in searches,
    and generally clean search term
    """
    title = scrub_years(title)
    for word in BLACKLIST:
        title = title.replace(word, '')
    title = title.strip().strip(':')
    #If there is just 1 word, make sure it is interesting:
    if len(title.split(' ')) == 1 and nltk.pos_tag([title]) != 'NNP':
        return None
    return title
