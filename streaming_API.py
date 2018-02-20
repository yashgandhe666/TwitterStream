from __future__ import print_function
import tweepy
import json
from pymongo import MongoClient
from datetime import datetime
import time

WORDS = ['#bigdata', '#AI', '#datascience', '#machinelearning', '#ml', '#iot']

CONSUMER_KEY = "OQkuCo2DgoeZJt2sOIGnTj1YX"
CONSUMER_SECRET = "CwABj1XlhhLp4BOu4TBdVPBHPEe5w85oazKX52CgrTjEWKjmPd"
ACCESS_TOKEN = "636332324-0sD5nz0IpeZKAYPlxMbKa2rGk5OBT0lBCMtVOO3p"
ACCESS_TOKEN_SECRET = "q7pNaMSXKX5bpuJYZldNjSuSAk9I3xiUMv6L8o4KtqxkB"



class StreamListener(tweepy.StreamListener):    

    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")
 
    def on_error(self, status_code):
        print('An Error has occured: ' + repr(status_code))
        return False
 
    def on_data(self, data):
        try:
            client = MongoClient()
            #database name : db
            db = client['twitterdb']
            #data stored in data_json
            data_json = json.loads(data)
            
            #Data Extraction
            
            # created_at = data_json['created_at']
            created_at = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(data_json['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
            tweet_id = data_json['id_str']
            username = data_json['user']['screen_name']
            name = data_json['user']['name']
            followers = data_json['user']['followers_count']
            retweets = data_json['retweet_count']
            favourites = data_json['user']['favourites_count']
            statuses = data_json['user']['statuses_count']
            user_mentions = [m['screen_name'] for m in data_json['entities']['user_mentions']]
            text = data_json['text']
            hashtags = [tag['text'] for tag in data_json['entities']['hashtags']]
            language = data_json['lang']

            tweet = {'created_at':created_at, 'tweet_id':tweet_id, 'username':username, 'name':name, 'followers':followers, 'retweets':retweets, 'favourites':favourites, 'statuses':statuses, 'text': text, 'hashtags': hashtags, 'language' : language}
            #To show the tweet getting collected
            print("Tweet collected at " + str(created_at))
            
            #Store curated tweet data in collection: twitter_search
            db.twitter_search.insert(tweet)

        except Exception as e:
           print(e)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
#Set up the listener. The 'wait_on_rate_limit=True' is needed to help with Twitter API rate limiting.
listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True)) 
streamer = tweepy.Stream(auth=auth, listener=listener)
print("Tracking: " + str(WORDS))
streamer.filter(track=WORDS)
