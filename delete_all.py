from credentials import twitter_access

import csv
import glob
import json
import logging
import time
import tweepy


DATA_PATH = './data/js/tweets/*.js'


def main():

    ckey = twitter_access['consumer_key']
    csecret = twitter_access['consumer_secret']
    tkey = twitter_access['access_token_key']
    tsecret = twitter_access['access_token_secret']

    auth = tweepy.OAuthHandler(ckey, csecret)
    auth.set_access_token(tkey, tsecret)

    api = tweepy.API(auth)
    user = api.me()

    tweet_ids = []
    files = glob.glob(DATA_PATH)
    for f in files:
        with open(f) as fin:
            d = fin.readlines()[1:]
            d = "".join(d)
            j = json.loads(d)
            for tweet in j:
                tweet_ids.append(tweet['id'])

    i = 0
    destroyed = []
    gone_wrong = []
    for t_id in tweet_ids:

        if (i % 20) == 0:
            print '{} tweets processed'.format(i)
            print '{} tweets deleted'.format(len(destroyed))
            print '{} tweets threw errors'.format(len(gone_wrong))
            print ''

        try:
            api.destroy_status(t_id)
            destroyed.append(t_id)
        except:
            gone_wrong.append(t_id)

        i += 1
        time.sleep(0.05)

    logging.info('{} tweets processed'.format(i))
    print '{} tweets deleted'.format(len(destroyed))
    print '{} tweets threw errors'.format(len(gone_wrong))
    print ''


if __name__ == '__main__':
    main()
