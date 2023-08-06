# -*- coding: utf-8 -*-

import textwrap
import StringIO
from datetime import datetime, timedelta

import pandas as pd
from pandas import Series
from pandas import DataFrame
from pandas import rolling_median

import numpy as np

# use non interactive mode
import matplotlib
matplotlib.use('Agg')
from matplotlib import dates
from mpl_toolkits.mplot3d import Axes3D

# Locators for tick positionning
from matplotlib.ticker import *

import matplotlib.pyplot as plt
# http://matplotlib.org/api/sankey_api.html
import matplotlib.sankey as sankey
from matplotlib.table import Table

from scipy.interpolate import griddata

# require Pillow
from PIL import Image

# sudo pip install py_expression_eval
from py_expression_eval import Parser

import pprint
# import sys
# import traceback


class Consumer(object):
    def __init__(self, c, dtFrom=None, dtTo=None):
        self._c=c
        self._items={}
        if dtFrom is None:
            dtFrom=datetime.now()-timedelta(days=365*10)
        self._dtFrom=dtFrom
        if dtTo is None:
            dtTo=datetime.now()
        self._dtTo=dtTo

    @property
    def dtFrom(self):
        return self._dtFrom

    @property
    def dtTo(self):
        return self._dtTo

    def stampStr(self):
        stamp='%s..%s' % (self.dtFrom.strftime('%d-%m-%Y'), self.dtTo.strftime('%d-%m-%Y'))
        return stamp

    def clean(self):
        self._items={}

    def dtstr(self, dt):
        return dt.strftime("%Y-%m-%d")

    def dbretrieve(self, key):
        df = pd.read_sql("""
            SELECT records.stamp, records.value
            FROM records
            INNER JOIN `keys` ON `keys`.id=records.idkey
            WHERE `keys`.`key`='%s'
            ORDER BY stamp
            """ % key,
            self._c,
            parse_dates='stamp',
            index_col='stamp')

        return df

    def resample(self, s, rule, how='min'):
        if rule:
            # http://pandas.pydata.org/pandas-docs/version/0.18.0/whatsnew.html#whatsnew-0180-breaking-resample
            r=s.resample(rule, closed='left', label='left')
            if how=='min':
                return r.min()
            elif how=='max':
                return r.max()
            elif how=='mean':
                return r.mean()
            print "ERROR: unimplemented resample term %s !" % how
            return r
        return s

    # resample period
    # http://pandas-docs.github.io/pandas-docs-travis/timeseries.html#offset-aliases
    # see also anchory offsets for resample period (i.e. W-MON) :
    # http://pandas-docs.github.io/pandas-docs-travis/timeseries.html#anchored-offsets
    def load(self, key, resample=None, resampleHow='min', reject=0.0):
        try:
            df=self._items[key]
        except:
            df=self.dbretrieve(key)
            self._items[key]=df

        s=df['value']
        s.name=key
        rs=self.resample(s, resample, how=resampleHow)
        rs2=self.reject_outliers(rs, reject)

        rs2.fillna(method='pad', inplace=True)
        # rs2.interpolate(inplace=True)

        return rs2

    def loadDaily(self, key, resampleHow='min', reject=0.0):
        return self.load(key, 'D', resampleHow, reject=reject)

    def loadWeekly(self, key, resampleHow='min', reject=0.0):
        return self.load(key, 'W-MON', resampleHow, reject=reject)

    def loadMonthly(self, key, resampleHow='min', reject=0.0):
        return self.load(key, 'MS', resampleHow, reject=reject)

    def loadYearly(self, key, resampleHow='min', reject=0.0):
        return self.load(key, 'AS', resampleHow, reject=reject)

    # def pruneOutOfDateRecords(self, s):
        # data=s[self._dtFrom:self._dtTo]
        # return data

    def conso(self, key, factor=1.0, resample='d', reject=0.0):
        try:
            # eliminate last value (may be incomplete -- as month conso)
            s=self.load(key, resample, reject=reject)[:-1]

            data=s[self._dtFrom:self._dtTo]
            return (data[-1]-data[0])*factor
        except:
            pass
        return 0.0

    def reject_outliers(self, data, threshold=3.0, window=3):
        if threshold<=0:
            return data

        # https://ocefpaf.github.io/python4oceanographers/blog/2015/03/16/outlier_detection/
        s = rolling_median(data, window=3, center=True).fillna(method='bfill').fillna(method='ffill')
        difference = np.abs(data - s)
        return data[difference<threshold]


class FlowStream(object):
    def __init__(self, index, name, value, factor=1.0, orientation=0):
        self._index=index
        self._name=name
        self._value=value
        self._factor=factor
        self._orientation=orientation

    @property
    def index(self):
        return self._index

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self.calcValue()

    @property
    def orientation(self):
        return self._orientation

    def calcValue(self):
        if self._value is not None:
            return self._value*self._factor
        return 0.0

    def normalizedValue(self, total):
        return self.value()/total

    def isInput(self):
        return None

    def isOutput(self):
        if self.isInput() is None:
            return None
        return not self.isInput()


class FlowStreamInput(FlowStream):
    def isInput(self):
        return True


class FlowStreamOutput(FlowStream):
    def isInput(self):
        return False


class Flow(object):
    def __init__(self, sankey, name, color, rotation):
        self._sankey=sankey
        self._name=name
        self._index=len(sankey.flows())
        self._color=color
        self._rotation=rotation
        self._inputs=[]
        self._outputs=[]
        self._prior=None
        self._priorConnect=None

    @property
    def sankey(self):
        return self._sankey

    @property
    def name(self):
        return self._name

    @property
    def consumer(self):
        return self.sankey.consumer

    @property
    def index(self):
        return self._index

    @property
    def color(self):
        return self._color

    @property
    def rotation(self):
        return self._rotation

    def inputStreamByName(self, name):
        for stream in self._inputs:
            if stream.name==name:
                return stream

    def outputStreamByName(self, name):
        for stream in self._outputs:
            if stream.name==name:
                return stream

    def inflate(self, name, value, orientation=0):
        if value is None:
            value=0
        value=abs(value)
        stream=FlowStreamInput(len(self._inputs), name, value, 1.0, orientation)
        print "(%s:%.02f)--%d-->[%s]" % (stream.name, stream.value, stream.index, self.name)
        self._inputs.append(stream)
        return stream

    def inflateLeft(self, name, value):
        return self.inflate(name, value, -1)

    def inflateRight(self, name, value):
        return self.inflate(name, value, 1)

    def inflateWith(self, flow, streamName, orientation=0):
        rstream=flow.outputStreamByName(streamName)
        if rstream:
            lstream=self.inflate(rstream.name, rstream.value, orientation)
            self._prior=flow.index
            self._priorConnect=(len(flow._inputs)+rstream.index, lstream.index)
            return lstream

    def inflateLeftWith(self, flow, streamName):
        return self.inflateWith(flow, streamName, -1)

    def inflateRightWith(self, flow, streamName):
        return self.inflateWith(flow, streamName, 1)

    def deflate(self, name, value, orientation=0):
        if value is None:
            value=0
        value=abs(value)
        stream=FlowStreamOutput(len(self._outputs), name, value, 1.0, orientation)
        print "[%s]--%d-->(%s:%.02f)" % (self.name, stream.index, stream.name, stream.value)
        self._outputs.append(stream)
        return stream

    def deflateRight(self, name, value):
        return self.deflate(name, value, 1)

    def deflateLeft(self, name, value):
        return self.deflate(name, value, -1)

    def totalIn(self):
        value=0
        for stream in self._inputs:
            value+=stream.value
        return value

    def totalOut(self):
        value=0
        for stream in self._outputs:
            value+=stream.value
        return value

    def total(self):
        return max(self.totalIn(), self.totalOut())

    def missing(self):
        return abs(self.totalIn()-self.totalOut())

    def missingOutput(self):
        if self.totalOut()<self.totalIn():
            return self.missing()
        return 0.0

    def missingInput(self):
        if self.totalIn()<self.totalOut():
            return self.missing()
        return 0.0

    def distributeMissingOnOutputs(self):
        missing=self.missing()
        if missing:
            total=self.totalOut()
            for stream in self._outputs:
                stream._value+=(stream._value/stream._factor/total)*missing

    def distributeMissingOnInputs(self):
        missing=self.missing()
        if missing:
            total=self.totalIn()
            for stream in self._inputs:
                stream._value+=(stream._value/stream._factor/total)*missing

    def completeMissingStream(self, name=None, orientation=0):
        missing=self.missing()
        if missing:
            if not name:
                name='%s:?' % self.name
                if self.totalIn()>self.totalOut():
                    self.deflate(name, missing, orientation)
                else:
                    self.inflate(name, missing, orientation)

    def completeLeftMissingStream(self, name=None):
        return self.completeMissingStream(name, -1)

    def completeRightMissingStream(self, name):
        return self.completeMissingStream(name, 1)

    def sankeyData(self):
        flows=[]
        labels=[]
        orientations=[]

        for stream in self._inputs:
            value=stream.value
            label=stream.name
            flows.append(value)

            if self.total()>0:
                ratio=value/self.total()
                if ratio>=0.001:
                    label='%s %.01f%%' % (label, ratio*100.0)

            labels.append(label)
            orientations.append(stream.orientation)

        for stream in self._outputs:
            value=stream.value
            label=stream.name
            value=stream.value
            if value>0:
                flows.append(-value)
            else:
                flows.append(0.0)

            if self.total()>0:
                ratio=value/self.total()
                if ratio>=0.001:
                    label='%s %.01f%%' % (label, ratio*100.0)

            labels.append(label)
            orientations.append(stream.orientation)

        return (flows, labels, orientations)


