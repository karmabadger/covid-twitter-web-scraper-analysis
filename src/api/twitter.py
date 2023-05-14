import tweepy
import os

from dotenv import load_dotenv
load_dotenv()


client = tweepy.Client(consumer_key=os.environ['TWITTER_API_KEY'],
                  consumer_secret=os.environ['TWITTER_API_SECRET'],
                  access_token= os.environ['TWITTER_ACCESS_TOKEN_KEY'],
                  access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'],
                  bearer_token=os.environ['TWITTER_BEARER_TOKEN'],
                  wait_on_rate_limit=True)


# print(client)