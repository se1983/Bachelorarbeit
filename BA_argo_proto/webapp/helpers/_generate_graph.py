from datetime import datetime
from time import mktime, strptime

import matplotlib
from matplotlib import gridspec
from matplotlib.figure import Figure
from matplotlib.pyplot import style

style.use('seaborn-whitegrid')
matplotlib.rcParams['xtick.labelsize'] = 20
matplotlib.rcParams['ytick.labelsize'] = 16


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
    ax1.set_ylabel("Temperature")
    do_plot(ax1, (dates, temperature))

    ax2 = fig.add_subplot(grid[1])
    ax2.set_xticklabels([])
    ax2.set_ylabel("Salinity")
    do_plot(ax2, (dates, salinity))

    ax3 = fig.add_subplot(grid[2])
    ax3.set_ylabel("Pressure")
    do_plot(ax3, (dates, pressure))

    fig.autofmt_xdate()
    fig.tight_layout()

    return fig
