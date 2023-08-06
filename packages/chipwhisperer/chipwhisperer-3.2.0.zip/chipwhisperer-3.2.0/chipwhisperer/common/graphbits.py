from PySide.QtCore import *
from PySide.QtGui import *
import numpy as np
import pyqtgraph as pg
from pyqtgraph.graphicsItems.GraphicsWidget import GraphicsWidget
from pyqtgraph.graphicsItems.LabelItem import LabelItem
import random

class fakeItem(object):

    def __init__(self):
        # self.opts = {'fillLevel':None, 'fillBrush':None, 'pen':{'color': pg.mkColor('r'), 'width':1}}
        self.opts = {}

class CustomItemSample(GraphicsWidget):
    """ Copy of ItemSample from GIT """

    # # Todo: make this more generic; let each item decide how it should be represented.
    def __init__(self, item, brectx=20, brecty=20):
        GraphicsWidget.__init__(self)
        self.item = item
        self._brectx = brectx
        self._brecty = brecty

    def boundingRect(self):
        return QRectF(0, 0, self._brectx, self._brecty)

    def paint(self, p, *args):
        # p.setRenderHint(p.Antialiasing)  # only if the data is antialiased.
        opts = self.item.opts

        # if opts.get('fillLevel', None) is not None and opts.get('fillBrush', None) is not None:
        #    p.setBrush(pg.mkBrush(opts['fillBrush']))
        #    p.setPen(pg.mkPen(None))
        #    p.drawPolygon(QPolygonF([QPointF(2, 18), QPointF(18, 2), QPointF(18, 18)]))

        # if not isinstance(self.item, pg.ScatterPlotItem):
        #    p.setPen(pg.mkPen(opts['pen']))
        #    p.drawLine(2, 18, 18, 2)

        symbol = opts.get('symbol', None)
        if symbol is not None:
            if isinstance(self.item, pg.PlotDataItem):
                opts = self.item.scatter.opts

            pen = pg.mkPen(opts['pen'])
            brush = pg.mkBrush(opts['brush'])
            size = opts['size']

            p.translate(10, 10)
            path = pg.graphicsItems.ScatterPlotItem.drawSymbol(p, symbol, size, pen, brush)


class CustomLabelItem(LabelItem):

    def __init__(self, name, div=4):
        self._divisor = div
        super(CustomLabelItem, self).__init__(name)        
    
    def itemRect(self):
        newrect = self.item.boundingRect()
        newrect.setHeight(newrect.height() / self._divisor)
        return self.item.mapRectToParent(newrect)

