from datetime import datetime
from time import mktime, strptime

from matplotlib.dates import DateFormatter
from matplotlib.figure import Figure
from matplotlib import gridspec
from matplotlib.pyplot import style, gcf, xticks

style.use('seaborn-whitegrid')


def _create_plot(data):
    temperature = data['temperature']
    salinity = data['salinity']
    pressure = data['pressure']
    dates = sorted([datetime.fromtimestamp(
        mktime(strptime(d, '%a, %d %b %Y %H:%M:%S GMT'))) for i, d in enumerate(data['timestamp'])])

    def do_plot(ax, data):
        ax.plot(*data, '-')

    grid = gridspec.GridSpec(3, 1)
    fig = Figure()
    fig.set_size_inches(8.5, 10.5)

    ax1 = fig.add_subplot(grid[0])
    ax1.set_xticklabels([])
    do_plot(ax1, (dates, temperature))

    ax2 = fig.add_subplot(grid[1])
    ax2.set_xticklabels([])
    do_plot(ax2, (dates, salinity))

    ax3 = fig.add_subplot(grid[2])
    do_plot(ax3, (dates, pressure))

    xticks(rotation=70)

    return fig
