import authorization


class TweepError(Exception):
    pass


def get_followers(account_name):
    """Return a list of all the followers of an account"""

    api = authorization.my_auth()  # authorization

    followers = []
    for page in tweepy.Cursor(api.followers_ids, screen_name=str(account_name)).pages():
        followers.extend(page)
    return followers


def tweetCount(input):
    """
    requires a list of twitter user ids
    returns a txt file composed of two columns each for user id and for number of tweets
    """

    api = authorization.my_auth()  # authorization

    with open('tweetCount.txt', 'w') as f:
        f.write("userID" + "\t" + "# of tweets")
    with open('errorID.txt', 'w') as f:
        f.write("")

    clean_input = []

    for uid in input:
        try:
            tweet_count = api.get_user(int(uid)).statuses_count
            clean_input.append(uid)
            with open('tweetCount.txt', 'a') as f:
                f.write(str(uid) + "\t" + str(tweet_count) + "\n")
        except:
            with open('errorID.txt', 'a') as f:
                f.write(uid + "\n")
    return tweet_count, clean_input
