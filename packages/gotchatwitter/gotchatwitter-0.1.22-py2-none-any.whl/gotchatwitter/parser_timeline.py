import json
from random import random
from time import sleep

from bs4 import BeautifulSoup

from parser_utils import *


MAX_WORDS_ANY = 20


def parse_user_timeline(u_screen_name, connector, header, **kwargs):
    adv_search = kwargs.get('adv_search', dict())
    date_since = adv_search.get('date_since', kwargs.get('date_since', ''))
    date_until = adv_search.get('date_until', kwargs.get('date_until', ''))
    words_any = adv_search.get('words_any', kwargs.get('words_any', []))
    # words_any = [re.sub('@|#', '', wa) for wa in words_any]
    question = adv_search.get('question', kwargs.get('question', False))

    if len(words_any) > MAX_WORDS_ANY:
        words_any = [words_any[x:x+MAX_WORDS_ANY] for x in range(0, len(words_any), MAX_WORDS_ANY)]
        for wa in words_any:
            kwargs['words_any'] = wa
            yield wa
            for row in parse_user_timeline(u_screen_name, connector, header, **kwargs):
                yield row
    else:
        tid_start = ''
        tid = ''
        error_count = 0
        max_position = ''
        is_page_one = True
        _next = True
        while _next:
            if adv_search or date_since or date_until or question or words_any:
                if is_page_one:
                    url = 'https://twitter.com/search?q=' + \
                          'from%3A' + u_screen_name + \
                          ('%20since%3A' + date_since if date_since else '') + \
                          ('%20until%3A' + date_until if date_until else '') + \
                          ('%20%3F' if question else '') + \
                          ('%20' + '%20OR%20'.join(words_any) if words_any else '') + \
                          '&src=typd&lang=en'
                    html = connector.get(url).content
                    is_page_one = False
                    soup = BeautifulSoup(html, 'lxml')
                    max_position = soup.find('div', class_=re.compile('stream-container'))\
                        .attrs.get('data-max-position')
                else:
                    url = 'https://twitter.com/i/search/timeline?vertical=default&q=from%3A' + u_screen_name + \
                          ('%20since%3A' + date_since if date_since else '') + \
                          ('%20until%3A' + date_until if date_until else '') + \
                          ('%20%3F' if question else '') + \
                          '&src=typd&include_available_features=1&include_entities=1&' + \
                          'max_position=' + max_position
                    # 'TWEET-' + tid + '-' + tid_start + '-' + \
                    # 'BD1UO2FFu9QAAAAAAAAETAAAAAcAAAASAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' + \
                    # '&reset_error_state=false'
                    html_json = json.loads(connector.get(url).content)
                    if html_json.get('errors', ''):
                        sleep(random() * 10)
                        error_count += 1
                        if error_count <= 5:
                            continue
                        else:
                            break
                    html = html_json['items_html'].strip()
                    _next = html_json['has_more_items']
                    soup = BeautifulSoup(html, 'lxml')
                    max_position = html_json.get('data-max-position', html_json.get('min_position', ''))
            else:
                if is_page_one:
                    url = 'https://twitter.com/' + re.sub('@', '', u_screen_name)
                    html = connector.get(url).content
                    soup = BeautifulSoup(html, 'lxml')
                    is_page_one = False
                else:
                    url = 'https://twitter.com/i/profiles/show/' \
                          + re.sub('\@', '', u_screen_name) \
                          + '/timeline/tweets?include_available_features=1&include_entities=1&max_position=' \
                          + tid \
                          + '&reset_error_state=false'
                    html_json = json.loads(connector.get(url).content)
                    html = html_json['items_html'].strip()
                    _next = html_json['has_more_items']
                    soup = BeautifulSoup(html, 'lxml')

            tweet_cardwraps = soup.find_all(lambda tag: re.compile('js-stream-item').search(str(tag))
                                                        and not re.compile('scroll-bump|separationModule').search(str(tag))
                                                        and tag.name == 'li')
            if len(tweet_cardwraps) == 0:
                break

            yield [url]
            for tweet_cardwrap in tweet_cardwraps:
                # print parse_text(tweet_cardwrap)
                status, uid, screen_name, tid, rid, timestamp, location_id, location_name = \
                    parse_header(tweet_cardwrap)
                language, text = parse_text(tweet_cardwrap)
                n_retweets, n_likes = parse_footer(tweet_cardwrap)
                quote_status, quote_text = parse_quote(tweet_cardwrap)
                status = quote_status if quote_status else status
                text = text + ' <quote> ' + quote_text + ' <quote>' if quote_text else text
                media = parse_media(tweet_cardwrap)
                yield [locals()[head].encode('utf-8') for head in header]
                if not tid_start:
                    tid_start = rid if rid else tid
