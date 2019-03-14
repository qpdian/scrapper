
import requests
from bs4 import BeautifulSoup
import datetime

from scraper.processor import Processor
from scraper.logger import Logger


class TwitterScraper:


    def __init__(self, users):
        self.users = users
        self.logger = Logger(self)
        self.processor = Processor()

    def dateFromMilesecond(self, milesecond):
        return datetime.datetime.fromtimestamp(milesecond / 1000.0)

    def scrape_tweet(self, content):
        
        comma = ','
        dot = '.'

        textHtml = content.find('p', {'class': 'tweet-text'})
        textValue = (textHtml.text if textHtml else None)
        tweetId = content['data-item-id']
        self.logger.scraping_item(tweetId)
        timeHtml = content.find('span', {'class': '_timestamp'})
        time = (self.dateFromMilesecond(int(timeHtml['data-time-ms'
                ])) if timeHtml else None)

        if content.find('div', {'class': 'stream-item-footer'}):
            interactions = [x.text for x in
                            content.select('.ProfileTweet-actionCount')]
            replies = int(interactions[0].split(' ')[0].replace(comma,
                          '').replace(dot, ''))
            retweets = int(interactions[1].split(' ')[0].replace(comma,
                           '').replace(dot, ''))
            likes = int(interactions[2].split(' ')[0].replace(comma, ''
                        ).replace(dot, ''))
        else:
            replies = ''
            retweets = ''
            likes = ''

        hashtags = [hashtag_node.text for hashtag_node in
                    content.select('.twitter-hashtag')]
        urls = [url_node['data-expanded-url'] for url_node in
                content.select('a.twitter-timeline-link:not(.u-hidden)'
                )]
        result = {
            'tweetId': tweetId,
            'time': time,
            'description': textValue,
            'author': None,
            'replies': replies,
            'retweets': retweets,
            'likes': likes,
            'entries': {'hashtags': hashtags, 'urls': urls},
            }

        self.processor.send(result, self)
        self.logger.result_sent(result)
       
        return result

    def get_response(self, user, params={}):
        url = 'https://twitter.com/i/profiles/show/{}/timeline/tweets?include_available_features=1&include_entities=1&include_new_items_bar=true'.format(user)
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': 'https://twitter.com/{}'.format(user),
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
            'X-Twitter-Active-User': 'yes',
            'X-Requested-With': 'XMLHttpRequest',
            }
        return requests.get(url, headers=headers, params=params,
                            timeout=8)

    def get_tweets_list(
        self,
        tweets,
        user,
        rangeTweets
        ):

        response = self.get_response(user, {'min_position': rangeTweets['min'
                                ], 'max_position': rangeTweets['max']})
        if response.status_code != 200:
            return []
        data = response.json()

        soup = BeautifulSoup(data['items_html'], 'html.parser')
        tweetsHtml = soup.findAll('li', {'class': 'stream-item'})
        tweetsSection = list(filter(lambda tweet: tweet.get('text'),
                             list(map(self.scrape_tweet, tweetsHtml))))


        if data.get('has_more_items'):
            rangeTweets['max'] = (tweetsSection[-1]['tweetId'
                                  ] if len(tweetsSection)
                                  > 0 else rangeTweets['max'])
            return tweetsSection + self.get_tweets_list(tweets, user,
                    rangeTweets)
        else:
            return tweetsSection

    def run(self):
        self.logger.start_scraping_run()
        for user in self.users:
            self.get_tweets_list([], user['name'],
                                 {'min': user['lastTweet'],
                                 'max': None})
        self.logger.finished_scraping_run()


if __name__ == '__main__':

    # get username from a database, where each username has a max_position ( get until last tweet)
    # the first time lastTweet is None, after save  last tweet more recent as lastTweet
    # 'domingobiojo','timofarc','farc_delpueblo','ivanmarquezfarc'
    # '1007252459075620864'

    s = TwitterScraper([{'name': 'diam_qu', 'lastTweet': None}])
    s.run()


			