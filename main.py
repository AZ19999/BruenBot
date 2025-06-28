import os
import random
from datetime import datetime
import requests
import tweepy

MESSAGESAWAKE = [
    "David Bruensburger is awake.",
    "David Bruensburger is up.",
    "David Bruensburger is still awake.",
    "David Bruensburger's status: Awake ✅",
    "David Bruensburger is concious.",
    "David Bruensburger is not asleep.",
    "David Bruensburger is active now.",
    "David Bruensburger is wide awake."
]

MESSAGESASLEEP = [
    "David Bruensburger is asleep.",
    "David Bruensburger went to bed",
    "David Bruensburger is not awake.",
    "David Bruensburger has begun his slumber.",
    "David Bruensburger's status: Awake ❌",
    "David Bruensburger is resting for the night.",
    "David Bruensburger is now not active.",
    "David Bruensburger is fast asleep."
]

# Authorize Twitter with v1.1 API
def auth_v1(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)


# Authorize Twitter with v2 API
def auth_v2(consumer_key, consumer_secret, access_token, access_token_secret):
    return tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_token_secret,
        return_type=requests.Response,
    )

# Tweet text or media
def tweet(media=None, text=None) -> requests.Response:
    # In the next for 4 lines we are getting the keys from Step 4
    consumer_key = os.environ['CONSUMER_KEY']
    consumer_secret = os.environ['CONSUMER_SECRET']
    access_token = os.environ['ACCESS_TOKEN']
    access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

    api_v1 = auth_v1(consumer_key, consumer_secret,
                     access_token, access_token_secret)
    client_v2 = auth_v2(consumer_key, consumer_secret,
                        access_token, access_token_secret)

    if text:
        return client_v2.create_tweet(text = text)
    elif media:
        media_id = api_v1.media_upload(media).media_id
        return client_v2.create_tweet(media_ids = [media_id])
    else:
        raise ValueError("Either 'text' or 'media' must be provided.")

def getRandomMessage() -> str:
    current_hour = datetime.now().hour
    if 8 <= current_hour < 22:  # Between 8 AM and 10 PM
        return random.choice(MESSAGESAWAKE)
    else:  # Outside of 8 AM to 10 PM
        return random.choice(MESSAGESASLEEP)

def main():
    message = getRandomMessage()
    print("tweeting: " + message)
    tweet(text = message)

if __name__ == '__main__':
    main()