class Figure(object):
    def __init__(self, nrows=1, ncols=1, **kwargs):
        self._nrows=nrows
        self._ncols=ncols
        self._plots={}

        # Make the graphs a bit prettier, and bigger
        # deprecated: pd.set_option('display.mpl_style', 'default')

        matplotlib.style.use('ggplot')
        # print matplotlib.style.available

        # fix default white background
        kwargs.setdefault('facecolor', 'white')

        # print kwargs
        self._fig=plt.figure(**kwargs)

    def plot(self, name):
        try:
            return self._plots[name]
        except:
            pass

    def addplot(self, name='main', row=0, col=0, vspan=1, hspan=1, **kwargs):
        plot=self.plot(name)
        if plot:
            return plot

        ax=plt.subplot2grid((self._nrows, self._ncols), (row, col), colspan=hspan, rowspan=vspan, **kwargs)
        plot=Plot(ax)
        return plot

    @property
    def fig(self):
        return self._fig

    def render(self):
        pass

    def image(self):
        self.render()

        buf = StringIO.StringIO()
        plt.savefig(buf,
                format='png',
                bbox_inches='tight',
                frameon=False,
                pad_inches=0.6,
                # transparent=False,
                facecolor=self._fig.get_facecolor(),
                edgecolor='none')
        buf.seek(0)
        image = Image.open(buf)
        # open don't load data until it is used, so load it before closing buffer !
        image.load()
        buf.close()

        return image

    def save(self, fpath):
        image=self.image()
        image.save(fpath)
        self.close()

    def close(self):
        self.fig.clf()
        plt.close(self.fig)

    def show(self):
        self.render()
        plt.show()

    def text(self, x, y, label, *args, **kwargs):
        # http://matplotlib.org/api/figure_api.html
        self.fig.text(x, y, label, *args, **kwargs)

    def addPageNumber(self, page, of=None):
        label='page %d' % page
        if of:
            label += '/%d' % of
        self.fig.text(0.95, 0.05, label, {'horizontalalignment': 'right'})

    def addFooter(self, label, **kwargs):
        kwargs.setdefault('horizontalalignment', 'left')
        self.fig.text(0.05, 0.05, label, **kwargs)

    def addHeader(self, label, **kwargs):
        kwargs.setdefault('horizontalalignment', 'left')
        self.fig.text(0.05, 0.95, label, **kwargs)

    def addHeaderRight(self, label, **kwargs):
        kwargs.setdefault('horizontalalignment', 'right')
        self.fig.text(0.95, 0.95, label, **kwargs)


class Plot(object):
    def __init__(self, ax):
        self._ax=ax

    @property
    def ax(self):
        return self._ax

    @property
    def figure(self):
        return self.ax.figure

    def setTitle(self, title, size=12, loc='center'):
        if title:
            self.ax.set_title(title, size=size, loc=loc)

    def setUnit(self, unit):
        if unit:
            self.ax.set_title(unit, size=12, loc='left')

    def setSecondaryUnit(self, unit):
        if unit:
            self.ax.set_title(unit, size=12, loc='right')

    def setYLabel(self, label, size=12):
        if label:
            self.ax.set_ylabel(label, size=size)

    def setXLabel(self, label, size=12):
        if label:
            self.ax.set_xlabel(label, size=size)

    def table(self, **kwargs):
        table=Table(self.ax, **kwargs)
        self.ax.set_axis_off()
        return table

    def ylabels(self):
        return self.ax.get_yticklabels()

    def setColorYLabels(self, color):
        [i.set_color(color) for i in self.ylabels()]


class SimplePlot(object):
    def __init__(self, s, width=17, height=11, title=None, ylabel=None, unit=None):
        self._s=s
        self._title=title
        self._ylabel=ylabel
        self._unit=unit
        self._figure=Figure(1, 1, figsize=(width, height), frameon=False)
        # self._figure.fig.patch.set_facecolor('white')

    @property
    def s(self):
        return self._s

    def onPlot(self, plot):
        self._s.plot(ax=plot.ax, drawstyle='steps-post')
        plot.ax.set_xlabel('')

    def render(self):
        plot=self._figure.addplot('main', 0, 0)
        plot.setTitle(self._title)
        plot.setUnit(self._unit)
        plot.setYLabel(self._ylabel)
        self.onPlot(plot)

    def image(self):
        self.render()
        return self._figure.image()

    def save(self, fpath):
        self.render()
        return self._figure.save(fpath)

    def close(self):
        self._figure.close()


class SimpleScatter(object):
    def __init__(self, x, y, colors=None, width=20, height=10, title=None, ylabel=None, xlabel=None, unit=None):
        self._x=x
        self._y=y
        self._colors=colors
        self._title=title
        self._ylabel=ylabel
        self._unit=unit
        self._figure=Figure(1, 1, figsize=(width, height), frameon=False)
        # self._figure.figpatch.set_facecolor('white')

    def render(self):
        plot=self._figure.addplot('main', 0, 0)
        plot.setTitle(self._title)
        plot.setUnit(self._unit)
        plot.setYLabel(self._ylabel)
        plot.ax.scatter(x=self._x, y=self._y, c=self._colors)

    def image(self):
        self.render()
        return self._figure.image()

    def save(self, fpath):
        self.render()
        return self._figure.save(fpath)


