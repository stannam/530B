import authorization


class TweepError(Exception):
    pass


def twitusers(input):
    """
    This function is for getting screen_names of the twitter users.
    The input should be a list of twitter user ids.
    The output is a file named 'finaluserlist.txt' and 'errorlist.txt'
    On 'finaluserlist.txt', I manually removed accounts that meets specific
    criteria. For example, accounts with screen_name that contains specific words. (The set of words are not provided
    here. Please refer to the paper.)
    """
    api = authorization.my_auth()
    with open('finaluserlist.txt', 'w', encoding='utf-8') as f:
        f.write(
            "userID" + "\t" + "name" + "\t" + "screen_name" + "\t" + "followers_count" + "\t" + "following_count" + "\t" + "# of tweets" + "\t" + "lang" + "\n")
    with open('errorID.txt', 'w', encoding='utf-8') as f:
        f.write("")

    for uid in input:
        try:
            user_data = api.get_user(int(uid))
            if user_data.followers_count < 1000 and user_data.protected is False:
                userID = user_data.id_str
                name = user_data.name
                screen_name = user_data.screen_name
                followers_count = str(user_data.followers_count)
                following_count = str(user_data.friends_count)
                statuses_count = str(user_data.statuses_count)
                language = user_data.lang
                print(name+"\n")
                with open('finaluserlist.txt', 'a', encoding='utf-8') as f:
                    f.write(
                        userID + "\t" + name + "\t" + screen_name + "\t" + followers_count + "\t" + following_count + "\t" + statuses_count + "\t" + language + "\n")
        except:
            with open('errorID.txt', 'a') as f:
                f.write(uid + "\n")
