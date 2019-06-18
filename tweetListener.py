import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from time import sleep
import json
import config
import pandas as pd

games_dict = {
    "pubg": ['pubg', '#pubg', '#PUBGM', 'PUBG'],
    "dota": ['#Dota', '#Dota2', 'Dota', '#Dota_2', '#Dota2'],
    "LOL": ['league of legends', 'League of Legends', '#LeagueOfLegends', '#league_of_legends'],
    "fifa": ['Fifa', '#fifa'],
    "hearthstone": ['#Hearthstone', 'Hearthstone'],
    "fortnite": ['Fortnite', '#Fortnite', 'fortnite', '#fortnitestreamer', '#FortniteBattleRoyale', '#FortniteSeason9',
                 '#FortniteWorldCup', '#FortniteProAM', '#fortnite'],
    "guildwars": ['#Guild Wars 2', '#GuildWars2', '#GW2', 'Guild Wars 2'],
    "sims": ['Sims 4', 'the sims 4', 'sims4', 'The Sims 4', 'Sims_4', '#the_sims_4', '#sims4', '#sims'],
    "wow": ['#WowClassic', 'WorldOfWarcraft', '#classicwow', '#WorldofWarcraft', '#vanillawow', '#wowvanilla',
            '#warcraft', '#wowstream'],
    "overwatch": ['Overwatch', '#Overwatch'],
    "HOTS": ['Heroes of the storm', '#Heroes of the storm', '#hots', '#heroesofthestorm'],
    "minecraft": ['minecraft', '#minecraft'],
    "bloodstained": ['Bloodstained: Ritual of the Night', 'Bloodstained Ritual of the Night', '#Bloodstained',
                     '#BloodstainedRitualoftheNight'],
    "COD": ['Call of Duty : Black Ops 4', 'Call of Duty Black Ops 4', '#BlackOps4', '#BO4', '#CallOfDuty', '#COD']}

follow_ids = ['16582027', '61033129','577401044','425871040','15411797']

games_key_words = []
games_df = []


def create_list_of_keywords():
    for game in games_dict.values():
        for game_key_word in game:
            games_key_words.append(game_key_word)


def create_games_df():
    for game in games_dict.values():
        games_df.append(pd.DataFrame(columns=['Name', 'Age']))


def game_csv_num(tweet_data):
    # check which game this data belong to.
    for idx, keyWord in enumerate(games_key_words):
        if tweet_data.find(keyWord):
            return idx
    return -1


def write_to_df_num(game_number, tweet_data):
    # TODO add tweet_data to DF that belong to him.
    # TODO if one of the dataframes bigger than 1000 add it to CSV and clean that dataFrame
    return


class MyListener(StreamListener):
    def on_data(self, data):
        try:
            tweet_json = json.loads(data)
            gameNumber = game_csv_num(tweet_json)
            write_to_df_num(gameNumber, tweet_json)

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
        twitter_stream.filter(track=games_key_words, follow=follow_ids, languages='en')

    except:
        print("err. but continues")
        sleep(3000)  # sleep 5 minutes and try again
