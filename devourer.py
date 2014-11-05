from deletebot_credentials import twitter_access, dropbox_access

import dropbox
import datetime
import tweepy


# Custom Settings:
MAX_AGE_IN_DAYS = 7
DELAY_BETWEEN_DELETES = 0.5
DELAY_BETWEEN_REQS = 45

# Tweets to save forever:
IDS_TO_KEEP = []

# Important constants to not mess around with:
API_TWEET_MAX = 3200
TWEETS_PER_PAGE = 200
NUM_PAGES = int(API_TWEET_MAX / TWEETS_PER_PAGE)


def main():

    n = datetime.datetime()

    ckey = access['consumer_key']
    csecret = access['consumer_secret']
    tkey = access['access_token_key']
    tsecret = access['access_token_secret']

    auth = tweepy.OAuthHandler(ckey, csecret)
    auth.set_access_token(tkey, tsecret)

    api = tweepy.API(auth)
    user = api.me()

    dropbox_tweets = []
    errors = []
    for page in tweepy.Cursor(api.user_timeline, id=user.id, count=200).pages():
        for tweet in page:
            try:
                delta = tweet.created_at - n
                if delta.days > MAX_AGE_IN_DAYS:
                    dropbox_tweets.append(tweet)
                    api.destroy_status(tweet.id)
                    time.sleep(DELAY_BETWEEN_DELETES)
                else:
                    continue
            except:
                errors.append(tweet.id)

            time.sleep(DELAY_BETWEEN_REQS)

    upload_to_dropbox(dropbox_tweets, errors)






def upload_to_dropbox(tweets, errors):
    pass


if __name__ == '__main__':
    main()
