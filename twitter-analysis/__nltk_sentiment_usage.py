import sys
import os
import nltk
import re
import string
import random

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



def nltk_downloader():
    nltk.download('twitter_samples')
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('stopwords')
    nltk.download('vader_lexicon')

def fetch_twitter_samples():

    positive_tweets = twitter_samples.strings('positive_tweets.json')
    negative_tweets = twitter_samples.strings('negative_tweets.json')
    text = twitter_samples.strings('tweets.20150430-223406.json')

    return positive_tweets, negative_tweets, text

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

def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token

def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)

def get_custom_input():
    print('Type your Custom Text to be analyzed and press Enter:')
    custom_input = input()
    # custom_input = "Many positive vibes. Yeah :)"
    print('Thanks. Your Text is "%s".\nThe Model will be trained first, afterwards your input will be analyzed. This could take some time.' %custom_input)

    return str(custom_input)

def get_train_test_data(positive_cleaned_tokens_list, negative_cleaned_tokens_list):

    positive_dataset = [(tweet_dict, "Positive") for tweet_dict in get_tweets_for_model(positive_cleaned_tokens_list)]
    negative_dataset = [(tweet_dict, "Negative") for tweet_dict in get_tweets_for_model(negative_cleaned_tokens_list)]

    dataset = positive_dataset + negative_dataset

    random.shuffle(dataset)

    train_data = dataset[:int((len(dataset) * 0.7))]
    test_data = dataset[int((len(dataset) * 0.7)):]

    return train_data, test_data


def get_model_classifier(train_data, test_data, classifier_type):

    classifier = classifier_type.train(train_data)

    print("Accuracy is:", classify.accuracy(classifier, test_data))
    print(classifier.show_most_informative_features(10))

    return classifier

def main():
    custom_input = get_custom_input()
    stop_words = stopwords.words('english')
    custom_tokens = remove_noise(word_tokenize(custom_input), stop_words)

    nltk_downloader()
    
    sid = SentimentIntensityAnalyzer()

    print("")
    print("1: Sentiment Intensity Analysis: poitive, negative, neutral percentages")
    print("Sentiment Intensity without noise removal")
    ss = sid.polarity_scores(custom_input)
    for k in sorted(ss):
        print('{0}: {1}, '.format(k, ss[k]), end='')
    print()

    print("Sentiment Intensity with noise removal")
    ss = sid.polarity_scores(" ".join(custom_tokens))
    for k in sorted(ss):
        print('{0}: {1}, '.format(k, ss[k]), end='')
    print()

    print("")
    print('2: Basic Sentiment Analysis: Only Positive or Negative')
    positive_tweets, negative_tweets, text = fetch_twitter_samples()

    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

    positive_cleaned_tokens_list = list()
    negative_cleaned_tokens_list = list()

    for tokens in positive_tweet_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    for tokens in negative_tweet_tokens:
        negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    freq_dist_pos = FreqDist(get_all_words(positive_cleaned_tokens_list))
    freq_dist_neg = FreqDist(get_all_words(negative_cleaned_tokens_list))

    train_data, test_data = get_train_test_data(positive_cleaned_tokens_list, negative_cleaned_tokens_list)

    classifier = get_model_classifier(train_data, test_data, NaiveBayesClassifier)

    print("Result: ", classifier.classify(dict([token, True] for token in custom_tokens)))


if __name__ == '__main__':
    main()