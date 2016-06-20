import os
import requests
from lxml import html
import pprint
import re
import nltk
from nltk.tokenize import word_tokenize

pp = pprint.PrettyPrinter(indent=4)

YOUTUBE_KEY = os.getenv('YOUTUBE_API_KEY')


def identify_proper_nouns(comment):
    """given a phrase, return only those words that might be the names of musicians/bands/songs"""
    interesting_search_terms = []
    # replace semicolons with commas
    comment = comment.replace(';', ',')
    # split on commas, since they might represent different recommendations:
    recs = comment.split(',')
    for words in recs:
        text = word_tokenize(words)
        interesting_search_terms.append(
            ' '.join([word for word, pos in nltk.pos_tag(text) if pos == 'NNP'])
        )
    return [a for a in interesting_search_terms if a]


def get_comments_from_page(ask_mefi_url):
    page = requests.get(ask_mefi_url)
    tree = html.fromstring(page.content)
    comments = tree.xpath('//div[@class="comments"]/text()')
    links = tree.xpath('//div[@class="comments"]/a')
    return comments, links


def get_link_info(a_tag):
    return a_tag.text, a_tag.get('href')


def extract_yt_video_id(url):
    video_url_format = r'www.youtube.com\/watch\?v=(\w+)'
    shortened_url_format = 'http://youtu.be/(\w+)'
    v = re.search(video_url_format, url)
    if v:
        return v.group(1)
    else:
        v2 = re.search(shortened_url_format, url)
        if v2:
            return v2.group(1)


def get_title_from_video_id(video_id):
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


def get_recommendations(ask_mefi_url):
    # get all the comments
    recommendations = []
    recommendation_count = {
        'youtube_title': 0,
        'comment': 0,
        'link_text': 0
    }
    comments, links = get_comments_from_page(ask_mefi_url)

    for c in comments:
        c = c.replace('\t', '').strip('\r\n').strip()
        if c:
            recommendations.extend(identify_proper_nouns(c))
            recommendation_count['comment'] += 1

    for link in links:
        link_text, link_url = get_link_info(link)
        yt_id = extract_yt_video_id(link_url)
        linked_video_title = get_title_from_video_id(yt_id)
        if linked_video_title:
            recommendations.append(linked_video_title)
            recommendation_count['youtube_title'] += 1
        else:
            recommendations.append(link_text)
            recommendation_count['link_text'] += 1

    return recommendations


def scrub_song_title(title):
    """remove common terms that wont be helpful in searches"""
    blacklist = [
        'NPR Music Tiny Desk Concert',
        'NPR',
        'Tiny Desk',
        'Official',
        '(Official Audio)',
        '- Live',
        'www.candyrat.com'
    ]
    for word in blacklist:
        title = title.replace(word, '').strip()
    return title

if __name__ == '__main__':
    pp.pprint(get_recommendations('http://ask.metafilter.com/297135/Finger-Picken'))