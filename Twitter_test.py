from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

consumer_key = 'jYsbPHYIHMDhz35NnWMesPF6D'
consumer_secret = '0DO4yX99bLt2dEwIfMU3Jvr7TwAFCKEe7m9H9l8OcAWfsA4d2l'
access_token = '20643271-QySVPZSaNjXtQf4OaOM1UTGfGaDKQlJS2qH4ACtEW'
access_token_secret = '2eXBKWxXB1bIUtZv2oRNdagx0UgD6gGwNJcedTwboa3DL'


class StdOutListener(StreamListener):
    def on_data(self, data):
        try:
            with open('C:\\Users\\Stanley\\PycharmProjects\\530\\result.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, StdOutListener())
stream.filter(track= ['다'], languages=['ko'])