import tkinter as tk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
from tkinter import ttk
import urllib
import json
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

style.use('ggplot')
f = Figure()
a = f.add_subplot(111)

LARGE_FONT = ('Verdana', 12)
NORM_FONT = ('Verdana', 10)
DataPace = '1d'
candleWidth = 0.008
resampleSize = '15Min'
DatCounter = 9000


def changeTimeFrame(tf):

    global DataPace
    if tf == '7d' and resampleSize == '1Min':
        popupmsg('Too much data chosen!')
    else:
        DataPace = tf
        DatCounter = 9000

def changeSampleSize(size, width):
    global resampleSize
    global candleWidth
    if DataPace == '7d' and resampleSize == '1Min':
        popupmsg('Too much data Chosen')
    elif DataPace == 'tick':
        popupmsg('pls choose OHLC')
    else:
        resampleSize = size
        DatCounter = 9000
        candleWidth = width

def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title('!')
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side='top', fill='x', pady=10)
    B1 = ttk.Button(popup, text='OK', command=popup.destroy)
    B1.pack()
    popup.mainloop()


class RabbitHoleApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)

        #container.grid_rowconfigure(0, weight=1)
        #container.grid_columnfigure(0, weight=1)
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Save settings', command = lambda: popupmsg('Not Supported Yet!'))
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=quit)
        menubar.add_cascade(label='File', menu=filemenu)

        dataTF = tk.Menu(menubar, tearoff=1)
        dataTF.add_command(label = 'Tick',
                           command=lambda: changeTimeFrame('Tick'))
        dataTF = tk.Menu(menubar, tearoff=1)
        dataTF.add_command(label = '1 Day',
                           command=lambda: changeTimeFrame('1d'))
        dataTF = tk.Menu(menubar, tearoff=1)
        dataTF.add_command(label = '3 Day',
                           command=lambda: changeTimeFrame('3d'))
        dataTF = tk.Menu(menubar, tearoff=1)
        dataTF.add_command(label = '1 Week',
                           command=lambda: changeTimeFrame('7d'))

        menubar.add_cascade(label = 'Data Time Frame', menu = dataTF)

        OHLC = tk.Menu(menubar, tearoff=1)
        OHLC.add_command(label = 'Tick',
                         command=lambda: changeTimeFrame('tick'))
        OHLC.add_command(label = '1 minute',
                         command=lambda: changeSampleSize('1Min', 0.0005))
        OHLC.add_command(label = '5 minute',
                         command=lambda: changeSampleSize('5Min', 0.003))
        OHLC.add_command(label = '15 minute',
                         command=lambda: changeSampleSize('15Min', 0.008))
        OHLC.add_command(label = '30 minute',
                         command=lambda: changeSampleSize('1Min', 0.016))
        OHLC.add_command(label = '1 Hour',
                         command=lambda: changeSampleSize('1H', 0.032))
        OHLC.add_command(label = '3 Hour',
                         command=lambda: changeSampleSize('3H', 0.096))
        menubar.add_cascade(label='OHLC Interval', menu=OHLC)

        tk.Tk.config(self, menu=menubar)


        self.frames = {}

        frame = StartPage(container, self)

        for F in (StartPage, PageOne, GraphPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='StartPage', font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = tk.Button(self, text='View Page One', command=lambda: controller.show_frame(PageOne))
        button1.pack()
        button2 = tk.Button(self, text='View GraphPage', command=lambda: controller.show_frame(GraphPage))
        button2.pack()

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='PageOne', font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = tk.Button(self, text='Back to Home', command=lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = tk.Button(self, text='View GraphPage', command=lambda: controller.show_frame(GraphPage))
        button2.pack()


class GraphPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='GraphPage', font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = tk.Button(self, text='Back to Home', command=lambda: controller.show_frame(StartPage))
        button1.pack()

        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8], [5,7,4,6,3,9,8,7])
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

app = RabbitHoleApp()
app.mainloop()
