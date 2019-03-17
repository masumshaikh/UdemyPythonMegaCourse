# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 22:58:00 2019

@author: e1081018
"""

from flask import Flask

app = Flask(__name__)
@app.route('/')

def home():
    return "Can't believe I spent money to learn how to do this!"

if __name__ == '__main__':
    app.run(debug=True)

    