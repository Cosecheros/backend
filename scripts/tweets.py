from firebase_admin import firestore
from datetime import datetime
import re

fdb = firestore.Client()

def get_data_with_day(date):
    data = []
    ref = fdb.collection("tweets_v2").get()
    for cosecha in ref:
        tweet = cosecha.to_dict()
        tw_date = tweet.get("date")
        if type(tw_date) == str:
            tw_datetime = datetime.strptime(tw_date, "%Y-%m-%d %H:%M:%S")
        else:
            tw_datetime = tw_date
        if tw_datetime.date() == date.date():
            data.append(tweet)
    return data

def get_data():
    data = []
    ref = fdb.collection("tweets_v2").get()
    for cosecha in ref:
        tweet = cosecha.to_dict()
        data.append(tweet)
    return data

def flatten_tweets(data):
    flattened = []
    for tweet in data:
        date = tweet.get("date")
        screen_name = tweet.get("screen_name")
        text = tweet.get("text")
        inundaciones = re.search("(?i)(\W|^)(granizo|granizos)(\W|$)", str(text))
        if not inundaciones:
            continue
        if "places" in tweet:
            places = tweet.get("places")
            if type(places) == list:
                for place in places:
                    lat = place.get("lat")
                    lon = place.get("lon")
                    alias = place.get("alias")
                    flattened_tweet = {"fecha": date, "usuario": screen_name, "texto": text, "alias": alias,"lat": lat, "lon": lon}
                    flattened.append(flattened_tweet)
    return flattened

def get_flat_tweets(fecha):
    date_format = "%d-%m-%Y"
    datetime_obj = datetime.strptime(fecha, date_format)
    date_str = datetime_obj.strftime(date_format)
    data = get_data_with_day(datetime_obj)
    flattened_tweets = flatten_tweets(data=data)
    return flattened_tweets