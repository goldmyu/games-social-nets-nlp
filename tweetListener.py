import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from time import sleep
from pymongo import MongoClient
import json
import config

MONGOHOST = "mongodb://localhost:27017/?serverSelectionTimeoutMS=5000&connectTimeoutMS=10000&3t.uriVersion=3&3t.connection.name=tweet"


class MyListener(StreamListener):
    def on_data(self,data):
        try:
            client = MongoClient(MONGOHOST)
            db = client.tweetGames

            tweet_json = json.loads(data)
            print(tweet_json)
            # reg_source = re.compile(r"href=.*(instagram|pinterest|Instagram|Pinterest|facebook|Facebook|tumblr|Tumblr).*>")
            # reg_entity = re.compile(r'instagram|pinterest|Instagram|Pinterest|facebook|Facebook|tumblr|Tumblr')

            # result = self.filter_tweets_by_network(tweet_json,"linkedin")
            #             if result:
            #                 print("Tweet Accepted {}".format(tweet_json["source"]))
            #                 db.social_tweets.insert(tweet_json)
            db.social_tweets.insert(tweet_json)
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):

        print(status)
        return True
##

auth = OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)

api = tweepy.API(auth)
# print("27.5")#
#

#

twitter_stream = Stream(auth, MyListener())
while True:
    try:
        #print(twitter_stream.filter(track=['pubg', '#pubg','Dota 2,#Dota_2','#Dota2','PUBG','league of legends','League of Legends','Fifa','Civilization VI','mikmak','Age of Empires','FarmVille','FarmVille2','Fortnite','#Fortnite','fortnite','#fortnite']),
        print(twitter_stream.filter(track=['Sims 4','the sims 4','sims4','The Sims 4','Sims_4','#the_sims_4','#sims4'],
              follow=['16582027','747807250819981312','103065157','3131144855','202159797',"3390728889","19397942","160952087","19017675","229466877","275799277","117777690","18807839","196994616","15010349","25073877","2797521996","704652692891820032","856010760","169426475","75223552","532247573","3131144855","375146901"],
              language='en'))
        #,follow=['747807250819981312','103065157','3131144855','202159797',"3390728889","19397942","160952087","19017675","229466877","275799277","117777690","18807839","196994616","15010349","25073877","2797521996","704652692891820032","856010760","169426475","75223552","532247573","3131144855","375146901"])
    except:
        print("err. but continues")
        sleep(3000) #sleep 5 minutes and try again

