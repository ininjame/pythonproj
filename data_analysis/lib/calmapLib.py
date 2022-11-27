# ----------------------------------------------------------------------------
# A modified version of calendar heat map by author Nicolas P. Rougier
# that accepts data of any size, has function to create input.
# License: BSD
# ----------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def calmap(ax, year, data):
    ax.tick_params('x', length=0, labelsize="medium", which='major')
    ax.tick_params('y', length=0, labelsize="x-small", which='major')

    # Month borders
    xticks, labels = [], []
    start = datetime(year,1,1).weekday()
    for month in range(1,13):
        first = datetime(year, month, 1)
        last = first + relativedelta(months=1, days=-1)

        y0 = first.weekday()
        y1 = last.weekday()
        x0 = (int(first.strftime("%j"))+start-1)//7
        x1 = (int(last.strftime("%j"))+start-1)//7

        P = [ (x0,   y0), (x0,    7),  (x1,   7),
              (x1,   y1+1), (x1+1,  y1+1), (x1+1, 0),
              (x0+1,  0), (x0+1,  y0) ]
        xticks.append(x0 +(x1-x0+1)/2)
        labels.append(first.strftime("%b"))
        poly = Polygon(P, edgecolor="black", facecolor="None",
                       linewidth=1, zorder=20, clip_on=False)
        ax.add_artist(poly)
    
    ax.set_xticks(xticks)
    ax.set_xticklabels(labels)
    ax.set_yticks(0.5 + np.arange(7))
    ax.set_yticklabels(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    ax.set_title("{}".format(year), weight="semibold")
    
    # Clearing first and last day from the data
    valid = datetime(year, 1, 1).weekday()
    data[:valid,0] = np.nan
    valid = datetime(year, 12, 31).weekday()
    # data[:,x1+1:] = np.nan
    data[valid+1:,x1] = np.nan

    # Showing data
    ax.imshow(data, extent=[0,53,0,7], zorder=10, vmin=0, vmax=int(np.nanmax(data)),
              cmap="RdYlBu", origin="lower", alpha=.75)

def create_input(data, year):

    def padding(series, year):
        """
        Take pandas series, generate padding and return values as array
        """
        days_before = (min(series.index) - datetime(year,1,1)).days
        days_after = ((datetime(year,1,1) + timedelta(days=370)) - max(series.index)).days 
        pad_pre =  np.empty(days_before)
        pad_pre.fill(np.nan)
        pad_post = np.empty(days_after)
        pad_post.fill(np.nan)

        return np.concatenate((pad_pre, series.values, pad_post))
    
    inp_raw = padding(data,year).reshape((53,7)).T
    first = datetime(year,1,1)
    dic = {}
    inp = []
    for i in range(7):
        date = first + timedelta(days=i)
        dic[date.weekday()] = inp_raw[i]
    for i in range(7):
        inp.append(dic[i])
    return np.array(inp)