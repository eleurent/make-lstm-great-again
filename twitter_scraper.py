""" Fetch tweets from a given twitter handle

Usage:
  twitter_scraper.py <handle> [-o <file>] [-c <n>]
                              [--include_retweets]
                              [--delay <seconds>]
                              [--token <t>]
                              [--encoding <e>]
  twitter_scraper.py -h | --help

Options:
  -h --help
  -o <file> --output <file>  Output file [default: tweets.txt]
  -c <n> --count <n>         Number of tweets fetched [default: 500]
  --include_retweets         Include retweets in the result
  --delay <seconds>          Delay between two API calls [default: 30]
  --token <t>                Token appended at the end of each tweet [default: \EOT]
  --encoding <e>             Encoding used when saving the tweets [default: utf-8]

The Twitter API connection has to be configured via a config.json file
holding the following dictionary:
{
    "consumer_key":"<consumer_key>",
    "consumer_secret":"<consumer_secret>",
    "access_token":"<access_token>",
    "access_token_secret":"<access_token_secret>"
}
"""

from __future__ import print_function
import sys, getopt
import json
import time
from twython import Twython
from docopt import docopt

""" A class to authenticate requests to Twitter API, to fetch a number of tweets
    from a given user, and dump the results in a file."""
class TwitterScraper(object):
    MAX_BATCH_SIZE = 200 # per API request

    def __init__(self):
        config = self.parse_config()
        self.twitter = Twython(config.get('consumer_key'), config.get('consumer_secret'),
                               config.get('access_token'), config.get('access_token_secret'))

    """ Parse authentification keys from config.json"""
    def parse_config(self):
        f = open('config.json', 'r')
        return json.load(f)

    """ Perform one API call to fetch tweets, with a limit count of 200."""
    def fetch_batch(self, handle, count, include_retweets, max_id):
        count = min(count, self.MAX_BATCH_SIZE)
        print("Fetching", count, "tweets.")
        return self.twitter.get_user_timeline(screen_name=handle,
            count=count, include_retweets=include_retweets, max_id=max_id)

    """ Fetch last tweets of a given handle in several API calls."""
    def fetch(self, parameters):
        q, r = parameters['--count'] / self.MAX_BATCH_SIZE, \
               parameters['--count'] % self.MAX_BATCH_SIZE
        if r > 0:
            tweets = self.fetch_batch(parameters['<handle>'], r, parameters['--include_retweets'], None)
        for i in range(q):
            print("Resting a while between API calls...", (i+1), "/", q)
            time.sleep(parameters['--delay'])
            tweets.extend(self.fetch_batch(parameters['<handle>'],
                                           self.MAX_BATCH_SIZE,
                                           parameters['--include_retweets'],
                                           tweets[-1]['id']))
        return tweets

    """ Dump a tweets corpus to a file.
    This method will add an end-of-tweet token at the end of each tweet."""
    @staticmethod
    def dump(tweets, parameters):
        with open(parameters['--output'], 'w') as f:
            for tweet in tweets:
                f.write(tweet['text'].encode(parameters['--encoding'])+parameters['--token']+'\n')

""" Cast numeric parameters"""
def cast_parameters(parameters):
    parameters['--count'] = int(parameters['--count'])
    parameters['--delay'] = float(parameters['--delay'])
    return parameters

if __name__ == '__main__':
    parameters = cast_parameters(docopt(__doc__))
    tweets = TwitterScraper().fetch(parameters)
    TwitterScraper.dump(tweets, parameters)