class BitPlotWidget(QWidget):
    """
    This class plots the faults injected in some location
    """
    def __init__(self, parent=None):
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        QWidget.__init__(self)
        layout = QVBoxLayout()

        self.viewWidget = pg.GraphicsLayoutWidget()  ## GraphicsView with GraphicsLayout inserted by default
        self.plot = self.viewWidget.addPlot()

        # Add scatter plot item
        self.scat = pg.ScatterPlotItem(pxMode=True)  # # Set pxMode=False to allow spots to transform with the view
        self.plot.addItem(self.scat)

        vb = self.scat.getViewBox()
        vb.setMouseMode(vb.RectMode)
        layout.addWidget(self.viewWidget)
        self.setLayout(layout)

        self.plot.setLabel('top', 'Fault Locations vs. Fault Offset')
        self.plot.setLabel('bottom', 'Location of Fault (Bit Number)')
        self.plot.setLabel('left', 'Offset (Clock Cycles)')

        self.legend = self.plot.addLegend()

        for i in range(100, -1, -10):
            item = fakeItem()
            item.opts["symbol"] = 's'
            item.opts["size"] = 4
            item.opts["pen"] = {'color': pg.mkColor(self.rgb(0, 100, i)), 'width':0}
            item.opts["brush"] = pg.mkBrush(self.rgb(0, 100, i))
            if i % 20 == 0:
                s = "%d%%" % i
            else:
                s = ""
            self.addCustomLegendItem(self.legend, item, s)


    def addCustomLegendItem(self, legend, item, name):
        label = CustomLabelItem(name)
        sample = CustomItemSample(item)
        row = len(legend.items)
        legend.items.append((sample, label))
        legend.layout.addItem(sample, row, 0)
        legend.layout.addItem(label, row, 1)
        legend.updateSize()

    def rgb(self, minimum, maximum, value):
        minimum, maximum = float(minimum), float(maximum)
        halfmax = (minimum + maximum) / 2
        b = int(max(0, 255 * (1 - value / halfmax)))
        r = int(max(0, 255 * (value / halfmax - 1)))
        g = 255 - b - r
        return (r, g, b, 255)


    def setData(self, data, dotsize=2, ydiv=4, yoffset=7, ymajor=8, failures=None):
        spots = []
        for y, d in enumerate(data):
            for x, p in enumerate(d):
                if p > 0:
                    bsh = pg.mkBrush(self.rgb(0, 100, p))  # RGBA
                    spots.append({'pos': (x, float(y) / float(ydiv) - yoffset), 'size':dotsize, 'pen': {'color': pg.mkColor(self.rgb(0, 100, p)), 'width':0}, 'symbol':'s', 'brush':bsh})

            if failures and failures[y] > 0:
                bsh = pg.mkBrush(self.rgb(0, 100, failures[y]))  # RGBA
                spots.append({'pos': (-1, float(y) / float(ydiv) - yoffset), 'size':4, 'pen': {'color': pg.mkColor(self.rgb(0, 100, failures[y])), 'width':0}, 'symbol':'d', 'brush':bsh})
                self.plot.addLine(y=float(y) / float(ydiv) - yoffset, pen={'color': pg.mkColor(self.rgb(0, 100, failures[y])), 'width':0.4})

        self.scat.addPoints(spots)

        numbits = len(data[0])
        self.plot.setXRange(0, numbits)

        majorticks = [ (i, "%d" % i) for i in range(0, numbits, 8) ]
        minorticks = [ (i, "") for i in range(0, numbits) ]
        self.plot.getAxis('bottom').setTicks([ majorticks, minorticks  ])
        self.plot.getAxis('bottom').setGrid(50)

        majorticks = [ (i, "%d" % i) for i in range(0, len(data) / ydiv, ymajor) ]
        # minorticks = [ (i, "%d" % i) for i in range(0, len(data) / ydiv, 2) ]
        self.plot.getAxis('left').setTicks([ majorticks, []  ])
        self.plot.getAxis('left').setGrid(50)