class DOWSignature(object):
    def __init__(self, s):
        self._s=s
        self._valid=False

    def colors(self, n=7):
        # todo:
        colors=['#363f15',
            '#89732e',
            '#4ab03b',
            '#8e3db6',
            '#551c31',
            '#345b9c',
            '#ae3a48']
        return colors

    def calc(self):
        self._x=[]
        self._y=[]
        self._color=[]

        colors=self.colors(7)

        for i in range(len(self._s)):
            stamp=self._s.index[i]
            yvalue=self._s[i]
            try:
                xvalue=stamp.weekday()
                self._x.append(xvalue)
                self._y.append(yvalue)
                self._color.append(colors[xvalue])
            except:
                pass

        self._valid=True

    def draw(self, plot):
        if not self._valid:
            self.calc()
        plot.ax.scatter(x=self._x, y=self._y, c=self._color)


class Signature(object):
    def __init__(self, sx, sy, colormode='dow'):
        self._sx=sx
        self._sy=sy
        self._colormode=colormode
        self._valid=False

    def color(self, n):
        colors=['#363f15',
            '#89732e',
            '#4ab03b',
            '#8e3db6',
            '#551c31',
            '#345b9c',
            '#ae3a48']

        try:
            return colors[n]
        except:
            return '#ff0000'

    def calc(self):
        self._x=[]
        self._y=[]
        self._color=[]

        for i in range(len(self._sy)):
            stamp=self._sy.index[i]
            yvalue=self._sy[i]
            try:
                xvalue=self._sx[stamp]
                self._x.append(xvalue)
                self._y.append(yvalue)
                if self._colormode=='year':
                    self._color.append(self.color(stamp.year % 7))
                elif self._colormode=='month':
                    self._color.append(self.color(stamp.month-1))
                else:
                    self._color.append(self.color(stamp.weekday()))
            except:
                pass

        self._valid=True

    def draw(self, plot):
        if not self._valid:
            self.calc()
        plot.ax.scatter(x=self._x, y=self._y, c=self._color)


# class TSignature(Signature):
    # def __init__(self, c, sy, tkey='r_9100_2_mtogvetre200d0_0_0'):
        # self._c=c
        # sx=c.loadDaily(tkey)
        # super(TSignature, self).__init__(sx, sy)


class Heatmap(object):
    def __init__(self, s, yresolution=15):
        self._s=s
        self._yresolution=yresolution
        self._valid=False
        self._xi=[]
        self._yi=[]
        self._zi=[]
        self._zmin=None
        self._zmax=None

    def calc(self):
        x=[]
        y=[]
        z=[]

        for i in range(len(self._s)):
            try:
                stamp=self._s.index[i]
                value=self._s[i]
                ttuple=stamp.timetuple()
                yday=ttuple.tm_yday
                seconds=ttuple.tm_hour*3600+ttuple.tm_min*60+ttuple.tm_sec
                x.append(yday)
                y.append(seconds)
                z.append(value)
            except:
                pass

        self._xi=np.arange(0, 365, 1.0)
        self._yi=np.arange(0, 86400+self._yresolution*60.0, 60.0*self._yresolution)
        X, Y=np.meshgrid(self._xi, self._yi)

        self._zi=griddata((x, y), z, (X, Y), method='cubic')
        self._zmin=min(z)
        self._zmax=max(z)
        self._valid=True

    @property
    def zi(self):
        return self._zi

    # colormaps : http://matplotlib.org/users/colormaps.html
    def draw(self, plot, label=None, colormap='plasma'):
        if not self._valid:
            self.calc()

        plot.ax.patch.set_facecolor('#222222')

        self._zi[self._zi<=self._zmin]=None
        self._zi[self._zi>self._zmax]=self._zmax

        # levels=np.linspace(zmin, zmax, 6, endpoint=True)
        levels=np.linspace(self._zmin, self._zmax, 11, endpoint=True)

        try:
            cm=plt.cm.get_cmap(colormap)
        except:
            cm=plt.cm.plasma

        cs=plot.ax.contourf(self._xi, self._yi, self._zi,
            levels=levels,
            vmin=self._zmin, vmax=self._zmax,
            # cmap=plt.cm.magma
            cmap=cm)

        ticks=[]
        for n in range(1, 13):
            ticks.append(datetime(2016, n, 1).timetuple().tm_yday)

        plot.ax.set_xticks(ticks)
        plot.ax.set_xticklabels(['JAN', 'FEV', 'MAR', 'AVR', 'MAI', 'JUN', 'JUI',
                                 'AOU', 'SEP', 'OCT', 'NOV', 'DEC'])
        plot.ax.xaxis.grid(True, which="major", linestyle='-', color='#666666')
        plot.ax.yaxis.grid(True, which="major", linestyle='-', color='#666666')

        ticks=range(0, 25, 3)
        plot.ax.set_yticks([n*3600 for n in ticks])
        plot.ax.set_yticklabels(['%02dh' % n for n in ticks])

        if label:
            plot.setTitle(label)

        cbar=plt.colorbar(cs, ax=plot.ax,
            orientation='vertical',
            # ticks=v
            pad=.03, aspect=40.0
            )

        # cbar.ax.set_aspect(10.0)



class HeatmapDiagram(object):
    HEATMAP_YRESOLUTION=15

    def __init__(self, data, width=11, height=17, title=None):
        self._data=data
        self._title=title
        self._size=(width, height)
        self._figure=None
        self._items=[]
        self._figSetup={'pageNumber': None,
                        'footer': None, 'header': None,
                        'rheader': None}

    @property
    def data(self):
        return self._data

    def addPageNumber(self, page, of=None):
        self._figSetup['pageNumber']={'page': page, 'of': of}

    def addFooter(self, label, **kwargs):
        self._figSetup['footer']={'label': label, 'kwargs': kwargs}

    def addHeader(self, label, **kwargs):
        self._figSetup['header']={'label': label, 'kwargs': kwargs}

    def addHeaderRight(self, label, **kwargs):
        self._figSetup['rheader']={'label': label, 'kwargs': kwargs}

    def addItem(self, key, label=None, colormap='plasma', zmin=None, zmax=None):
        item={'key': key, 'label': label, 'colormap': colormap, 'zmin': zmin, 'zmax': zmax}
        self._items.append(item)
        return item

    def image(self):
        figure=Figure(len(self._items), 1, figsize=self._size, frameon=False)

        if self._figSetup['pageNumber']:
            figure.addPageNumber(self._figSetup['pageNumber']['page'],
                                 self._figSetup['pageNumber']['of'])

        if self._figSetup['footer']:
            figure.addFooter(self._figSetup['footer']['label'],
                             **self._figSetup['footer']['kwargs'])

        if self._figSetup['header']:
            figure.addHeader(self._figSetup['header']['label'],
                             **self._figSetup['header']['kwargs'])

        if self._figSetup['rheader']:
            figure.addHeaderRight(self._figSetup['rheader']['label'],
                                  **self._figSetup['rheader']['kwargs'])

        if self._title:
            title=textwrap.wrap(self._title, 110)
            title='\n'.join(title)
            figure.fig.suptitle(title, fontsize=12)
        plt.subplots_adjust(left=0.12, bottom=0.15, right=0.95, top=0.9, wspace=0.01, hspace=0.18)

        nplot=0
        for item in self._items:
            print "HEATMAP LOADING", item
            s=self.data.load(item['key'], '%dT' % self.HEATMAP_YRESOLUTION, 'max')
            # print s, self.data.dtFrom, self.data.dtTo
            s=s[self.data.dtFrom:self.data.dtTo]

            hm=Heatmap(s, self.HEATMAP_YRESOLUTION)
            hm.calc()
            plot=figure.addplot('hm%d' % nplot, nplot, 0)
            hm.draw(plot, label=item['label'],
                    colormap=item['colormap'])

            nplot+=1

        image=figure.image()
        figure.close()

        return image

    def save(self, fpath):
        image=self.image()
        return image.save(fpath)


