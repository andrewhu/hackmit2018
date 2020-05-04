from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import sqlite3
from flask import Flask, request, redirect, jsonify
from helpers import *

app = Flask(__name__)

# Variables that contains the user credentials to access Twitter API
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""


# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        datajson = json.loads(data)
        try:
            if 'place' not in datajson:
                return
            if datajson['place'] is not None:
                print(datajson['place'])
                tweet_id_ = datajson['id']
                created_at_ = datajson['created_at']
                coords_raw = datajson['place']['bounding_box']['coordinates'][0][0]
                coords_ = str(coords_raw[1]) + ", " + str(coords_raw[0])
                body_ = datajson['text']
                if 'florence' in body_.lower() or 'hurricane' in body_.lower() or 'storm' in body_.lower():
                    conn = sqlite3.connect("tweets.sqlite")
                    c = conn.cursor()
                    sentiment = get_sentiment(body_)
                    sql = "INSERT INTO tweets(tweet_id, created_at, coords, body, sentiment) VALUES (?,?,?,?,?)"
                    c.execute(sql, (tweet_id_, created_at_, coords_, body_,sentiment))
                    conn.commit()
                    conn.close()
        except Exception as e:
            print(e)
            pass

        return True

    def on_error(self, status):
        print(status)


#
if __name__ == '__main__':
    # This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track=['hurricane', 'florence', 'storm'])
