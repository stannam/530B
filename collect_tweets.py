import authorization
import regex as re
import os
import pandas as pd


class TweepError(Exception):
    pass


def collect_tweets(category):
    """
    :param category: name of the userlist txt file.
    :return: txt files for tweet messages, plus three txt files under the directory 'result'.
            (user id).txt is the collection of 'pure' tweet messages made by the person with the user id.
            tocollect.txt is the user ID's to be collected
            finished.txt is the user ID's finished collecting tweets from
            and log.txt is the log file.

    Function 'collect_tweets' collects recent 'pure' tweets (maximum 200) from each user in the userlist,
              and saves collected messages in each txt file named after the user ID.
              'Pure' tweets indicate the tweets that are not retweets. See function 'tweet_cleaner.'
    """
    result_directory = './result/'+category+'/'
    if not os.path.isdir(result_directory):
        os.mkdir(result_directory)
        open(result_directory+'finished.txt', 'a').close()
        user_data = pd.read_csv(category+'.txt', sep="\t")
        userlist = list(user_data.userID)
        with open(result_directory+'tocollect.txt', 'w') as f:
            for uid in userlist:
                f.write("%s\n" % uid)
    tocollect = []
    with open(result_directory+'tocollect.txt') as f:
        for line in f:
            tocollect.append(line.strip())
    finished = []
    with open(result_directory+'finished.txt') as f:
        for line in f:
            finished.append(line.strip())

    while len(tocollect) > 0:
        twit_count = 0
        user_id = tocollect[-1]
        open(result_directory+user_id+'.txt', 'w', encoding='utf-8').close()
        try:
            status_set = api.user_timeline(user_id=user_id, count=200, tweet_mode='extended')
        except Exception as e:
            scr_name = user_data.loc[user_data['userID'] == int(user_id)]['screen_name']
            scr_name = pd.Series.to_string(scr_name, index=0)
            scr_name = re.sub(" ", "", scr_name)
            try:
                status_set = api.user_timeline(screen_name=scr_name, count=200, tweet_mode='extended')
            except Exception as e:
                twit_count = str(e)
                status_set = []

        for status in status_set:
            twit_dict = status._json
            message = tweet_cleaner(twit_dict)
            if message is not None:
                twit_count += 1
                with open(result_directory+user_id+'.txt', 'a', encoding='utf-8') as f:
                    f.write(">!!>>!!>>!" + message)  # '>!!>>!!>>!' separates two tweets

        finished.append(tocollect.pop())
        log = str(user_id)+"\t"+str(twit_count)
        # update tocollect.txt finished.txt and log.txt

        with open(result_directory+'tocollect.txt','w') as f:
            for uid in tocollect:
                f.write("%s\n" % uid)
        with open(result_directory+'finished.txt','w') as f:
            for uid in finished:
                f.write("%s\n" % uid)
        with open(result_directory+'log.txt','a') as f:
            f.write(log+"\n")



def tweet_cleaner(twit_dict):
    """
    :param twit_dict: retrieved tweet in the dict type
    :return: full tweet message

    Function 'tweet_cleaner' removes retweets and returns the full message (not truncated) of tweets with
    140+ characters.
    """
    if twit_dict['truncated']:
        tweet_message = twit_dict['extended_tweet']['full_text']
    else:
        try:
            tweet_message = twit_dict['full_text']
        except:
            tweet_message = twit_dict['text']
    try:
        if "RT @" not in tweet_message:
            tweet_message = re.sub("\n|\r", " ", tweet_message)     # remove changes of line in a tweet
            tweet_message = re.sub("  ", " ", tweet_message)        # remove multiple spaces
            return tweet_message
    except:
        pass


if __name__ == "__main__":
    api = authorization.my_auth()
    collect_tweets('finaluserlist_liberal')