from credentials import twitter_access

from datetime import date, timedelta
from time import strptime

import csv
import glob
import json
import logging
import time
import tweepy


DATA_PATH = './data/js/tweets/*.js'

# If you want to preserve tweets after a certain date or since
# a certain number of days, fill out only *one* of the following
# variables with the appropriate information.
# If you leave both variables as 'None', *all* of your tweets will
# be deleted by this script.

# Only delete tweets that are older than this many days:
# Replace 'None' with a number, e.g., 'MAX_DAYS = 7'
MAX_DAYS = None

# Only delete tweets that are older than this date:
# Replace 'None' with 'date(year=<YEAR>, month=<MONTH>, day=<DAY>)'
# e.g., March 14th 2014 would be 'MAX_DATE = date(year=2014, month=3, day=)'
MAX_DATE = None


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
                tweet_date = clean_date(tweet['created_at'])
                max_date = get_max_date()
                delta = max_date - tweet_date
                if delta.days > 0:
                    tweet_ids.append(tweet['id'])
                else:
                    continue

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


def clean_date(date_string):
    """
    Clean 'created_at' tweet attribute into
    date object. 'created_at' contains date, time,
    and timezone info; split date off and convert
    into date object.
    """
    datestring_format = "%Y-%m-%d"
    split = date_string.split()
    date_string_date = split[0]
    date_struct = strptime(date_string_date, datestring_format)
    d = date(*date_struct[:3])
    return d


def get_max_date():

    if MAX_DATE is not None:
        return MAX_DATE
    elif MAX_DAYS is not None:
        max_date = date.today() - timedelta(days=MAX_DAYS)
        return max_date
    else:
        return date.today()


if __name__ == '__main__':
    main()
