import nltk
from database_client import DatabaseClient
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import matplotlib.pyplot as plt
import string
import re
from collections import Counter


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
        # remove t.co shortener url
        sentence = re.sub(r'(\S*t\.co\S*)', ' ', sentence)
        # remove all .com links beacause twitter images tend not to specify https which undergoes our link filter
        sentence = re.sub(r'(\S*\.com*\S*)', ' ', sentence)
        # collapse all "-"
        sentence = re.sub('-', '', sentence)
        # remove all non alphanumeric chars
        sentence = re.sub(r'[^A-Za-z0-9]+', ' ', sentence)
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

    # calculate relative occurence frequency
    totalNounOccurences = sum(occurences.values())
    for key in occurences:
        occurences[key] = occurences[key] / totalNounOccurences
    return occurences


def updateOccurences(dictionary, occurences):
    for occurence in occurences:
        if occurence in dictionary:
            dictionary[occurence] += 1
        else:
            dictionary[occurence] = 1


def calculateMeanFractionalDifference(termFreqMain, termFreqExtension):
    top50main = Counter(termFreqMain).most_common(50)

    fractionSum = 0
    for term in top50main:
        scoreInExtension = 0
        if term[0] in termFreqExtension:
            scoreInExtension = termFreqExtension[term[0]]
        fraction = 0
        if term[1] <= scoreInExtension:
            fraction = term[1] / scoreInExtension
            print('fractional difference for ' + term[0] + ' is: ' + str(
                term[1]) + ' : ' + str(scoreInExtension) + ' = ' + str(fraction))
        else:
            fraction = scoreInExtension / term[1]
            print('fractional difference for ' + term[0] + ' is: ' + str(
                scoreInExtension) + ' : ' + str(term[1]) + ' = ' + str(fraction))
        fractionSum += fraction

    meanDifference = fractionSum / 50
    return meanDifference


def main():

    main = 'volkswagen'
    extension = 'volkswagen_id3'

    dbClient = DatabaseClient()
    termFrequencyMain = calculateTermFrequency(dbClient, main)
    termFrequencyMain.pop(main, None)
    fDist = FreqDist(termFrequencyMain)
    fDist.plot(35)

    termFrequencyExtension = calculateTermFrequency(dbClient, extension)
    # pretty output
    termFrequencyExtension.pop(main, None)
    termFrequencyExtension.pop('id3', None)
    fDist = FreqDist(termFrequencyExtension)
    fDist.plot(35)

    meanDifference = calculateMeanFractionalDifference(
        termFrequencyMain, termFrequencyExtension)
    print('Mean difference in frequency as measure for product fit: ' +
          str(meanDifference))


if __name__ == "__main__":
    main()
