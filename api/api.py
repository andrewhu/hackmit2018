from flask import Flask, request, redirect, jsonify, render_template
from flask_cors import CORS
from helpers import *

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return render_template("api.html")


@app.route("/tweets/")
def tweets():
    points = get_all_florence_tweets()
    data = []
    for p in points:
        lat, lng = p[3].split(',')

        elem = {
            'id': p[0],
            'tweet_id': p[1],
            'date': p[2],
            'lat': float(lat),
            'lng': float(lng),
            'body': p[4],
            'sentiment': p[5],
            'weight': p[6]
        }
        data.append(elem)
    return jsonify(data)


@app.route("/coords/")
def coords():
    all_tweets = get_all_florence_tweets()
    data = []
    for tweet in all_tweets:
        lat, lng = tweet[3].split(',')
        coord = {'lat': float(lat),
                 'lng': float(lng),
                 'weight': tweet[6]}
        data.append(coord)
    return jsonify(data)


@app.route("/sentiment/")
def sentiment():
    all_tweets = get_all_florence_tweets()
    for tweet in all_tweets:
        tweet.append(get_sentiment(tweet[4]))
    return jsonify(dat)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
