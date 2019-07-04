import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from time import sleep
import json
import config
import pandas as pd
import os

# =====================================================================================================================

games_dict = {
    "pubg": ['pubg', '#pubg', '#PUBGM', 'PUBG'],
    "dota": ['#Dota', '#Dota2', 'Dota', '#Dota_2', '#Dota2'],
    "LOL": ['league of legends', 'League of Legends', '#LeagueOfLegends', '#league_of_legends'],
    "fifa": ['Fifa', '#fifa'],
    "hearthstone": ['#Hearthstone', 'Hearthstone'],
    "fortnite": ['Fortnite', '#Fortnite', 'fortnite', '#fortnitestreamer', '#FortniteBattleRoyale',
        '#FortniteSeason9', '#FortniteWorldCup', '#FortniteProAM', '#fortnite'],
    "guildwars": ['#Guild Wars 2', '#GuildWars2', '#GW2', 'Guild Wars 2'],
    "sims": ['Sims 4', 'the sims 4', 'sims4', 'The Sims 4', 'Sims_4', '#the_sims_4', '#sims4', '#sims',
             '#TS4IslandLiving', 'simmer', '#TheSims4IslandLiving'],
    "wow": ['#WowClassic', 'WorldOfWarcraft', '#classicwow', '#WorldofWarcraft', '#vanillawow', '#wowvanilla',
            '#warcraft', '#wowstream', 'battle for azeroth', '#battleforazeroth'],
    "overwatch": ['Overwatch', '#Overwatch'],
    "HOTS": ['Heroes of the storm', '#Heroes_of_the_storm', '#hots', '#heroesofthestorm'],
    "minecraft": ['minecraft', '#minecraft'],
    "bloodstained": ['Bloodstained: Ritual of the Night', 'Bloodstained Ritual of the Night', '#Bloodstained',
                     '#BloodstainedRitualoftheNight'],
    "COD": ['Call of Duty : Black Ops 4', 'Call of Duty Black Ops 4', '#BlackOps4', '#BO4', '#CallOfDuty', '#COD']}

follow_ids = ['16582027', '61033129', '577401044', '425871040', '15411797', '708959670065631232', '997194164788842497',
              '719324795167309827', '176507184', '1604298906', '191636054', '140070953', '138372303', '1209608880',
              '816711729581158400', '67146159', '239970376', '47787563', '2420931980',
              '793477314793406465', '1861393146', '64565898', '214174332', '3253758956']

tweet_data_fields = ['created_at', 'id', 'id_str', 'text', 'source', 'truncated', 'in_reply_to_status_id',
                     'in_reply_to_status_id_str', 'in_reply_to_user_id', 'in_reply_to_user_id_str',
                     'in_reply_to_screen_name', 'user', 'geo', 'coordinates', 'place', 'contributors',
                     'quoted_status_id', 'quoted_status_id_str', 'quoted_status', 'quoted_status_permalink',
                     'is_quote_status', 'quote_count', 'reply_count', 'retweet_count', 'favorite_count', 'entities',
                     'favorited', 'retweeted', 'filter_level', 'lang', 'timestamp_ms']

# =====================================================================================================================

datasets_folder = 'data-sets/'
dump_to_csv_limit = 100
games_key_words = []
games_df_dict = {}


# =====================================================================================================================

def create_list_of_keywords():
    for game in games_dict.values():
        for game_key_word in game:
            games_key_words.append(game_key_word)


def create_games_df():
    for game_name, _ in games_dict.items():
        games_df_dict.update({game_name: pd.DataFrame(columns=tweet_data_fields)})


def get_game_from_tweet(tweet_data):
    for gameName, game_key_words in games_dict.items():
        for key_word in game_key_words:
            if (tweet_data['text'].lower()).find(key_word.lower()) >= 0:
                return gameName
    return -1


def write_df_to_csv(df, game_name):
    game_csv = datasets_folder + game_name + '.csv'
    if os.path.isfile(game_csv):
        df.to_csv(game_csv, mode='a', header=False, index=False)
    else:
        df.to_csv(game_csv, index=False)


def write_tweet_to_game_df(game_name, tweet_data):
    game_df = games_df_dict.get(game_name)
    games_df_dict[game_name] = game_df.append(tweet_data, ignore_index=True)
    if games_df_dict[game_name].shape[0] > dump_to_csv_limit:
        write_df_to_csv(games_df_dict[game_name], game_name)
        games_df_dict[game_name] = games_df_dict[game_name].iloc[0:0]
        print("Flushed tweets from df to CSV file of game : {}".format(game_name))


class MyListener(StreamListener):
    def on_data(self, data):
        try:
            tweet_json = json.loads(data)
            game_name = get_game_from_tweet(tweet_json)
            if game_name != -1:
                write_tweet_to_game_df(game_name, tweet_json)

        except BaseException as e:
            print("Error on_data: %s" % str(e))

        return True

    def on_error(self, status):
        print(status)
        return True


auth = OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth)
twitter_stream = Stream(auth, MyListener())

create_list_of_keywords()
create_games_df()

while True:
    try:
        twitter_stream.filter(track=games_key_words, follow=follow_ids)
    except:
        print("err. but continues")
        sleep(1000)  # sleep 5 minutes and try again
