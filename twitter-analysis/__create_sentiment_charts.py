import matplotlib.pyplot as plt
import json

brands = ['audi', 'volkswagen', 'mercedes']

for b in brands:
	data = dict()
	with open("export/json/" + b + "_results.json") as f:
		data = json.load(f)
	print(data)
	values_b = list()
	values_e = list()
	for k in data:
		if k != "last_exec_date":
			print(k)
			dates = sorted(data[k].keys())
			values = list()
			for date in sorted(dates):
				values.append(data[k][date]['value'])


			plt.plot(dates, values, "r--")
			plt.xticks(rotation=90)
			plt.ylim(-0.5,0.5)
			plt.show()
