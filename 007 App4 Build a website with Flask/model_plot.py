# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 17:18:10 2019

@author: e1081018
"""

from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
import quandl

def get_candlesticks():
    df = quandl.get("CHRIS/ICE_T1", start_date = "2018-03-28", end_date = "2019-03-28")
    green_bars = df[df['Settle'] > df['Open']] # up days
    red_bars   = df[df['Settle'] < df['Open']] # down days 
    twelve_hours = 12*60*60*1000

    fig = figure(x_axis_type='datetime', title = "Candlestick Chart", width=1000, height = 300)
    fig.vbar(green_bars.index, width=1, bottom=green_bars["Low"], top=green_bars["High"], color="black")
    fig.vbar(green_bars.index, width=twelve_hours, bottom=green_bars["Open"], top=green_bars["Settle"], color="green")
    
    fig.vbar(red_bars.index, width=1, bottom=red_bars["Low"], top=red_bars["High"], color="black")
    fig.vbar(red_bars.index, width=twelve_hours, bottom=red_bars["Open"], top=red_bars["Settle"], color="red")

    return fig

def write_plot_page(out_html_file):
    plot = get_candlesticks()
   
    html = file_html(plot, CDN, "my plot")
    with open(out_html_file, "w") as plot_file:
        plot_file.write(html)
