from datetime import datetime
from time import mktime, strptime

import matplotlib
from matplotlib import gridspec
from matplotlib.figure import Figure
from matplotlib.pyplot import style
import matplotlib.patches as mpatches

style.use('seaborn-whitegrid')
matplotlib.rcParams['xtick.labelsize'] = 20
matplotlib.rcParams['ytick.labelsize'] = 16


def create_plot(data):
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
    patch = mpatches.Patch(color='dodgerblue', label='Temperatur\n$°C$')
    ax1.legend(handles=[patch], prop={'size': 20}, loc=3)
    ax1.plot(dates, temperature, '-', color='dodgerblue')

    ax2 = fig.add_subplot(grid[1])
    ax2.set_xticklabels([])
    patch = mpatches.Patch(color='dodgerblue', label='Salzgehalt\n$g/l$')
    ax2.legend(handles=[patch], prop={'size': 20}, loc=3)
    do_plot(ax2, (dates, salinity))
    ax2.plot(dates, salinity, '-', color='dodgerblue')

    ax3 = fig.add_subplot(grid[2])
    patch = mpatches.Patch(color='dodgerblue', label='Druck')
    ax3.legend(handles=[patch], prop={'size': 20}, loc=3)
    do_plot(ax3, (dates, pressure))
    ax3.plot(dates, pressure, '-', color='dodgerblue')

    fig.autofmt_xdate()
    fig.tight_layout()

    return fig
