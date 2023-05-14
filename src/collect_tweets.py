from api.twitter import client

import argparse

import pandas as pd

import datetime as dt

import json

def collect_tweets(query, count=100, next_token=None):
    """
    Collect tweets from Twitter API
    :param query: search query
    :param count: number of tweets to collect
    :return: list of tweets
    """
    # df = pd.DataFrame(columns=['id', 'text', 'created_at', 'retweet_count', 'favorite_count', 'lang'])
    tweets = client.search_recent_tweets(query, 
                                         max_results=count, 
                                         tweet_fields=["author_id","created_at","entities","public_metrics","geo","context_annotations", "referenced_tweets"],
    user_fields=["name","username","verified","public_metrics"],
    place_fields=["country","full_name","place_type"],
    end_time=dt.datetime(2021, 12, 8),
    next_token=next_token,
)

    # df.append(tweets.data[0].data, ignore_index=True)

    return tweets


def main():
    """
    Collect tweets from Twitter API
    :return: None
    """

    parser = argparse.ArgumentParser(description='Collect tweets from Twitter API')
    parser.add_argument('-o', '--output', help='output file', default='tweets.json')
    args = parser.parse_args()


    

    num_tweets_required = 10000
    batch_limit = 100
    total_num_tweets = 0
    next_token = None

    f = open(args.output, 'w')
    
    while total_num_tweets < num_tweets_required:
        # query = "(vaccination OR AstraZeneca OR Janssen OR Moderna OR Pfizer OR BioNTech) lang:en -is:retweet"
        query = "(vaccination) lang:en -is:retweet"
        # query = "(vaccination) lang:en -is:retweet"
        # query = "(vaccination OR AstraZeneca OR Janssen OR Moderna OR Pfizer OR BioNTech) lang:en -is:retweet"
        tweets = collect_tweets(query, count=batch_limit, next_token=next_token)

        # print("data", tweets.data)
        for tweet in tweets.data:
            f.write(json.dumps(tweet.data))
            f.write('\n')
            
        total_num_tweets += tweets.meta['result_count']
        next_token = tweets.meta['next_token']
        
        print("total_num_tweets:", total_num_tweets)

    f.close()








if __name__ == '__main__':
    main()