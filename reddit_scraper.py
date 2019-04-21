import praw
import configparser

config = configparser.ConfigParser()
config.read("credentials.ini")

reddit = praw.Reddit(client_id=config['REDDIT']['personal_use_script'],
                     client_secret=config['REDDIT']['secret'],
                     user_agent=config['REDDIT']['script_name'],
                     username=config['REDDIT']['username'],
                     password=config['REDDIT']['password'])

print(reddit.user.me())
