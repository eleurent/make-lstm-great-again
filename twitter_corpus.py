#!/usr/bin/python
import sys, getopt
import json
import time
from twython import Twython

class TwitterCorpus(object):
    MAX_TWEETS_COUNT = 3200
    MAX_BATCH_SIZE = 200 # per API request
    API_REST_TIME = 300 # 5mn
    END_OF_TWEET_TOKEN = "\EOT"

    def __init__(self):
        config = self.parse_config()
        self.twitter = Twython(config.get('consumer_key'), config.get('consumer_secret'),
                               config.get('access_token'), config.get('access_token_secret'))

    """ Parse authentification keys from config.json"""
    def parse_config(self):
        f = open('config.json')
        config = json.load(f)
        return config

    """ Perform one API call to fetch tweets, with a limit count of 200."""
    def fetch_batch(self, handle, count, max_id):
        count = min(count, self.MAX_BATCH_SIZE)
        print "Fetching", count, "tweets."
        return self.twitter.get_user_timeline(screen_name=handle,
            count=count, include_retweets=False, max_id=max_id)

    """ Fetch last tweets of a given handle in several API calls."""
    def fetch(self, handle, count):
        count = min(count, self.MAX_TWEETS_COUNT)
        tweets = self.fetch_batch(handle, count % self.MAX_BATCH_SIZE, None)
        for i in range(0, count/self.MAX_BATCH_SIZE):
            print "Waiting a while between API calls..."
            time.sleep(self.API_REST_TIME)
            tweets.extend(self.fetch_batch(handle, self.MAX_BATCH_SIZE, tweets[-1]['id']))
        return tweets

    """ Dump a tweets corpus to a file.
    This method will add an end-of-tweet token at the end of each tweet."""
    @staticmethod
    def dump(tweets, filename, token=''):
        f = open(filename,'w')
        for tweet in tweets:
            f.write(tweet['text'].encode('utf-8')+token+'\n')
        f.close()


def main(argv):
    username = 'realDonaldTrump'
    count = 100
    outfile = 'corpus.txt'
    token = TwitterCorpus.END_OF_TWEET_TOKEN
    man = 'twitter_corpus.py [-u <username> -n <count> -o <outfile> -t <token>]'
    try:
        opts, args = getopt.getopt(argv,"hu:n:o:t:",["username=","count=","outfile=","token="])
    except getopt.GetoptError:
        print man
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print man
            sys.exit()
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-n", "--count"):
            count = arg
        elif opt in ("-o", "--outfile"):
            outfile = arg
        elif opt in ("-t", "--token"):
            token = arg

    tc = TwitterCorpus()
    tweets = tc.fetch(username, count)
    TwitterCorpus.dump(tweets, outfile, token)

if __name__ == "__main__":
   main(sys.argv[1:])