import tweepy
import authorization
import datetime as dt
from collect_tweets import tweet_cleaner


class TweepError(Exception):
    pass


class StreamListener(tweepy.StreamListener):
    def on_data(self, data):
        import json
        this_tweet = json.loads(data)
        tweet_message = tweet_cleaner(this_tweet)
        if tweet_message is not None:
            print(tweet_message, "\n")
            with open('StreamListener.txt', 'a', encoding='utf-8') as f:
                f.write(">!!>>!!>>!" + tweet_message)               # '>!!>>!!>>!' separates two tweets

    def on_error(self, status_code):
        print(status_code)


if __name__ == "__main__":
    api = authorization.my_auth()
    stream_listener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener, tweet_mode='extended')

    with open('StreamListener.txt', 'a', encoding='utf-8') as f:
        f.write('\n' + 'startOfTwitterStream at: ' + str(dt.datetime.now()) + '\n')     # Save collected tweets from the listener

    gib = stream.filter(track=['다'], locations=[126, 34, 129, 38])  # Coordinate covers south korea. "다" is a sentence ending particle in Korean
