# -*- coding: utf-8 -*-
"""
Created on Sat Dec 20 20:01:14 2014

@author: Matteo Campanelli
"""

from data import *

import plotly.plotly as py
from plotly.graph_objs import *

username = 'matteocam'
apikey = 'ds3hgpyarj'

py.sign_in(username, apikey)

def plotWeek():    
    week = Scatter(
        x = range(7),
        y = getNormalizedWeekData()
    )
        
    d = Data([week])
    plot_url = py.plot(d)
    
def plotWeekByYear():    
    weeks = []
    for y in pMailsPerWeekByYear.keys():
        week = Scatter(
            x = range(7),
            y = normalize( pMailsPerWeekByYear[y] ),
            name = str(y)
        )
        weeks.append(week)
        
    d = Data(weeks)
    plot_url = py.plot(d)
    
def plotLenPMails():
    lens, _ = getPMailsLens()

    d = Data([
            Histogram( x = lens )
            ])
    plot_url = py.plot(d, filename='histogram-lens')

def plotScatterLenSizeVocab():
    stuff = getEmailsLensSizeVocab()
    markerPMails = Marker(
        color='rgb(164, 194, 244)',
        size=8,
        line=Line(
            color='white',
            width=0.5
        ) )
    markerWkMails = Marker(
        color='rgb(255, 217, 102)',
        size=8,
        line=Line(
            color='white',
            width=0.5
        ) )
    d = Data([
            Scatter( x = stuff['pMails']['lens'], y = stuff['pMails']['vsizes'], mode='markers', marker = markerPMails, name = "pMails" ),
            Scatter( x = stuff['wkMails']['lens'], y = stuff['wkMails']['vsizes'], mode='markers', marker = markerWkMails, name = "wkMails" )
            ])
    
    plot_url = py.plot(d, filename='scatter-lens-size-vocabs')


def __plotScatterLenSizeVocab():
    lens, vsizes = __getPMailsLensSizeVocab()
    d = Data([
            Scatter( x = lens, y = vsizes, mode='markers' )
            ])
    
    plot_url = py.plot(d, filename='scatter-lens-size-vocabs-only-personal')
    