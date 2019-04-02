# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 22:58:00 2019

@author: e1081018
"""

import model_plot as mp
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/') # this means the page is the home page
def home():
    return render_template("home.html")

@app.route('/about/') # this means the page is in the /about/ directory
def about():
    return render_template("about.html")

@app.route('/stock/')
def stock():
    mp.write_plot_page("templates/stock.html")
    return render_template("stock.html")

@app.route('/components/')
def components():
    return render_template("components.html")

if __name__ == '__main__':
    app.run(debug=True)

    