class FaultTypevsTwoParameters(QWidget):
    """
    Plot type of fault vs. two parameters 
    """
    def __init__(self, parent=None, xname='Parameter #1 Name',
                                    yname='Parameter #2 Name',
                                    title='100% Not Bullshit',
                                    legend=None):
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        QWidget.__init__(self)
        layout = QVBoxLayout()

        self.viewWidget = pg.GraphicsLayoutWidget()  ## GraphicsView with GraphicsLayout inserted by default
        self.plot = self.viewWidget.addPlot()

        # Add scatter plot item
        self.scat = pg.ScatterPlotItem(pxMode=True)  # # Set pxMode=False to allow spots to transform with the view
        self.plot.addItem(self.scat)

        vb = self.scat.getViewBox()
        vb.setMouseMode(vb.RectMode)
        layout.addWidget(self.viewWidget)
        self.setLayout(layout)

        self.plot.setLabel('top', title)
        self.plot.setLabel('bottom',xname)
        self.plot.setLabel('left', yname)

        if legend:
            self.legend = self.plot.addLegend()            
            for l in legend:
                item = fakeItem()
                
                item.opts["symbol"] = l["symbol"]
                item.opts["size"] = l["size"]
                item.opts["pen"] = {'color': pg.mkColor(l["color"]), 'width':0}
                item.opts["brush"] = pg.mkBrush(l["color"])
                self.addCustomLegendItem(self.legend, item, l["text"])               

    def addCustomLegendItem(self, legend, item, name):
        label = CustomLabelItem(name, div=2)
        sample = CustomItemSample(item)
        row = len(legend.items)
        legend.items.append((sample, label))
        legend.layout.addItem(sample, row, 0)
        legend.layout.addItem(label, row, 2)
        legend.updateSize()

    def rgb(self, minimum, maximum, value):
        minimum, maximum = float(minimum), float(maximum)
        halfmax = (minimum + maximum) / 2
        b = int(max(0, 255 * (1 - value / halfmax)))
        r = int(max(0, 255 * (value / halfmax - 1)))
        g = 255 - b - r
        return (r, g, b, 255)     


    def setData(self, data, dotsize=6):
        spots = []
        for t in data:
            
            ds = dotsize
            
            if t[1] < 0:
                sym = '+'
                clr = 'r'
            elif t[1] == 0:
                sym = None
                ds = 1
                clr = 'k'
            elif t[1] == 1:
                sym = 'o'
                clr = 'b'
            elif t[1] > 1:
                sym = 's'              
                clr = 'g'       
            
            bsh = pg.mkBrush(clr)  # RGBA
            spots.append({'pos': t[0], 'symbol':sym, 'size':ds, 'pen': {'color': pg.mkColor(clr), 'width':0},  'brush':bsh})
        
        self.scat.addPoints(spots)

    def setData_old(self, data, dotsize=2, ydiv=4, yoffset=7, ymajor=8, failures=None):
        spots = []
        for y, d in enumerate(data):
            for x, p in enumerate(d):
                if p > 0:
                    bsh = pg.mkBrush(self.rgb(0, 100, p))  # RGBA
                    spots.append({'pos': (x, float(y) / float(ydiv) - yoffset), 'size':dotsize, 'pen': {'color': pg.mkColor(self.rgb(0, 100, p)), 'width':0}, 'symbol':'s', 'brush':bsh})

            if failures and failures[y] > 0:
                bsh = pg.mkBrush(self.rgb(0, 100, failures[y]))  # RGBA
                spots.append({'pos': (-1, float(y) / float(ydiv) - yoffset), 'size':4, 'pen': {'color': pg.mkColor(self.rgb(0, 100, failures[y])), 'width':0}, 'symbol':'d', 'brush':bsh})
                self.plot.addLine(y=float(y) / float(ydiv) - yoffset, pen={'color': pg.mkColor(self.rgb(0, 100, failures[y])), 'width':0.4})

        self.scat.addPoints(spots)

        numbits = len(data[0])
        self.plot.setXRange(0, numbits)

        majorticks = [ (i, "%d" % i) for i in range(0, numbits, 8) ]
        minorticks = [ (i, "") for i in range(0, numbits) ]
        self.plot.getAxis('bottom').setTicks([ majorticks, minorticks  ])
        self.plot.getAxis('bottom').setGrid(50)

        majorticks = [ (i, "%d" % i) for i in range(0, len(data) / ydiv, ymajor) ]
        # minorticks = [ (i, "%d" % i) for i in range(0, len(data) / ydiv, 2) ]
        self.plot.getAxis('left').setTicks([ majorticks, []  ])
        self.plot.getAxis('left').setGrid(50)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    app = QApplication([])
    mw = QMainWindow()
    mw.resize(800, 800)

    piwidget = BitPlotWidget()

    data = []
    for j in range(0, 500):
        # newdata = [ random.randint(0, 100) > 95 for i in range(0, 64) ]
        newdata = [ random.randint(0, 100) if random.randint(0, 100) > 95 else 0 for i in range(0, 64) ]
        data.append(newdata)

    piwidget.setData(data)

    mw.setCentralWidget(piwidget)
    mw.show()
    mw.setWindowTitle('Ploterrific Jerkface')


    app.exec_()
