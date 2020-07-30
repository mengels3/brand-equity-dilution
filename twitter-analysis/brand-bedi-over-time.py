from datetime import datetime, timedelta
import matplotlib.dates
import matplotlib.pyplot as plt
import json

# -------------------- AUDI ------------------------

with open('twitter-db-fetch/results/merged-data-audi.json') as f:
    data = json.load(f)

data.reverse()

dates_audi = []
data_audi = []
for datapoint in data:
    dates_audi.append(datapoint['date'])
    data_audi.append(datapoint['bedi'])

# -------------------- VW ------------------------

with open('twitter-db-fetch/results/merged-data-volkswagen.json') as f:
    data = json.load(f)

data.reverse()

dates_volkswagen = []
data_volkswagen = []
for datapoint in data:
    dates_volkswagen.append(datapoint['date'])
    data_volkswagen.append(datapoint['bedi'])

# -------------------- MERCEDES ------------------------

with open('twitter-db-fetch/results/merged-data-mercedes.json') as f:
    data = json.load(f)

data.reverse()

dates_mercedes = []
data_mercedes = []
for datapoint in data:
    dates_mercedes.append(datapoint['date'])
    data_mercedes.append(datapoint['bedi'])

plt.plot(dates_audi, data_audi, label='Audi')
plt.plot(dates_volkswagen, data_volkswagen, label='Volkswagen')
plt.plot(dates_mercedes, data_mercedes, label='Mercedes')
plt.legend()
# beautify the x-labels
plt.gcf().autofmt_xdate()
plt.xlabel("time")
plt.ylabel("BEDI")
plt.show()
