from database_client import DatabaseClient
from datetime import datetime, timedelta
import matplotlib.dates
import matplotlib.pyplot as plt
import json

dbClient = DatabaseClient()


def calculateVisibilityForToday():
    # get fraction for the live timeframe (3 days currently)
    threeDaysAgo = datetime.now() - timedelta(days=3)

    tweetsMainLast3daysCount = len(list(filter(lambda tweet: datetime.strptime(
        tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y') >= threeDaysAgo, dbClient.getAllDocuments("mercedes"))))

    tweetsExtensionLast3daysCount = len(list(filter(lambda tweet: datetime.strptime(
        tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y') >= threeDaysAgo, dbClient.getAllDocuments("mercedes_eqc"))))

    fraction = tweetsExtensionLast3daysCount / tweetsMainLast3daysCount
    print("visibility of extension is: " + str(fraction))


def calculateGraphOverTime():
    # get all tweets for main brand and extension
    twoWeeksAgo = datetime.now() - timedelta(days=14)

    # only take tweets from last 14 days
    tweetsMainLastTwoWeeks = list(filter(lambda tweet: datetime.strptime(
        tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y') > twoWeeksAgo, dbClient.getAllDocuments("volkswagen")))

    tweetsExtensionLastTwoWeeks = list(filter(lambda tweet: datetime.strptime(
        tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y') > twoWeeksAgo, dbClient.getAllDocuments("volkswagen_id3")))

    timestamps = []
    values = []
    # calculate fraction for each day in the last two weeks for graph over time
    for i in range(14):
        lowerBoundMain = list(filter(lambda tweet: datetime.strptime(
            tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y') < (datetime.now() - timedelta(days=i)), tweetsMainLastTwoWeeks))
        upperAndLowerBoundMain = list(filter(lambda tweet: datetime.strptime(
            tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y') > (datetime.now() - timedelta(days=i+1)), lowerBoundMain))

        # get tweets in specific timeframe per day
        lowerBoundExtension = list(filter(lambda tweet: datetime.strptime(
            tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y') < (datetime.now() - timedelta(days=i)), tweetsExtensionLastTwoWeeks))
        upperAndLowerBoundExtension = list(filter(lambda tweet: datetime.strptime(
            tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y') > (datetime.now() - timedelta(days=i+1)), lowerBoundExtension))

        timestamp = datetime.now() - timedelta(days=i)
        fraction = 0 if len(upperAndLowerBoundMain) == 0 else len(upperAndLowerBoundExtension) / \
            len(upperAndLowerBoundMain)
        timestamps.insert(i, timestamp)
        values.insert(i, fraction)

    print(timestamps)
    print(values)

    writeToJsonFile(timestamps, values)

    # plot
    plt.plot(timestamps, values)
    # beautify the x-labels
    plt.gcf().autofmt_xdate()
    plt.xlabel("time")
    plt.ylabel("visibility")
    plt.show()


def writeToJsonFile(timestamps, values):
    data = []
    fit = 0.213
    for i in range(len(timestamps)):
        data.insert(i, {'date': timestamps[i].strftime(
            '%Y-%m-%d'), 'visibility': values[i], 'likelihood': values[i] * fit})

    with open('dilution-likelihood-volkswagen.json', 'w') as outfile:
        json.dump(data, outfile)


def main():
    # calculateVisibilityForToday()
    calculateGraphOverTime()


if __name__ == "__main__":
    main()