class EnergyDiagram(object):
    def __init__(self, data, key, keyTRef='r_9100_2_mtogvetre200d0_0_0', width=11, height=17, title=None, unit=None, ymax=None):
        self._data=data
        self._key=key
        self._keyTRef=keyTRef
        self._title=title
        self._unit=unit
        self._ymax=ymax
        self._figure=Figure(4, 2, figsize=(width, height), frameon=False)
        # self._figure.fig.patch.set_facecolor('white')
        if title:
            title=textwrap.wrap(title, 110)
            title='\n'.join(title)
            self._figure.fig.suptitle(title, fontsize=12)
        # plt.subplots_adjust(left=0, bottom=0.2, right=1, top=0.9, wspace=0.15, hspace=0.3)
        plt.subplots_adjust(left=0.15, bottom=0.15, right=0.9, top=0.85, wspace=0.15, hspace=0.3)

    @property
    def data(self):
        return self._data

    def addPageNumber(self, page, of=None):
        self._figure.addPageNumber(page, of)

    def addFooter(self, label, **kwargs):
        self._figure.addFooter(label, **kwargs)

    def addHeader(self, label, **kwargs):
        self._figure.addHeader(label, **kwargs)

    def addHeaderRight(self, label, **kwargs):
        self._figure.addHeaderRight(label, **kwargs)

    def loadDaily(self, key, conso=False):
        p=Parser()
        e=p.parse(key)
        variables={}
        for v in e.variables():
            sv=self.data.loadDaily(v)
            sv[sv==0] = np.nan
            if sv is None or len(sv)<1:
                print "UNKNOWN VARIABLE", v
                return None
            sv2=sv
            if conso:
                sv2=sv.shift(-1)-sv
                sv2[sv2<0]=np.nan
                if self._ymax:
                    sv2[sv2>=self._ymax]=np.nan
            sv2.interpolate(inplace=True)
            variables[v]=sv2

        s=e.evaluate(variables)
        return s

    def loadMonthly(self, key, conso=False):
        p=Parser()
        e=p.parse(key)
        variables={}
        for v in e.variables():
            sv=self.data.loadMonthly(v)
            sv[sv==0] = np.nan
            if sv is None or len(sv)<1:
                print "UNKNOWN VARIABLE", v
                return None
            sv2=sv
            if conso:
                # eliminate last value (could be incomplete)
                sv2=(sv.shift(-1)-sv)[:-1]
                sv2[sv2<0]=np.nan
                if self._ymax:
                    sv2[sv2>=self._ymax]=np.nan
            sv2.interpolate(inplace=True)
            variables[v]=sv2

        s=e.evaluate(variables)
        return s

    def renderProfile(self):
        plot=self._figure.addplot('profile', 0, 0)
        s=self.loadDaily(self._key)

        dt=datetime.now()
        data=s[dt-timedelta(days=365*10):]
        try:
            data.plot(ax=plot.ax, drawstyle='steps-post', linewidth=2.0, color='green')
        except:
            pass
        plot.ax.set_xlabel('')
        plot.setTitle('index compteur')
        # plot.ax.patch.set_facecolor('white')
        if self._unit:
            plot.setUnit('%s' % self._unit)

    def renderConso(self):
        plot=self._figure.addplot('conso', 0, 1)
        # plot.ax.patch.set_facecolor('white')
        stref=self.data.loadDaily(self._keyTRef, resampleHow='mean')
        s=self.loadDaily(self._key, True)

        dt=datetime.now()
        dtFrom=dt-timedelta(days=5*365)
        data=s[dtFrom:]

        try:
            data.plot(ax=plot.ax, drawstyle='steps-post',
                    linewidth=2.0,
                    color='green', label='conso')
        except:
            pass

        ax2=plot.ax.twinx()

        stref2=stref[dtFrom:]
        stref2.plot(ax=ax2, drawstyle='steps-post', color='red', label='Tmoy', alpha=0.4, linewidth=0.3)
        [i.set_color('red') for i in ax2.get_yticklabels()]
        # disable ax2 grid
        ax2.grid(b=None)

        plot.ax.set_xlabel('')
        plot.setTitle(u'conso journaliere')
        if self._unit:
            plot.setUnit('%s/jour' % self._unit)
        plot.setSecondaryUnit(u'°C')

    def renderYear(self):
        plot=self._figure.addplot('yearconso', 1, 0, hspan=2)
        # plot.ax.patch.set_facecolor('white')
        stref=self.data.loadDaily(self._keyTRef, resampleHow='mean')
        s=self.loadDaily(self._key, True)

        dt=datetime.now()
        dtFrom=dt-timedelta(days=365*2)
        data=s[dtFrom:]

        try:
            data.plot(ax=plot.ax, linewidth=2.0,
                    color='green', drawstyle='steps-post')
        except:
            pass

        ax2=plot.ax.twinx()

        stref2=stref[dtFrom:]
        stref2.plot(ax=ax2, drawstyle='steps-post', color='red', label='Tmoy', alpha=0.4, linewidth=0.3)
        [i.set_color('red') for i in ax2.get_yticklabels()]
        # disable ax2 grid
        ax2.grid(b=None)

        plot.ax.set_xlabel('')
        plot.setTitle(u'conso journaliere')
        if self._unit:
            plot.setUnit('%s/jour' % self._unit)
        plot.setSecondaryUnit(u'°C')
        # ax.fill_between(s.index, s.values)

    def renderSignature(self):
        plot=self._figure.addplot('signature', 2, 0, hspan=1, vspan=2)
        # plot.ax.patch.set_facecolor('white')

        stref=self.data.loadDaily(self._keyTRef)
        s=self.loadDaily(self._key, True)
        if self._ymax:
            s[s>=self._ymax]=np.nan

        dt=datetime.now()
        data=s[dt-timedelta(days=365*3):]

        sig=Signature(sy=data, sx=stref, colormode='year')

        plot.setTitle(u'signature conso journalière')
        plot.ax.set_xlabel('Tmoy journaliere')
        sig.draw(plot)
        if self._unit:
            plot.setUnit('%s/jour' % self._unit)

    def color(self, n):
        colors=['#363f15',
            '#89732e',
            '#4ab03b',
            '#8e3db6',
            '#551c31',
            '#345b9c',
            '#ae3a48']

        try:
            return colors[n]
        except:
            return '#ff0000'

    def renderData(self):
        plot=self._figure.addplot('values', 2, 1, hspan=1, vspan=2)
        table=plot.table()

        s=self.loadMonthly(self._key, True)

        # y0=datetime.now().year
        y0=self.data.dtTo.year
        history=3

        widthLabel=0.25
        widthCell=(1.0-widthLabel)/float(history)
        colorCellTitle='#dddddd'
        # sformat='%%.02f %s' % self._unit

        labels=[None,
                'JANVIER', 'FEVRIER', 'MARS', 'AVRIL',
                'MAI', 'JUIN', 'JUILLET', 'AOUT', 'SEPTEMBRE',
                'OCTOBRE', 'NOVEMBRE', 'DECEMBRE',
                'TOTAL']

        heightCell=(1.0)/len(labels)

        row=0
        for label in labels:
            if label:
                table.add_cell(row+1, history, widthLabel, heightCell,
                        text=label, loc='left',
                        facecolor=colorCellTitle)
                row+=1

        for n in range(0, history):
            year=y0-n
            color=self.color(year % 7)
            # print "data", year, color
            cell=table.add_cell(0, n, widthCell, heightCell,
                    text=str(year), loc='right',
                    facecolor=colorCellTitle)

            try:
                total=0
                data=s[str(year)]
                row=1
                for m in range(0, 12):
                    value=0
                    try:
                        value=data[m]
                        if np.isnan(value):
                            svalue='--'
                        else:
                            svalue='%.1f %s' % (value, self._unit)
                    except:
                        svalue='--'

                    table.add_cell(row, n, widthCell, heightCell,
                            text=svalue,
                            loc='right')

                    table._cells[(row, n)]._text.set_color(color)
                    row+=1
                total=data.sum()
            except:
                pass

            table.add_cell(row, n, widthCell, heightCell,
                    text='%.1f %s' % (total, self._unit),
                    loc='right',
                    facecolor=colorCellTitle)

            properties=table.properties()
        for cell in properties['child_artists']:
            cell.set_fontsize(10)

        plot.ax.add_table(table)

    def render(self):
        self.renderProfile()
        self.renderConso()
        self.renderYear()
        self.renderData()
        self.renderSignature()

    def image(self):
        self.render()
        return self._figure.image()

    def save(self, fpath):
        self.render()
        return self._figure.save(fpath)

    def close(self):
        self._figure.close()


