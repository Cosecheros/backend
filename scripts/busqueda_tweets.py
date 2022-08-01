import tweepy
import json
import re
import spacy
import requests
import urllib
from google.api_core.exceptions import InvalidArgument
from datetime import datetime
from dateutil import tz
from google.cloud import firestore
from google.cloud import storage

# Instancing key, token from Twitter developer
consumer_key = ""
consumer_secret = ""

access_token = ""
access_token_secret = ""

#Initializing the API
auth_tw = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth_tw.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth_tw, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Instancing the Database
db = firestore.Client()
# This list is to avoid saving the same tweets multiple times. 
saved_tweets = []

# INTA Radares
radares = {
    "Pergamino": "-33.8358155353661,-60.5450748689576,400km",
    "Parana": "-31.74452564012187,-60.513421293468966,400km",
    "Cordoba": '-31.4173391,-64.183319,400km',
    "Neuquen": '-38.94815609842747,-68.09935336935173,400km',
    "Resistencia": '-27.5954104255766,-59.1446432497471,400km',
    "Las Lomitas": '-24.7102155246944,-60.598287756527,400km',
    "Ezeiza": '-34.8758213531443,-58.5648395364287,400km',
    "Bariloche": '-41.1225978897056,-71.3797361980635,400km',
    "Anguil": '-36.5543101532231,-64.045242126436,400km',
    "San Rafael": '-34.62125757706778, -68.33242255962756,400km',
    "La Carlota": '-33.420768345626435, -63.29628799262556, 400km' 
    }


def utc_to_local_date(created_at):
    '''
    Transform a UTC date to local time zone date
    '''
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    tw_date_format = '%a %b %d %H:%M:%S %z %Y'
    utc = datetime.strptime(created_at, tw_date_format)
    utc = utc.replace(tzinfo=from_zone)
    central = utc.astimezone(to_zone)
    return central


def post_tweet_in_db(tweet_data):
    print(tweet_data)
    try:
        id = str(tweet_data.pop("tweet_id"))
        db.collection("dev_tweets").document(id).set(tweet_data)
    except requests.exceptions.HTTPError:
        print("HTTP Error")
    except InvalidArgument:
        print("400 Cannot convert an array value in an array value.")


def get_coordinates(endpoint, nombre, **kwargs):
    '''
    Get coordinates from Gob AR database
    '''
    API_BASE_URL = "https://apis.datos.gob.ar/georef/api/"
    kwargs["nombre"] = nombre
    url = "{}{}?{}".format(API_BASE_URL, endpoint, urllib.parse.urlencode(kwargs))
    req = requests.get(url).json()
    return req[endpoint]


def extract_locations(full_text):
    '''
    Extract locations using spacy NER(named entity recognition)
    '''
    tweet_locations = []
    nlp = spacy.load("es_core_news_sm")
    tweet = nlp(full_text)
    for ent in tweet.ents:
        if ent.label_ == "LOC":
            tweet_locations.append(ent.text)
    return tweet_locations


def get_location_coordinates(locations):
    '''
    Get locations coordinates from a list of locations
    '''
    locations_coordinates = []
    for location in locations:
        location.replace("[^A-Za-z]", "")
        try: 
            result = get_coordinates(endpoint="municipios", nombre=location)
            if result != []:
                place = result[0]
                coordinates = {"alias": location, "lon": place["centroide"]["lon"], "lat": place["centroide"]["lat"]}
                locations_coordinates.append(coordinates)
        except KeyError:
            print("keyError")
            continue
    return locations_coordinates

def event_type(text):
    granizo = re.search("granizo", text)
    inundaciones = re.search("inundacion|inundaciones|anegamiento", text)
    helada = re.search("helada|heladas", text)
    if granizo:
        return "granizo"
    elif inundaciones:
        return "inundaciones"
    else:
        return "helada"

# def build_proccessed_tweet(data, locations, tw_place):
    

def proccess_tweet(tweet):
    '''
    Extract important data from the tweet
    '''
    text = tweet._json['full_text']
    e_type=event_type(text)
    avisos = re.search("(^Aviso|^Alerta)", text)
    screen_name = tweet._json["user"]["screen_name"]
    tweet_id = tweet._json["id"]
    date = utc_to_local_date(tweet._json['created_at'])
    place = tweet._json['place']
    locations = extract_locations(full_text=text)
    if locations != []:
        coordinates = get_location_coordinates(locations=locations)
        if coordinates != []:
            data = {"screen_name": screen_name, "tweet_id": tweet_id, "date": date, "text": text,
                    "places": coordinates, "tw_place": place, "event_type": e_type}
        else:
            data = {"screen_name": screen_name, "tweet_id": tweet_id, "date": date, "text": text,
                    "tw_place": place, "event_type": e_type}
    else:
        data = {"screen_name": screen_name, "tweet_id": tweet_id, "date": date, "text": text, "event_type": e_type}
    return data

def tw_search(keyword, date, geocode):
    '''
    Search by keyword, date and geocode
    '''
    count = 0
    for tweet in tweepy.Cursor(api.search,
                               q=keyword,
                               geocode=geocode,
                               lang='es',
                               tweet_mode="extended").items(6000):
        tw_date = utc_to_local_date(tweet._json['created_at'])
        if date.date() == tw_date.date():
            txt = tweet._json.get('full_text')
            retweeted = re.search("^RT", txt)
            tweet_id = tweet._json["id"]
            if not retweeted and tweet_id not in saved_tweets:
                count += 1
                data = proccess_tweet(tweet=tweet)
                post_tweet_in_db(tweet_data=data)
    return count


def main(req):
    keyword = "granizo OR inundacion OR inundaciones OR anegamiento OR anegamiento OR incendio OR nevada"
    date = datetime.now()
    for radar in radares:
        amount_tweets_saved = tw_search(keyword=keyword, date=date, geocode=radares[radar])
        print("De", radar, "se guardaron", amount_tweets_saved, "tweets")
    
        
main(req="")

