import praw
import configparser
import pandas as pd
import datetime as dt

game= 'FUTMobile'
def get_date(created):
    return dt.datetime.fromtimestamp(created)

def reply_and_nested_reply( comment):
    if (len(comment.replies._comments) > 0):
        for reply in comment.replies._comments:
            topics_dict["title"].append(submission.title)
            topics_dict["author"].append(reply.author)
            topics_dict["score"].append(reply.score)
            topics_dict["id"].append(reply.id)
            topics_dict["url"].append("")
            topics_dict["comms_num"].append("")
            topics_dict["created"].append(reply.created)
            topics_dict["body"].append(reply.body)
            topics_dict["shortlink"].append(reply.permalink)
            topics_dict["type"].append("reply")
            bag_of_text.append(reply.body)
            reply_and_nested_reply( reply)


config = configparser.ConfigParser()
config.read("..\credentials.ini")

reddit = praw.Reddit(client_id=config['REDDIT']['personal_use_script'],
                     client_secret=config['REDDIT']['secret'],
                     user_agent=config['REDDIT']['script_name'],
                     username=config['REDDIT']['username'],
                     password=config['REDDIT']['password'])

print(reddit.user.me())
subreddit = reddit.subreddit('pubg')
# top_subreddit = subreddit.search('israel')
# top_subreddit = subreddit.search("fortnite")
topics_dict = { "title":[], \
                "author":[], \
                "score":[], \
                "id":[], "url":[], \
                "comms_num": [], \
                "created": [], \
                "body":[], \
                "shortlink":[], \
                "type":[]}
bag_of_text=[]
# for submission in top_subreddit:
for submission in subreddit.hot(limit=100000):
    print(submission.title, submission.id)
    submission.comments.replace_more(limit=0)

    topics_dict["title"].append(submission.title)
    topics_dict["author"].append(submission.author)
    topics_dict["score"].append(submission.score)
    topics_dict["id"].append(submission.id)
    topics_dict["url"].append(submission.url)
    topics_dict["comms_num"].append(submission.num_comments)
    topics_dict["created"].append(submission.created)
    topics_dict["body"].append(submission.selftext)
    topics_dict["shortlink"].append(submission.shortlink)
    topics_dict["type"].append("topic")
    bag_of_text.append(submission.title)
    bag_of_text.append(submission.selftext)
    for comment in submission.comments._comments:
        topics_dict["title"].append(submission.title)
        topics_dict["author"].append(comment.author)
        topics_dict["score"].append(comment.score)
        topics_dict["id"].append(comment.id)
        topics_dict["url"].append("")
        topics_dict["comms_num"].append("")
        topics_dict["created"].append(comment.created)
        topics_dict["body"].append(comment.body)
        topics_dict["shortlink"].append(comment.permalink)
        topics_dict["type"].append("comment")
        bag_of_text.append(comment.body)
        reply_and_nested_reply(comment)



subreddit = reddit.subreddit('all')
top_subreddit = subreddit.search(game)

for submission in top_subreddit:
    print(submission.title, submission.id)
    submission.comments.replace_more(limit=0)

    topics_dict["title"].append(submission.title)
    topics_dict["author"].append(submission.author)
    topics_dict["score"].append(submission.score)
    topics_dict["id"].append(submission.id)
    topics_dict["url"].append(submission.url)
    topics_dict["comms_num"].append(submission.num_comments)
    topics_dict["created"].append(submission.created)
    topics_dict["body"].append(submission.selftext)
    topics_dict["shortlink"].append(submission.shortlink)
    topics_dict["type"].append("topic")
    bag_of_text.append(submission.title)
    bag_of_text.append(submission.selftext)
    for comment in submission.comments._comments:
        topics_dict["title"].append(submission.title)
        topics_dict["author"].append(comment.author)
        topics_dict["score"].append(comment.score)
        topics_dict["id"].append(comment.id)
        topics_dict["url"].append("")
        topics_dict["comms_num"].append("")
        topics_dict["created"].append(comment.created)
        topics_dict["body"].append(comment.body)
        topics_dict["shortlink"].append(comment.permalink)
        topics_dict["type"].append("comment")
        bag_of_text.append(comment.body)
        reply_and_nested_reply(comment)



topics_data = pd.DataFrame(topics_dict)
_timestamp = topics_data["created"].apply(get_date)

topics_data = topics_data.assign(timestamp = _timestamp)
topics_data.to_csv(game + '.csv', index=False)

text_data = pd.DataFrame(bag_of_text)
text_data.to_csv(game + '_text.csv', index=False)