class VolumeDiagram(object):
    def __init__(self, data, key, width=11, height=17, title=None, unit=None, ymax=None, color=None):
        self._data=data
        self._key=key
        self._title=title
        self._unit=unit
        self._ymax=ymax
        if color is None:
            color='blue'
        self._color=color
        self._figure=Figure(4, 2, figsize=(width, height), frameon=False)
        # self._figure.fig.patch.set_facecolor('white')
        if title:
            title=textwrap.wrap(title, 110)
            title='\n'.join(title)
            self._figure.fig.suptitle(title, fontsize=12)
        plt.subplots_adjust(left=0.15, bottom=0.15, right=0.9, top=0.85, wspace=0.15, hspace=0.3)

    @property
    def data(self):
        return self._data

    def addPageNumber(self, page, of=None):
        self._figure.addPageNumber(page, of)

    def addFooter(self, label, **kwargs):
        self._figure.addFooter(label, **kwargs)

    def addHeader(self, label, **kwargs):
        self._figure.addHeader(label, **kwargs)

    def addHeaderRight(self, label, **kwargs):
        self._figure.addHeaderRight(label, **kwargs)

    def loadDaily(self, key, conso=False):
        p=Parser()
        e=p.parse(key)
        variables={}
        for v in e.variables():
            sv=self.data.loadDaily(v)
            sv[sv==0] = np.nan
            if sv is None or len(sv)<1:
                print "UNKNOWN VARIABLE", v
                return None
            sv2=sv
            if conso:
                sv2=sv.shift(-1)-sv
                sv2[sv2<0]=np.nan
                if self._ymax:
                    sv2[sv2>=self._ymax]=np.nan

            # todo: check if really welcomed :)
            sv2.interpolate(inplace=True)
            variables[v]=sv2

        s=e.evaluate(variables)
        return s

    def loadMonthly(self, key, conso=False):
        p=Parser()
        e=p.parse(key)
        variables={}
        for v in e.variables():
            sv=self.data.loadMonthly(v)
            sv[sv==0] = np.nan
            if sv is None or len(sv)<1:
                print "UNKNOWN VARIABLE", v
                return None
            sv2=sv
            if conso:
                # eliminate last value (could be incomplete)
                sv2=(sv.shift(-1)-sv)[:-1]
                sv2[sv2<0]=np.nan
                if self._ymax:
                    sv2[sv2>=self._ymax]=np.nan

            # todo: check if really welcomed :)
            sv2.interpolate(inplace=True)
            variables[v]=sv2

        s=e.evaluate(variables)
        return s

    def renderProfile(self):
        plot=self._figure.addplot('profile', 0, 0)
        s=self.loadDaily(self._key)

        # todo: check if really welcomed ;)
        s.interpolate(inplace=True)

        dt=datetime.now()
        data=s[dt-timedelta(days=365*10):]
        try:
            data.plot(ax=plot.ax, drawstyle='steps-post', linewidth=2.0, color=self._color)
        except:
            pass
        plot.ax.set_xlabel('')
        plot.setTitle('index compteur')
        # plot.ax.patch.set_facecolor('white')
        if self._unit:
            plot.setUnit('%s' % self._unit)

    def renderConso(self):
        plot=self._figure.addplot('conso', 0, 1)
        # plot.ax.patch.set_facecolor('white')
        s=self.loadMonthly(self._key, True)

        dt=datetime.now()
        dtFrom=dt-timedelta(days=5*365)
        data=s[dtFrom:]

        try:
            data.plot(ax=plot.ax, drawstyle='steps-post',
                    linewidth=2.0,
                    color=self._color, label='conso')
        except:
            pass

        plot.ax.set_xlabel('')
        plot.setTitle(u'conso mensuelle')
        if self._unit:
            plot.setUnit('%s/jour' % self._unit)

    def renderYear(self):
        plot=self._figure.addplot('yearconso', 1, 0, hspan=2)
        # plot.ax.patch.set_facecolor('white')
        s=self.loadMonthly(self._key, True)

        dt=datetime.now()
        data=s[dt-timedelta(days=365*2):]

        try:
            data.plot(ax=plot.ax, linewidth=2.0,
                    color=self._color, drawstyle='steps-post')
        except:
            pass

        # ax.fill_between(s.index, s.values)
        plot.ax.set_xlabel('')
        plot.setTitle(u'conso mensuelle')
        if self._unit:
            plot.setUnit('%s/jour' % self._unit)

    def renderSignature(self):
        plot=self._figure.addplot('signature', 2, 0, hspan=1, vspan=2)
        # plot.ax.patch.set_facecolor('white')

        s=self.loadDaily(self._key, True)

        dt=datetime.now()
        data=s[dt-timedelta(days=365*3):]

        sig=DOWSignature(s=data)

        plot.setTitle(u'signature conso journalière')
        plot.ax.set_xlabel('jour semaine (0=DI, 1=LU, ...)')
        sig.draw(plot)
        if self._unit:
            plot.setUnit('%s/jour' % self._unit)

    def renderData(self):
        plot=self._figure.addplot('values', 2, 1, hspan=1, vspan=2)
        table=plot.table()

        s=self.loadMonthly(self._key, True)

        # y0=datetime.now().year
        y0=self.data.dtTo.year
        history=3

        widthLabel=0.25
        widthCell=(1.0-widthLabel)/float(history)
        colorCellTitle='#dddddd'
        # sformat='%%.02f %s' % self._unit

        labels=[None,
                'JANVIER', 'FEVRIER', 'MARS', 'AVRIL',
                'MAI', 'JUIN', 'JUILLET', 'AOUT', 'SEPTEMBRE',
                'OCTOBRE', 'NOVEMBRE', 'DECEMBRE',
                'TOTAL'
                ]

        heightCell=(1.0)/len(labels)

        row=0
        for label in labels:
            if label:
                table.add_cell(row, history, widthLabel, heightCell,
                        text=label, loc='left',
                        facecolor=colorCellTitle)
            row+=1

        for n in range(0, history):
            year=y0-n
            table.add_cell(0, n, widthCell, heightCell,
                    text=str(year), loc='right',
                    facecolor=colorCellTitle)

            try:
                total=0
                data=s[str(year)]
                row=1
                for m in range(0, 12):
                    value=0
                    try:
                        value=data[m]
                        if np.isnan(value):
                            svalue='--'
                        else:
                            svalue='%.1f %s' % (value, self._unit)
                    except:
                        svalue='--'

                    table.add_cell(row, n, widthCell, heightCell,
                            text=svalue,
                            loc='right')
                    row+=1
                total=data.sum()
            except:
                pass

            table.add_cell(row, n, widthCell, heightCell,
                    text='%.1f %s' % (total, self._unit),
                    loc='right',
                    facecolor=colorCellTitle)

        properties=table.properties()
        for cell in properties['child_artists']:
            cell.set_fontsize(10)

        plot.ax.add_table(table)

    def render(self):
        self.renderProfile()
        self.renderConso()
        self.renderYear()
        self.renderData()
        self.renderSignature()

    def image(self):
        self.render()
        return self._figure.image()

    def save(self, fpath):
        self.render()
        return self._figure.save(fpath)

    def close(self):
        self._figure.close()


