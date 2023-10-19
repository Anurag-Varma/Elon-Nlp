import tweepy
import configparser
import pandas as pd
import pickle
import time
from tweepy import *
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import numpy as np
import os


def sentiment(val):
    if val>=0.8:
        return "Highly Positive"
    elif val>=0.3 and val<0.8:
        return "Positive"
    elif val>=-0.3 and val<0.3:  
        return "Neutral"
    elif val>=0.8 and val<-0.3:
        return "Negative"
    elif val<-0.8:
        return "Highly Negative"

config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']
access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


f = open('store.pckl', 'rb')
previousID = pickle.load(f)
f.close()

user = 'PAnuragVarma'
limit=300
columns = ['User', 'Tweet' ,'Date', 'Likes', 'Retweets', 'Id', 'Mentions'] 
Dict={'neg':"negative",'pos':"positive",'neu':"neutral"}


while(1):
    tweets = tweepy.Cursor(api.user_timeline, screen_name=user, count=200, tweet_mode='extended').items(limit)
    data = []

    for tweet in tweets:
        data.append([tweet.user.screen_name, tweet.full_text, tweet.created_at, tweet.favorite_count, tweet.retweet_count, tweet.id, tweet.entities['user_mentions']])

    df = pd.DataFrame(data, columns=columns)

    idList=[]
    for i in df.iterrows():
        idList.append(i[1]['Id'])

    tweetPreset=1
    try:
        newIndex=idList.index(previousID)
        print(newIndex)
    except Exception as e:
        newIndex=0
        tweetPreset=0

    flag=0
    if newIndex>0 or tweetPreset==0:
        count=0
        for i in df.iterrows():
            tweetId=i[1]['Id']
            if flag==0:
                topTweetId=tweetId
                flag=1
            tweetUserName=i[1]['User']
            tweetText=i[1]['Tweet']
            output=SentimentIntensityAnalyzer().polarity_scores(tweetText)
            tweetSentiment=sentiment(output['compound'])

            print(tweetUserName)
            print(tweetText)
            print(output)
            print("\n")

            y = []
            mylabels = []
            if output['pos']>0:
                    y.append(output['pos'])
                    mylabels.append(Dict['pos'])
            if output['neg']>0:
                    y.append(output['neg'])
                    mylabels.append(Dict['neg'])
            if output['neu']>0:
                    y.append(output['neu'])
                    mylabels.append(Dict['neu'])

            plt.pie(y, labels = mylabels,autopct='%1.1f%%', startangle=90)
            plt.title('Tweet Sentiment Analysis')
            plt.savefig('sentiment.png')

            try:
                media = api.media_upload("sentiment.png")
                reply_status = "@%s %s %s %s %s" % (tweetUserName, " The tweet : \"", tweetText,"\" has a Sentiment Analysis of : ", tweetSentiment)
                api.update_status(reply_status,in_reply_to_status_id=tweetId, auto_populate_reply_metadata= True,media_ids=[media.media_id])
            except Exception as e:
                print(e)
                print("\n")

            os.remove('sentiment.png')
            plt.clf()
            time.sleep(30)

            count+=1
            if count>=newIndex:
                break

        f = open('store.pckl', 'wb')
        pickle.dump(topTweetId, f)
        f.close()
        previousID=topTweetId

    time.sleep(60)



