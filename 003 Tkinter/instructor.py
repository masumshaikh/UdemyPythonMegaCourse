# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 22:04:06 2019

@author: e1081018
"""

import tkinter as Tk

def km_to_miles():
    s = e1_value.get()
    if len(s) > 0:
        miles = float(s)*1.6
        t1.delete(1.0, Tk.END)
        t1.insert(Tk.END, miles)

root = Tk.Tk()

b1 = Tk.Button(root, text = "Execute", command = km_to_miles)

e1_value = Tk.StringVar()
e1 = Tk.Entry(root, textvariable = e1_value)

t1 = Tk.Text(root, height = 1, width = 20 )


b1.grid(row = 0, column = 0)
e1.grid(row = 0, column = 1)
t1.grid(row = 0, column = 2)

root.mainloop()