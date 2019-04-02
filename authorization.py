def my_auth():
    """

    :rtype: object
    """
    import tweepy
    consumer_key = ''
    consumer_secret = ''
    access_token = ''
    access_token_secret = ''

    # Setup tweepy to authenticate with Twitter credentials:
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # return a twitter api with your credentials
    return tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