class EfficiencyDiagram(object):
    def __init__(self, data, key1, key2, factor=1.0, keyTRef='r_9100_2_mtogvetre200d0_0_0', width=11, height=17, title=None, unit1=None, unit2=None):
        self._data=data
        self._key1=key1
        self._key2=key2
        self._factor=factor
        self._keyTRef=keyTRef
        self._title=title
        self._unit1=unit1
        self._unit2=unit2
        self._figure=Figure(4, 2, figsize=(width, height), frameon=False)
        # self._figure.fig.patch.set_facecolor('white')
        if title:
            self._figure.fig.suptitle(title, fontsize=12)
        plt.subplots_adjust(left=0, bottom=0.2, right=1, top=0.9, wspace=0.15, hspace=0.3)

    @property
    def data(self):
        return self._data

    def loadWeekly(self, key, conso=False):
        p=Parser()
        e=p.parse(key)

        variables={}
        for v in e.variables():
            print "LOAD", v
            sv=self.data.loadWeekly(v)
            if sv is None or len(sv)<1:
                print "UNKNOWN VARIABLE", v
                return None
            sv2=sv
            if conso:
                sv2=sv.shift(-1)-sv
                sv2[sv2<0]=np.nan
            variables[v]=sv2

        print "EVAL"
        s=e.evaluate(variables)
        print "OK"
        return s

    def renderProfile1(self):
        plot=self._figure.addplot('profile1', 0, 0)
        s=self.loadWeekly(self._key1)

        dt=datetime.now()
        dtFrom=dt-timedelta(days=365*10)
        data=s[dtFrom:]
        try:
            data.plot(ax=plot.ax, drawstyle='steps-post', linewidth=2.0, color='green')
        except:
            pass

        plot.setTitle(self._key1)
        plot.ax.set_xlabel('')
        # plot.ax.patch.set_facecolor('white')
        plot.setUnit(self._unit1)

    def renderProfile2(self):
        plot=self._figure.addplot('profile2', 0, 1)
        s=self.loadWeekly(self._key2)

        dt=datetime.now()
        dtFrom=dt-timedelta(days=365*10)
        data=s[dtFrom:]
        try:
            data.plot(ax=plot.ax, drawstyle='steps-post',
                    linewidth=2.0,
                    color='green')
        except:
            pass

        plot.setTitle(self._key2)
        plot.ax.set_xlabel('')
        # plot.ax.patch.set_facecolor('white')
        plot.setUnit(self._unit2)

    def renderEfficiency(self):
        plot=self._figure.addplot('rendement hebdomadaire', 1, 0, hspan=2, vspan=2)
        # plot.ax.patch.set_facecolor('white')

        s1=self.loadWeekly(self._key1, True)
        s2=self.loadWeekly(self._key2, True)

        s=s1/(s2*self._factor)

        dt=datetime.now()
        dtFrom=dt-timedelta(days=365*5)
        data=s[dtFrom:]

        try:
            data.plot(ax=plot.ax, linewidth=2.0,
                    color='green', drawstyle='steps-post')
        except:
            pass

        plot.ax.set_ylim([0, 1.5])

        stref=self.data.loadWeekly(self._keyTRef)
        stref2=stref[dtFrom:]

        ax2=plot.ax.twinx()
        stref2.plot(ax=ax2,
                drawstyle='steps-post',
                color='red',
                label='Tmoy',
                alpha=0.4)

        [i.set_color('red') for i in ax2.get_yticklabels()]
        plot.ax.set_xlabel('')
        plot.setTitle(u'rendement')
        plot.setSecondaryUnit(u'°C')

        # signature
        plot=self._figure.addplot('signature', 3, 0, hspan=2, vspan=1)
        # plot.ax.patch.set_facecolor('white')

        sig=Signature(sy=data, sx=stref2, colormode='year')
        # sig=DOWSignature(s=data)

        plot.setTitle(u'signature rendement hebdomadaire')
        plot.ax.set_xlabel('Tmoy journaliere')
        sig.draw(plot)
        plot.setUnit('%')

    def render(self):
        self.renderProfile1()
        self.renderProfile2()
        self.renderEfficiency()

    def image(self):
        self.render()
        return self._figure.image()

    def save(self, fpath):
        self.render()
        return self._figure.save(fpath)

    def close(self):
        self._figure.close()


class SankeyDiagram(object):
    def __init__(self, width=11, height=17, title=None, format='%.02f', gap=0.4, fontsize=8, textoffset=0.35, margin=0.15, unit=''):
        self._flows=[]
        self._fontsize=fontsize

        # http://matplotlib.org/api/figure_api.html#matplotlib.figure.Figure.add_subplot
        # subplot=dict(xticks=[], yticks=[])
        # self._figure=Figure(subplot_kw=subplot, figsize=(width, height), frameon=False)
        self._figure=Figure(1, 1, figsize=(width, height), frameon=False)

        plot=self._figure.addplot('sankey', xticks=[], yticks=[])
        plot.ax.patch.set_facecolor('white')

        plot.setTitle(title, 12)

        # http://matplotlib.org/api/sankey_api.html
        self._sankey=sankey.Sankey(ax=plot.ax, format=format,
                unit=unit,
                gap=gap,
                offset=textoffset,
                margin=margin)

        # self._figure.fig.patch.set_facecolor('white')

    def addPageNumber(self, page, of=None):
        self._figure.addPageNumber(page, of)

    def addFooter(self, label, **kwargs):
        self._figure.addFooter(label, **kwargs)

    def addHeader(self, label, **kwargs):
        self._figure.addHeader(label, **kwargs)

    def addHeaderRight(self, label, **kwargs):
        self._figure.addHeaderRight(label, **kwargs)

    def createFlow(self, name, color=None, rotation=0):
        try:
            self._flows[-1].completeLeftMissingStream()
        except:
            pass

        if color is None:
            color=self._flows[-1].color
        flow=Flow(self, name, color, rotation)
        self._flows.append(flow)
        return flow

    def createHorizontalFlow(self, name, color=None):
        return self.createFlow(name, color, 0)

    def createVerticalFlow(self, name, color=None):
        return self.createFlow(name, color, -90)

    def flows(self):
        return self._flows

    def flow(self, index):
        return self._flows[index]

    def render(self):
        total=0
        for flow in self._flows:
            total=max(total, flow.total())
        if total>0:
            self._sankey.scale=1.0/total
            for flow in self._flows:
                flow.completeLeftMissingStream()
                print "---RENDERING", flow.name, flow.total()
                if flow.total()>0:
                    (flows, labels, orientations)=flow.sankeyData()
                    try:
                        self._sankey.add(flows=flows, labels=labels, orientations=orientations,
                            rotation=flow.rotation,
                            facecolor=flow.color,
                            prior=flow._prior,
                            connect=flow._priorConnect)
                    except:
                        print "****** EXCEPTION!"
                        print flow.name
                        pprint.pprint(flows)
                else:
                    print "Ignoring flow %s" % flow.name

            diagrams=self._sankey.finish()
            for diagram in diagrams:
                # diagram.text.set_fontweight('bold')
                diagram.text.set_fontsize(self._fontsize)
                for text in diagram.texts:
                    text.set_fontsize(self._fontsize)
            return True

    def image(self):
        self.render()
        return self._figure.image()

    def save(self, fpath):
        self.render()
        return self._figure.save(fpath)


