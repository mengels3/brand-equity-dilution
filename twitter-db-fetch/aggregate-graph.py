import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import json

# [{
#     "date": "2020-07-05",
#     "visibility": 0.09242761692650334,
#     "likelihood": 0.01968708240534521,
#     "sentiment": -0.018313913043478233,
#     "bedi": -0.00036054751525128247
# }]


def plotAggregateGraph(data):

    dates = []
    likelihood = []
    sentiment = []
    bedi = []
    for datapoint in data:
        dates.append(datapoint['date'])
        likelihood.append(datapoint['likelihood'])
        sentiment.append(datapoint['sentiment'])
        bedi.append(datapoint['bedi'])

    fig = plt.figure()
    host = fig.add_subplot(111)

    par1 = host.twinx()
    par2 = host.twinx()

    host.set_xlabel("Time")
    host.set_ylabel("BEDI")
    par1.set_ylabel("Likelihood")
    par2.set_ylabel("Sentiment")

    cmap = plt.cm.get_cmap('viridis', 3)
    color1 = cmap(0)
    color2 = cmap(0.5)
    color3 = cmap(0.9)

    p1, = host.plot(dates, bedi,
                    color=color1, label="BEDI")
    p2, = par1.plot(dates, likelihood,
                    color=color2, label="Likelihood")
    p3, = par2.plot(dates, sentiment, color=color3, label="Sentiment")

    lns = [p1, p2, p3]
    host.legend(handles=lns, loc='best')

    # right, left, top, bottom
    par2.spines['right'].set_position(('outward', 60))
    # no x-ticks
    # par2.xaxis.set_ticks([])
    # Sometimes handy, same for xaxis
    # par2.yaxis.set_ticks_position('right')

    host.yaxis.label.set_color(p1.get_color())
    par1.yaxis.label.set_color(p2.get_color())
    par2.yaxis.label.set_color(p3.get_color())

    plt.gcf().autofmt_xdate()

    plt.savefig("pyplot_multiple_y-axis.png", bbox_inches='tight')


def mergeData(main_name, extension_name):
    with open('twitter-db-fetch/results/dilution-likelihood-'+main_name+'.json') as f:
        likelihood = json.load(f)

    with open('sentiment-analysis/'+main_name+'_results.json') as f:
        sentiment = json.load(f)

    mergedData = list()

    for datapoint in likelihood:
        date = datapoint['date']
        try:
            extension_sent = sentiment[extension_name][date]['value']
            main_sent = sentiment[main_name][date]['value']
            value = (extension_sent - main_sent) / 2
            datapoint['sentiment'] = value
            datapoint['bedi'] = value * datapoint['likelihood']
            mergedData.append(datapoint)
        except Exception as ex:
            print('missing sentiment for date', ex)

    with open('twitter-db-fetch/results/merged-data-'+main_name+'.json', 'w') as outfile:
        json.dump(mergedData, outfile)


def main():
    # mergeData('mercedes', 'mercedes_eqc')

    with open('twitter-db-fetch/results/merged-data-mercedes.json') as f:
        data = json.load(f)

    data.reverse()
    plotAggregateGraph(data)


if __name__ == "__main__":
    main()
