import dropbox
import datetime
import json
import os
import tweepy

from credentials import twitter_access, dropbox_access


# Custom Settings:
MAX_AGE_IN_DAYS = 7
DELAY_BETWEEN_DELETES = 0.5
DELAY_BETWEEN_REQS = 45

# Tweets to save forever:
IDS_TO_KEEP = []


def main():

    n = datetime.datetime.now()

    ckey = twitter_access['consumer_key']
    csecret = twitter_access['consumer_secret']
    tkey = twitter_access['access_token_key']
    tsecret = twitter_access['access_token_secret']

    auth = tweepy.OAuthHandler(ckey, csecret)
    auth.set_access_token(tkey, tsecret)
    api = tweepy.API(auth)
    user = api.me()

    errors = []
    for page in tweepy.Cursor(api.user_timeline, id=user.id, count=200).pages():
        for tweet in page:
            try:
                delta = tweet.created_at - n
                if tweet.id in IDS_TO_KEEP:
                    continue
                elif delta.days > MAX_AGE_IN_DAYS:
                    if dropbox_access:
                        clean_tweet = clean_up_tweet(tweet)
                        response = upload_to_dropbox(clean_tweet, 'tweet')
                    api.destroy_status(tweet.id)
                    time.sleep(DELAY_BETWEEN_DELETES)
                else:
                    continue
            except:
                errors.append(tweet.id)

            time.sleep(DELAY_BETWEEN_REQS)

    return errors


def clean_up_tweet(tweet):

    clean_tweet = {
        'id': tweet.id,
        'created_at': str(tweet.created_at),
        'text': tweet.text,
        'user_name': tweet.user.screen_name,
        'retweet_count': tweet.retweet_count,
        'favorite_count': tweet.favorite_count,
        'in_reply_to_screen_name': tweet.in_reply_to_screen_name,
        'in_reply_to_user_id': tweet.in_reply_to_user_id,
        'in_reply_to_status_id': tweet.in_reply_to_status_id,
    }

    return clean_tweet


def upload_to_dropbox(tweet):

    filename = str(obj['id']) + '.json'
    f = open(filename, 'wb')
    json.dump(obj, f)
    f.close()

    #
    client = dropbox.client.DropboxClient(dropbox_access)
    f = open(filename, 'rb')
    response = client.put_file(filename, f)
    f.close()
    # Delete file
    os.remove(filename)

    return response


if __name__ == '__main__':
    main()