class DowLoadCurve(object):
    def __init__(self, data, key, keyTRef='r_9100_2_mtogvetre200d0_0_0', width=11, height=17, title=None, unit=None):
        self._data=data
        self._key=key
        self._keyTRef=keyTRef
        self._title=title
        self._unit=unit
        self._figure=Figure(7, 1, figsize=(width, height), frameon=False)
        if title:
            title=textwrap.wrap(title, 110)
            title='\n'.join(title)
            self._figure.fig.suptitle(title, fontsize=12)
        plt.subplots_adjust(left=0.15, bottom=0.05, right=0.9, top=0.85, hspace=0.5)

        self._loads=[]
        self.load()

    @property
    def data(self):
        return self._data

    def addPageNumber(self, page, of=None):
        self._figure.addPageNumber(page, of)

    def addFooter(self, label, **kwargs):
        self._figure.addFooter(label, **kwargs)

    def addHeader(self, label, **kwargs):
        self._figure.addHeader(label, **kwargs)

    def addHeaderRight(self, label, **kwargs):
        self._figure.addHeaderRight(label, **kwargs)

    def color(self, n):
        # todo:
        colors=['#FFCC33',
                '#FFB92E',
                '#FFA72A',
                '#FF9425',
                '#FF8220',
                '#FF6F1C',
                '#FF5D17',
                '#FF4A13',
                '#FF380E',
                '#FF2509',
                '#FF1305',
                '#FF0000']

        try:
            return colors[n]
        except:
            return '#ff00ff'

    def load(self):
        loads=[]
        s=self.data.load(self._key)

        dtFrom=s.index[0]
        dtTo=s.index[-1]

        dt=datetime(dtFrom.year, dtFrom.month, dtFrom.day, 0, 0, 0, 0)

        while dt <= dtTo:
            s1=s[dt:dt+timedelta(seconds=86400-1)]
            loads.append(s1)
            dt=dt+timedelta(days=1)

        self._loads=loads

    def renderMerged(self):
        stref=self.data.loadDaily(self._keyTRef, resampleHow='mean')

        dtnow=datetime.now()
        dt0=datetime(dtnow.year, dtnow.month, dtnow.day, 0, 0, 0, 0)

        sdow=['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

        plots=[]
        for dow in range(0, 7):
            plot=self._figure.addplot('cdc-%d' % dow, dow, 0)
            plots.append(plot)
            plot.ax.xaxis.set_major_locator(dates.HourLocator(interval=3))
            plot.ax.xaxis.set_major_formatter(dates.DateFormatter('%H'))
            plot.ax.xaxis.set_minor_locator(dates.HourLocator())
            plot.setTitle(sdow[dow], loc='center')
            # plot.ax.patch.set_facecolor('white')
            if self._unit and dow==0:
                plot.setUnit('%s' % self._unit)
            if dow < 6:
                plot.ax.set_xticklabels([])

        for s in self._loads:
            try:
                s1=s.copy()
                dow=s1.index[0].weekday()
                dtref=s1.index[0].replace(hour=0, minute=0, second=0)
                tref=stref[dtref]

                nbstep=4
                tstep=int((tref+10.0)/nbstep)

                offset=dt0-s1.index[0]
                s1.index+=offset
                s1.plot(ax=plots[dow].ax,
                        drawstyle='steps-post',
                        linewidth=1.0,
                        color=self.color(tstep), alpha=0.6)
                plots[dow].ax.set_xlabel('')
            except:
                pass

    def render(self):
        self.renderMerged()

    def image(self):
        self.render()
        return self._figure.image()

    def save(self, fpath):
        self.render()
        return self._figure.save(fpath)

    def close(self):
        self._figure.close()


class LoadCurveModel(object):
    def __init__(self, dow, unit=None):
        self._dow=dow
        self._unit=unit
        self._data={}
        self._models={}
        self._vref=None

    @property
    def dow(self):
        return self._dow

    @property
    def unit(self):
        return self._unit

    def getDataKeys(self):
        return self._data.keys()

    def setModel(self, dt, polyfit):
        self._models[dt]=polyfit

    def getModel(self, dt):
        try:
            return self._models[dt]
        except:
            pass

    def smooth(self, s):
        wsize=int(max(3, len(s)/10.0))
        s2=s.rolling(window=wsize, center=True).mean()
        # remove nan values
        s2 = s2[~np.isnan(s2)]
        return s2

    def modelize(self, dt, s, porder=1):
        try:
            s2=self.smooth(s)
            pfitparam=np.polyfit(s2.index, s2.values, porder)
            pfit=np.poly1d(pfitparam)
            self.setModel(dt, pfit)
            return pfit
        except:
            pass

    def loadData(self, dt, s):
        self._data[dt]=s.copy()
        self.modelize(dt, s, 1)

    def getData(self, dt):
        try:
            return self._data[dt]
        except:
            pass

    def getSmoothedData(self, dt):
        return self.smooth(self.getData(dt))

    def getSerieFromModel(self, dt, vref0=-10.0, vref1=35.0, vstep=1.0):
        try:
            pfit=self.getModel(dt)
            x=np.arange(vref0, vref1, vstep)
            y=np.array([np.polyval(pfit, v) for v in x])
            s=Series(y, index=x)

            # mark negative values
            s[s<=0]=np.nan
            # remove nan values
            s=s[~np.isnan(s)]

            return s
        except:
            pass

    def predict(self, dt, vref):
        try:
            try:
                dt=dt.hour*3600+dt.minute+dt.second
            except:
                pass

            dt0=int(dt/900.0)*900
            pfit0=self.getModel(dt0)
            value0=np.polyval(pfit0, vref)
            self._vref=vref
            if dt==dt0:
                return value0
            else:
                dt1=dt0+900
                pfit1=self.getModel(dt1)
                value1=np.polyval(pfit1, vref)
                return value0+(value1-value0)/(dt1-dt0)*(dt-dt0)
        except:
            pass

    def rejectOutliers(self, s, threshold=3.0, window=3):
        try:
            if threshold<=0:
                return s

            # https://ocefpaf.github.io/python4oceanographers/blog/2015/03/16/outlier_detection/
            s2 = s.rolling(window=3, center=True)
            # .fillna(method='bfill').fillna(method='ffill')
            difference = np.abs(s2 - s)
            return s[difference<threshold]
        except:
            return s

    def predictRibbon(self, vref=None):
        if vref is None:
            vref=self._vref

        # fig=Figure()
        # plot=fig.addplot('cdc', 0, 0)

        try:
            x=[]
            y=[]

            for dt in range(0, 86400, 900):
                v=self.predict(dt, vref)
                if v is not None:
                    x.append(dt)
                    y.append(v)

            s=Series(y, index=x)
            # s.plot(ax=plot.ax, color='red')

            s2=self.rejectOutliers(s)
            # s2.plot(ax=plot.ax, color='green')

            s3=s2.rolling(window=8, center=True).mean().fillna(method='ffill').fillna(method='bfill')
            # s3.plot(ax=plot.ax, color='blue')

            # fig.save('ribbon%d.png' % self._dow)
            self._vref=vref
            return min(s3)
        except:
            pass

    def predictPeak(self, vref=None):
        if vref is None:
            vref=self._vref
        try:
            x=[]
            y=[]

            for dt in range(0, 86400, 900):
                v=self.predict(dt, vref)
                if v is not None:
                    x.append(dt)
                    y.append(v)

            s=Series(y, index=x)
            s2=self.rejectOutliers(s)
            s3=s2.rolling(window=8, center=True).mean().fillna(method='ffill').fillna(method='bfill')
            self._vref=vref
            return max(s3)
        except:
            pass


class DailyLoadCurve(object):
    VIEW_RAW=0
    VIEW_MODELIZED_RAW=1
    VIEW_MODELIZED_FIT=2

    def __init__(self, data, dow, key, keyTRef='r_9100_2_mtogvetre200d0_0_0', width=17, height=11, title=None, unit=None):
        self._data=data
        self._key=key
        self._dow=dow
        self._keyTRef=keyTRef
        self._title=title
        self._unit=unit
        self._model=LoadCurveModel(self._dow, self._unit)
        self._figure=Figure(1, 1, figsize=(width, height), frameon=False)
        if title:
            title=textwrap.wrap(title, 110)
            title='\n'.join(title)
            self._figure.fig.suptitle(title, fontsize=12)
        plt.subplots_adjust(left=0.05, bottom=0.10, right=0.95, top=0.92, wspace=0.15, hspace=0.3)

        self._loads=[]
        self.load()

    @property
    def data(self):
        return self._data

    @property
    def model(self):
        return self._model

    def addPageNumber(self, page, of=None):
        self._figure.addPageNumber(page, of)

    def addFooter(self, label, **kwargs):
        self._figure.addFooter(label, **kwargs)

    def addHeader(self, label, **kwargs):
        self._figure.addHeader(label, **kwargs)

    def addHeaderRight(self, label, **kwargs):
        self._figure.addHeaderRight(label, **kwargs)

    def color(self, n):
        # todo:
        colors=['#FFCC33',
                '#FFB92E',
                '#FFA72A',
                '#FF9425',
                '#FF8220',
                '#FF6F1C',
                '#FF5D17',
                '#FF4A13',
                '#FF380E',
                '#FF2509',
                '#FF1305',
                '#FF0000']

        try:
            return colors[n]
        except:
            return '#ff00ff'

    def load(self):
        loads=[]
        s=self.data.load(self._key)
        stref=self.data.loadDaily(self._keyTRef, resampleHow='mean')

        dtFrom=s.index[0]
        dtTo=s.index[-1]

        dt=datetime(dtFrom.year, dtFrom.month, dtFrom.day, 0, 0, 0, 0)
        while dt <= dtTo:
            try:
                if dt.weekday()==self._dow:
                    tref=stref[dt]
                    s1=s[dt:dt+timedelta(seconds=86400-1)]

                    # smooth a bit to get better results
                    s2=s1.rolling(window=2, center=True).mean()

                    data={'t': tref, 'cdc-raw': s1, 'cdc': s2}
                    loads.append(data)
            except:
                pass
            dt=dt+timedelta(days=1)

        loads.sort(key=lambda x: x['t'])
        self._loads=loads

        datas={}
        for data in self._loads:
            s=data['cdc'].copy()

            # resample t here to cleanup samples
            s1=s.resample('15min').mean().interpolate(method='cubic')
            tref=data['t']
            for dt in s1.index:
                dti=dt.hour*3600+dt.minute*60+dt.second
                try:
                    datas[dti]
                except:
                    datas[dti]=[]
                value=s1[dt]
                if not np.isnan(value):
                    record={'t': tref, 'value': value}
                    datas[dti].append(record)
                    # print dti, value

        for dt in datas.keys():
            x=[]
            y=[]
            z=[]

            cdc=datas[dt]
            if len(cdc)<3:
                continue

            cdc.sort(key=lambda x: x['t'])
            for record in cdc:
                # print record
                x.append(dt)
                y.append(record['t'])
                z.append(record['value'])

            s1=Series(z, index=y, dtype='float64')
            self.model.loadData(dt, s1)

    def render(self, view=VIEW_MODELIZED_FIT):
        # dtnow=datetime.now()
        # dt0=datetime(dtnow.year, dtnow.month, dtnow.day, 0, 0, 0, 0)

        sdow=['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
        plot=self._figure.addplot('cdc', 0, 0, projection='3d')
        plot.ax.xaxis.set_major_locator(FixedLocator(range(0, 86400, 3600*3)))
        plot.ax.xaxis.set_minor_locator(FixedLocator(range(0, 86400, 3600)))
        # plot.ax.xaxis.set_major_formatter(dates.DateFormatter('%H'))
        # plot.ax.xaxis.set_minor_locator(dates.HourLocator())

        plot.ax.set_xlabel('', size=10)
        plot.ax.set_ylabel(u'Text °C', size=10)
        plot.ax.set_zlabel(u'power', size=10)
        plot.ax.set_title(sdow[self._dow], loc='right')

        for data in self._loads:
            z1=data['cdc'].values
            z2=data['cdc-raw'].values
            x=[]
            for t in data['cdc'].index:
                x.append(t.hour*3600+t.minute*60+t.second)

            y=[data['t']]*len(x)
            nbstep=4
            tstep=int((data['t']+10.0)/nbstep)
            color=[self.color(tstep)]*len(x)

            if view==DailyLoadCurve.VIEW_RAW:
                plot.ax.scatter(x, y, z2, c=color)
                plot.ax.plot_wireframe(x, y, z1, color=color)
            if view==DailyLoadCurve.VIEW_MODELIZED_FIT:
                plot.ax.plot_wireframe(x, y, z1, color=color)

        for dt in self.model.getDataKeys():
            s1=self.model.getData(dt)
            s2=self.model.getSmoothedData(dt)
            s3=self.model.getSerieFromModel(dt, -10.0, 35.0, 1.0)

            if view==DailyLoadCurve.VIEW_MODELIZED_RAW:
                plot.ax.plot_wireframe(dt, s1.index, s1.values, color='orange', alpha=1.0)
                plot.ax.plot_wireframe(dt, s2.index, s2.values, color='red', alpha=1.0)
            elif view==DailyLoadCurve.VIEW_MODELIZED_FIT:
                # plot.ax.plot_wireframe(dt, s1.index, s1.values, color='orange', alpha=1.0)
                plot.ax.plot_wireframe(dt, s3.index, s3.values, color='blue')

    def image(self, view=VIEW_MODELIZED_FIT):
        self.render(view)
        image=self._figure.image()
        self._figure.close()
        return image

    def save(self, fpath, view=VIEW_MODELIZED_FIT):
        self.render(view)
        self._figure.save(fpath)
        self._figure.close()

    # def close(self):
        # self._figure.close()

    def show(self, view=VIEW_MODELIZED_FIT):
        self.render(view)
        self._figure.show()


if __name__ == "__main__":
    pass
