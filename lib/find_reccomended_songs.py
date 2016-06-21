import os
import requests
from lxml import html
import pprint
import re
import nltk
from nltk.tokenize import word_tokenize

pp = pprint.PrettyPrinter(indent=4)

YOUTUBE_KEY = os.getenv('YOUTUBE_API_KEY')

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


def get_comments_from_page(ask_mefi_url):
    """get all comments (text) and links (<a href>s) from a metafilter URL
    """
    page = requests.get(ask_mefi_url)
    tree = html.fromstring(page.content)
    comments = tree.xpath('//div[@class="comments"]/text()') + tree.xpath('//div[@class="comments best"]/text()')
    links = tree.xpath('//div[@class="comments"]/a') + tree.xpath('//div[@class="comments best"]/a')
    return comments, links


def get_link_info(a_tag):
    """get the link text and URL from an <a href> tag"""
    return a_tag.text, a_tag.get('href')


def extract_yt_video_id(url):
    """if the URL is to a YouTube video, return the video's id"""
    video_url_format = r'www.youtube.com\/watch\?v=(\w+)'
    shortened_url_format = 'http://youtu.be/(\w+)'
    v = re.search(video_url_format, url)
    if v:
        return v.group(1)
    else:
        v2 = re.search(shortened_url_format, url)
        if v2:
            return v2.group(1)


def scrub_years(text):
    """we dont care about years"""
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
    blacklist = [
        'NPR Music Tiny Desk Concert',
        'NPR',
        'Tiny Desk',
        'Official',
        '(Official Audio)',
        '- Live',
        'www.candyrat.com',
        '( Audio)',
        '(Video Version)',
        '(Lyrics)',
        '( Video)',
        '.wmv',
        'FULL ALBUM',
        'Full Album',
        'YouTube',
        '()',
        '( )',
        '(  )'
    ]
    title = scrub_years(title)

    for word in blacklist:
        title = title.replace(word, '')

    title = title.strip().strip(':')

    #If there is just 1 word, make sure it is interesting:
    if len(title.split(' ')) == 1 and nltk.pos_tag([title]) != 'NNP':
        return None

    return title


def track_results(rec_tracker):
    """print the results of mining the thread"""
    total = rec_tracker['youtube'] + rec_tracker['link_text'] + rec_tracker['comment']

    print """
    Found {} possible recommendations:
    {} directly from comments
    {} from YouTube video titles
    {} from links to elsewhere on the web
    """.format(total, rec_tracker['comment'], rec_tracker['youtube'], rec_tracker['link_text'])


def get_recommendations(ask_mefi_url):
    """end-to-end process"""
    # initialize variables
    recommendations = []
    rec_tracker = {
        'youtube': 0,
        'comment': 0,
        'link_text': 0
    }

    # get all the comments
    comments, links = get_comments_from_page(ask_mefi_url)

    # process text comments
    for c in comments:
        c = c.replace('\t', '').strip('\r\n').strip()
        for phrase in split_comment_into_phrases(c):
            useful_words = identify_proper_nouns(phrase)
            if useful_words:
                recommendations.append(useful_words)
                rec_tracker['comment'] += 1

    # process <a href> links
    for link in links:
        link_text, link_url = get_link_info(link)
        yt_id = extract_yt_video_id(link_url)
        linked_video_title = get_title_from_yt_id(yt_id)
        if linked_video_title:
            recommendations.append(linked_video_title)
            rec_tracker['youtube'] += 1
        elif len(link_text) > word_len_cutoff:
            recommendations.append(link_text)
            rec_tracker['link_text'] += 1

    track_results(rec_tracker)
    useful_search_terms = [scrub_search_term(r) for r in recommendations]
    return [u for u in useful_search_terms if u]


if __name__ == '__main__':
    pp.pprint(get_recommendations('http://ask.metafilter.com/296503/Meditation-Music-like-Kay-Gardners-A-Rainbow-Path'))
