import nltk
from database_client import DatabaseClient
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import matplotlib.pyplot as plt
import string
import re


# sentence = "@potheadphrog777 @shaken_pie @Linked_Caleb Random guy in Audi.\nI tend to believe him 😂 https://t.co/K0pedGq7Vc"
# # if retweet remove 'RT' at beginning
# if sentence.startswith('RT'):
#     sentence = sentence[2:]
# # remove line breaks
# sentence = re.sub(r'[\n]+', ' ', sentence)
# # remove all @-handles such as @sam_harris
# sentence = re.sub(r'(@[^\s]+)', '', sentence)
# # remove all non alphanumeric chars
# sentence = re.sub(r'[^A-Za-z0-9 ]+', '', sentence)
# # remove all leading and trainling whitespace or tabs
# sentence = sentence.strip()
# print('cleaned: ' + sentence)

# # POS tagging and filtering for nouns
# tokens = nltk.word_tokenize(sentence.lower())
# tokens = list(filter(lambda token: not str(token).startswith('http'), tokens))
# print('tokens: ' + str(tokens))
# tagged = nltk.pos_tag(tokens)
# print('pos_tagged: ' + str(tagged))
# nouns = list(filter(lambda taggedWord: taggedWord[1] == 'NN' or taggedWord[1]
#                     == 'NNS' or taggedWord[1] == 'NNP' or taggedWord[1] == 'NNPS', tagged))
# nouns = list(map(lambda noun: noun[0], nouns))
# stop_words = set(stopwords.words('english'))
# filtered_nouns = [w for w in nouns if not w in stop_words]

# lem = WordNetLemmatizer()
# lemmatized_nouns = list(
#     map(lambda noun: lem.lemmatize(noun), filtered_nouns))
# print('lemmatized_nouns: ' + str(lemmatized_nouns))

def calculateTermFrequency(dbClient, collection):
    # 1. get all tweets
    tweets = dbClient.getAllDocuments(collection)
    # 2. filter for language
    tweets = list(filter(lambda tweet: tweet['lang'] == 'en', tweets))
    tweets = tweets[:1000]
    # create map for couinting word occurcences
    occurences = dict()
    # 3. do POS separation
    for tweet in tweets:
        sentence = tweet['full_text']

        if sentence.startswith('RT'):
            sentence = sentence[2:]
        # remove line breaks
        sentence = re.sub(r'[\n]+', ' ', sentence)
        # remove all @-handles such as @sam_harris
        sentence = re.sub(r'(@[^\s]+)', '', sentence)
        # remove all non alphanumeric chars
        sentence = re.sub(r'[^A-Za-z0-9 ]+', '', sentence)
        # remove all leading and trainling whitespace or tabs
        sentence = sentence.strip()

        # POS tagging and filtering for nouns
        tokens = nltk.word_tokenize(sentence.lower())
        tokens = list(filter(lambda token: not str(
            token).startswith('http'), tokens))
        tagged = nltk.pos_tag(tokens)
        nouns = list(filter(lambda taggedWord: taggedWord[1] == 'NN' or taggedWord[1]
                            == 'NNS' or taggedWord[1] == 'NNP' or taggedWord[1] == 'NNPS', tagged))
        nouns = list(map(lambda noun: noun[0], nouns))
        stop_words = set(stopwords.words('english'))
        filtered_nouns = [w for w in nouns if not w in stop_words]

        lem = WordNetLemmatizer()
        lemmatized_nouns = list(
            map(lambda noun: str(lem.lemmatize(noun)), filtered_nouns))
        # print('lemmatized_nouns: ' + str(lemmatized_nouns))

        updateOccurences(occurences, lemmatized_nouns)
    return occurences


def updateOccurences(dictionary, occurences):
    for occurence in occurences:
        if occurence in dictionary:
            dictionary[occurence] += 1
        else:
            dictionary[occurence] = 1


dbClient = DatabaseClient()
termFrequencyAudi = calculateTermFrequency(dbClient, 'audi')
termFrequencyAudi.pop('audi', None)

termFrequencyAudiEtron = calculateTermFrequency(dbClient, 'audi_etron')
termFrequencyAudiEtron.pop('audi', None)
termFrequencyAudiEtron.pop('etron', None)
# fDist = FreqDist(termFrequencyAudi)
# fDist.plot(10)
# fDist.plot(20)
