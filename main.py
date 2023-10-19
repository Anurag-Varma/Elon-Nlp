import twitter
import tweepy
from tweepy import *
from twitter import *
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import numpy as np
import time

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

api_key = "oUM5fKKQ4FEpKTN6Pl12SaaOY"
api_key_secret = "3o0KC8YcjgnuGmwMojfUBWfbArGIrzxy8A2EK9DvWH1VSJOW7l"
access_token = "1523901817343868928-Lwd3WQwDVsqeJpIPt6V5jIMSb8j0kE"
access_token_secret = "utIp7cMZZojLbp8ND9uj0AkIdZrG3BlFA70srStsMu3LL"
twitter = Twitter(auth=OAuth2(bearer_token="AAAAAAAAAAAAAAAAAAAAAPu5cQEAAAAAI9PjOt5aBnwXTGdiDxBhB%2BPjmXM%3DI9kR0qImnutowUSuqcJ9lAyKDgghlHr92wdJjjibW9sh93d4sf"))


Q=['elon','elon musk']
Dict={'neg':"negative",'pos':"positive",'neu':"neutral"}

for i in range(5):
    x=twitter.search.tweets( q=Q, tweet_mode='extended')

    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)


    tweetId = x['statuses'][0]['id']
    tweetUserName=x["statuses"][0]["user"]["screen_name"]
    tweetText=x["statuses"][0]["full_text"]
    output=SentimentIntensityAnalyzer().polarity_scores(tweetText)
    tweetSentiment=sentiment(output['compound'])

    print(tweetUserName)
    print(tweetText)
    print(output)
    print("\n")


    y = []
    mylabels = []
    for i in output:
        if output[i]>0 and i!='compound':
            y.append(output[i])
            mylabels.append(Dict[i])
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

    time.sleep(60)
