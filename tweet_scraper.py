import snscrape.modules.twitter as sntwitter
import os
import requests
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()

def init_proxy():
    proxy_url = os.environ["PROXY_URL"]
    api_key = os.environ["API_KEY"]

    proxies = {
        'http': f"{proxy_url}?api_key={api_key}",
        'https': f"{proxy_url}?api_key={api_key}"
    }

    sntwitter.proxy_http = proxies['http']
    sntwitter.proxy_https = proxies['https']


def scrape_tweets():
    init_proxy()    

    date = datetime.now()
    since = datetime(date.year, 1, 1)

    date = date.strftime("%Y-%m-%d")
    since = since.strftime("%Y-%m-%d")

    query = f"since:{since} until:{date} ramadan market"
    tweets = []
    
    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        print(tweet)
        data = {
            'title': '',
            'author': tweet.user.username,
            'location': '' if tweet.place is None else tweet.place.fullName,
            'datetime': tweet.date.isoformat(),
            'content': tweet.rawContent,
            'url': tweet.url,

            'replyCount': tweet.replyCount,
            'retweetCount': tweet.retweetCount,
            'likeCount': tweet.likeCount,
            'quoteCount': tweet.quoteCount,
            'lang': tweet.lang,
            # 'links': tweet.links,
            # 'media': tweet.media,
            # 'retweetedTweet': tweet.retweetedTweet,
            # 'quotedTweet': tweet.quotedTweet,
            'inReplyToTweetId': str(tweet.inReplyToTweetId),
            'inReplyToUser': '' if tweet.inReplyToUser is None else tweet.inReplyToUser.username,
            'mentionedUsers': [] if tweet.mentionedUsers is None else [d.username for d in tweet.mentionedUsers],
            # 'card': tweet.card,
            'viewCount': tweet.viewCount,
            # 'vibe': tweet.vibe,
            # 'bookmarkCount': tweet.bookmarkCount,
        }
        tweets.append(data)

    return tweets
