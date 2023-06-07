import tweepy
from .sqlite_db import schemas

def auth(user: schemas.UserCredentials):
    client = tweepy.Client(bearer_token= user.twitter_bearer_token, consumer_key= user.consumer_key,
                           consumer_secret= user.consumer_secret, access_token= user.access_token,
                           access_token_secret= user.access_token_secret)
    res=client.get_me()
    '''after this i will try to get the id of the user from res and get the followers using get_user_follower() and return the result in list'''
    return res


