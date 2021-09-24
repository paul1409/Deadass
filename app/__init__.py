from flask import Flask, render_template, request, redirect, url_for
import configparser
import tweepy


# authorization
app = Flask(__name__)

import sys

import configparser

config = configparser.ConfigParser()

config.read("config.ini")

consumer_key = config["TWITTER"]["CONSUMER_KEY"]
consumer_secret = config["TWITTER"]["CONSUMER_SECRET"]
access_token = config["TWITTER"]["ACCESS_TOKEN"]
access_token_secret = config["TWITTER"]["ACCESS_TOKEN_SECRET"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

me = api.me()
name = me.screen_name


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        if app.config["TESTING"] == False:
            content = request.form["content"]
            new_status = api.update_status(content)
            print(content)

    tweets = api.user_timeline(name)
    return render_template("index.html", name=name, tweets=tweets)


@app.route("/tweet:<id>", methods=["GET", "POST"])
def get_single_tweet(id):
    tweet = [api.get_status(id)]
    return render_template("index.html", tweets=tweet)


@app.route("/status", methods=["GET", "POST"])
def post_status():
    return render_template("post_status.html", name=name)


@app.route("/remove_status:<id>", methods=["GET", "POST"])
def get_status(id):
    if app.config["TESTING"] == False:
        print(id)
        api.destroy_status(id)
    return redirect("/")
