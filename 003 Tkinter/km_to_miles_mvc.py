# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 22:17:53 2019

@author: e1081018
"""

import tkinter as Tk

class Model():
    def km_to_miles(self, s):
        if len(s) > 0:
            return float(s)*1.6

class View():
    def __init__(self, master):
        self.b1 = Tk.Button(master, text = "Execute")
        
        self.e1_value = Tk.StringVar()
        self.e1 = Tk.Entry(master, textvariable = self.e1_value)
        
        self.t1 = Tk.Text(master, height = 1, width = 20 )

        self.b1.grid(row = 0, column = 0)
        self.e1.grid(row = 0, column = 1)
        self.t1.grid(row = 0, column = 2)
        
    def output(self, miles):
        self.t1.delete(1.0, Tk.END)
        self.t1.insert(Tk.END, miles)

class Controller():
    def __init__(self):
        self.root = Tk.Tk()
        self.model = Model()
        self.view = View(self.root)
        self.view.b1.bind("<Button>", self.execute)

    def run(self):
        self.root.title("Toy Tkinter MVC example")
        self.root.mainloop()
        
    def execute(self, event):
        km = self.view.e1_value.get()
        miles = self.model.km_to_miles(km)
        self.view.output(miles)
    
if __name__ == '__main__':
    c = Controller()
    c.run()
