import ast
import numbers
import os

import pandas as pd
import re  # regular expression
import preprocessor as p
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

import string
import json
import nltk

# nltk.download('punkt')

# =================================================================================================
# datasets_folder = 'data-sets/'
datasets_folder = '../../../../../work/twitter_data_games/'
clean_data_set_folder = datasets_folder + 'cleaned-data-sets/'

dataset_name = 'pubg.csv'

data = pd.read_csv(datasets_folder + dataset_name, usecols=['text', 'lang', 'truncated', 'extended_tweet'])
# data = pd.read_csv(datasets_folder + dataset_name, usecols=['text', 'lang'])
clean_data = pd.DataFrame(columns=['text'])
# =================================================================================================

# HappyEmoticons
emoticons_happy = {':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}', ':^)', ':-D', ':D', '8-D',
                   '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D', '=-3', '=3', ':-))', ":'-)", ":')", ':', ':^', '>:P',
                   ':-P', ':P', 'X-P', 'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)', '<3'}

# Sad Emoticons
emoticons_sad = {':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<', ':-[', ':-<', '=\\', '=/',
                 '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c', ':c', ':{', '>:\\', ';('}

# Emoji patterns
emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
# combine sad and happy emoticons
emoticons = emoticons_happy.union(emoticons_sad)


def clean_tweets(tweet):
    # after tweepy preprocessing the colon symbol left remain after      #removing mentions
    tweet = p.clean(tweet)
    tweet = tweet.lower()

    tweet = re.sub(r':', '', tweet)
    tweet = re.sub(r'‚Ä¶', '', tweet)
    tweet = re.sub(r'\'', '', tweet)
    tweet = re.sub(r'’', '', tweet)
    tweet = re.sub(r'\\"', '', tweet)
    tweet = re.sub(r'\.', '', tweet)
    tweet = re.sub(r'…', '', tweet)
    tweet = re.sub(r'\*', '', tweet)

    # replace consecutive non-ASCII characters with a space
    tweet = re.sub(r'[^\x00-\x7F]+', ' ', tweet)
    regex = re.compile('[^a-zA-Z ]')
    tweet = regex.sub('', tweet)
    # remove emojis from tweet
    tweet = emoji_pattern.sub(r'', tweet)
    # filter using NLTK library append it to a string
    filtered_tweet = []

    # looping through conditions
    word_tokens = word_tokenize(tweet)
    for w in word_tokens:
        # check tokens against stop words , emoticons and punctuations
        if w not in emoticons and w not in string.punctuation:
            filtered_tweet.append(w)

    return ' '.join(filtered_tweet)


p.set_options(p.OPT.URL, p.OPT.MENTION, p.OPT.EMOJI, p.OPT.SMILEY, p.OPT.RESERVED)


def write_df_to_csv(df):
    game_clean_csv = clean_data_set_folder + 'clean_' + dataset_name
    print('Saving cleaned tweet dataframe to csv : ' + game_clean_csv)
    if os.path.isfile(game_clean_csv):
        df.to_csv(game_clean_csv, mode='a', header=False, index=False)
    else:
        df.to_csv(game_clean_csv, index=False)


for i in range(data.shape[0]):
    if data['lang'][i] == 'en':
        before_clean = data['text'][i]
        extended_tweet = data['extended_tweet'][i]
        if not isinstance(extended_tweet, numbers.Number):
            extended_tweet = ast.literal_eval(extended_tweet)
        try:
            if data['truncated'][i] and bool(extended_tweet['full_text']):
                clean_tweet = clean_tweets(extended_tweet['full_text'])
                clean_data = clean_data.append({'text': clean_tweet}, ignore_index=True)
            else:
                clean_tweet = clean_tweets(data['text'][i])
                clean_data = clean_data.append({'text': clean_tweet}, ignore_index=True)
        except TypeError as e:
            print("During data cleaning an Error occurred at index {}\nError is : {}".format(i, e))
            clean_tweet = clean_tweets(data['text'][i])
            clean_data = clean_data.append({'text': clean_tweet}, ignore_index=True)

        if i % 10000 == 0:
            print('original tweet:\n' + before_clean + "\nCleaned Tweet:\n" + clean_tweet)
            write_df_to_csv(clean_data)
            clean_data = clean_data.iloc[0:0]

write_df_to_csv(clean_data)
print("\n\n\nFinished cleaning data for data-set : " + dataset_name)
