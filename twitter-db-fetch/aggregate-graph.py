import matplotlib.pyplot as plt
from datetime import datetime, timedelta

fig = plt.figure()
host = fig.add_subplot(111)

par1 = host.twinx()
par2 = host.twinx()

# host.set_ylim(0.032, 0.05)
# par1.set_ylim(-0.4, -0.2)
# par2.set_ylim(0.1, 0.27)

host.set_xlabel("Time")
host.set_ylabel("Visibility")
par1.set_ylabel("Sentiment")
par2.set_ylabel("Fit")

lastThreeDays = [datetime.now() - timedelta(days=2),
                 datetime.now() - timedelta(days=1), datetime.now()]

cmap = plt.cm.get_cmap('viridis', 3)
color1 = cmap(0)
color2 = cmap(0.5)
color3 = cmap(0.9)

p1, = host.plot(lastThreeDays, [0.032, 0.035, 0.05],
                color=color1, label="Visibility")
p2, = par1.plot(lastThreeDays, [-0.2, -0.3, -0.4],
                color=color2, label="Sentiment")
p3, = par2.plot(lastThreeDays, [0.1, 0.14, 0.27], color=color3, label="Fit")

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
