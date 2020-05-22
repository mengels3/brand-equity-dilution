import sys
import os
import nltk
import re
import string
import random
import pymongo
import config
import statistics
import datetime

import matplotlib.pyplot as plt

from database_client import DatabaseClient

from nltk import FreqDist
from nltk import classify
from nltk import NaiveBayesClassifier

from nltk.tag import pos_tag

from nltk.corpus import stopwords
from nltk.corpus import subjectivity
from nltk.corpus import twitter_samples

from nltk.tokenize import word_tokenize

from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from nltk.stem.wordnet import WordNetLemmatizer

from pymongo import MongoClient


def nltk_downloader():
    nltk.download('twitter_samples')
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('stopwords')
    nltk.download('vader_lexicon')

def get_tweets(keyword):
    dbClient = DatabaseClient()

    tweets = dbClient.getAllDocuments(keyword)
    print("Currently there are %s tweets stored in the database collection '%s'." %(str(len(tweets)), keyword))

    max_id = max(list(map(lambda tweet: int(tweet['id_str']), tweets)))
    print("Id of latest fetched tweet is %s." %str(max_id))

    return tweets


def remove_noise(tweet_tokens, stop_words):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens


def get_sentiment_of_tweet(tweet, neg, neu, pos):

    stop_words = stopwords.words('english')
    cleaned_tweet = remove_noise(word_tokenize(tweet), stop_words)
    
    sid = SentimentIntensityAnalyzer()

    ss = sid.polarity_scores(" ".join(cleaned_tweet))

    neg.append(ss['neg'])
    neu.append(ss['neu'])
    pos.append(ss['pos'])

    return neg, neu, pos

def main():
    nltk_downloader()
    brands = ['audi', 'volkswagen', 'mercedes']
    keywords = ['audi', 'audi_etron', 'volkswagen', 'volkswagen_id3', 'mercedes', 'mercedes_eqc']

    for b in brands:
        results = dict()
        for kw in keywords:
            if b in kw:
                print("Sentiment Intensity Analysis with noise removal for \"%s\": poitive, negative, neutral percentages" %kw)
                tweets = False

                results[kw] = dict()
                
                while not tweets:
                    try:
                        tweets = get_tweets(kw)
                    except:
                        tweets = False

                neg, neu, pos = list(), list(), list()

                for tweet in tweets:
                    if tweet['lang'] == 'en':
                        date = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y').date()
                        try:
                            x = results[kw][date]
                        except KeyError:
                            results[kw][date] = dict()
                            results[kw][date]['neg'] = list()
                            results[kw][date]['neu'] = list()
                            results[kw][date]['pos'] = list()
                        results[kw][date]['neg'], results[kw][date]['neu'], results[kw][date]['pos'] = get_sentiment_of_tweet(tweet['full_text'], results[kw][date]['neg'], results[kw][date]['neu'], results[kw][date]['pos'])

                # neg_avg = sum(neg) / len(neg)
                # neu_avg = sum(neu) / len(neu)
                # pos_avg = sum(pos) / len(pos)

                # neg_med = statistics.median(neg)
                # neu_med = statistics.median(neu)
                # pos_med = statistics.median(pos)

                # print("%s:\n\tAverages: neg= %s, neu= %s, pos= %s, count= %s\n\tMedian: neg= %s, neu= %s, pos=%s\n" %(kw, str(neg_avg), str(neu_avg), str(pos_avg), str(len(neg)), str(neg_med), str(neu_med), str(pos_med)))


                # Pie chart, where the slices will be ordered and plotted counter-clockwise:
                # labels = 'neg', 'neu', 'pos'
                # sizes = [neg_avg, neu_avg, pos_avg]

                # fig1, ax1 = plt.subplots()
                # ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
                # ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

                # plt.show()

            # negativity of tweets:

        x_axis_vals = dict()
        y_axis_vals = dict()
        vals = dict()
        for kw in results:
            x_axis_vals[kw] = list()
            y_axis_vals[kw] = list()

            for date in sorted(results[kw]):
                neg_avg = sum(results[kw][date]['neg']) / len(results[kw][date]['neg'])
                y_axis_vals[kw].append(neg_avg)
                x_axis_vals[kw].append(str(date))

        print(x_axis_vals[list(x_axis_vals.keys())[0]])
        print(y_axis_vals[list(y_axis_vals.keys())[0]])
        print(x_axis_vals[list(x_axis_vals.keys())[1]])
        print(y_axis_vals[list(y_axis_vals.keys())[1]])


        plt.plot(x_axis_vals[list(x_axis_vals.keys())[1]], y_axis_vals[list(y_axis_vals.keys())[1]], 'r--', x_axis_vals[list(x_axis_vals.keys())[0]], y_axis_vals[list(y_axis_vals.keys())[0]], 'b--')
        plt.show()

if __name__ == '__main__':
    main()