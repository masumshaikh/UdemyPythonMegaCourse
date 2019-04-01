# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 17:18:10 2019

@author: e1081018
"""

from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html


def write_plot_page(out_html_file):
    plot = figure()
    plot.circle([1,2], [3,4])
    
    html = file_html(plot, CDN, "my plot")
    with open(out_html_file, "w") as plot_file:
        plot_file.write(html)
