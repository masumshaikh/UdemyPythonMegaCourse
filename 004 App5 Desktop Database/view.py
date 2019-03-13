# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 20:50:12 2019

@author: Masum Shaikh
"""
import tkinter as Tk
        
class View():
    # Define three frames and grid them into the window
    # Items in each frame will be packed or gridded depending on the frame.
    def __init__(self, window):
        # Not actually necessary to pass the rows, columns etc from here:
        # Could do eg, ... = TopFrame(window) and specify them inside each class.
        # But this pattern makes it easy to see ...
        # ...the layout of the frames here in one place.
        self.topframe = TopFrame(window, \
                                 row = 0, column = 0, columnspan = 2)
        self.bottomleftframe = BottomLeftFrame(window, \
                                 row = 1, column = 0)     
        self.bottomrightframe = BottomRightFrame(window, \
                                 row = 1, column = 1)

        window.grid_rowconfigure(0, weight=0) # First row doesn't resize.
        window.grid_rowconfigure(1, weight=1) # Second row does

        window.grid_columnconfigure(0, weight=4) # First column resizes 4x faster
        window.grid_columnconfigure(1, weight=1) # than the second
        
class TopFrame():
    def __init__(self, window, row, column, columnspan):
        self.frame = Tk.Frame(window)
        self.frame.grid(row = row, column = column, columnspan = columnspan)
        
        self.lb_title = Tk.Label(self.frame, text = "Title")
        self.lb_author = Tk.Label(self.frame, text = "Author")
        self.lb_year = Tk.Label(self.frame, text = "Year")
        self.lb_isbn = Tk.Label(self.frame, text = "ISBN")

        self.title  = Tk.StringVar()
        self.author = Tk.StringVar()
        self.year   = Tk.StringVar()
        self.isbn   = Tk.StringVar()

        self.e_title  = Tk.Entry(self.frame, textvariable = self.title)
        self.e_author = Tk.Entry(self.frame, textvariable = self.author)
        self.e_year   = Tk.Entry(self.frame, textvariable = self.year)
        self.e_isbn   = Tk.Entry(self.frame, textvariable = self.isbn)
                
        self.lb_title.grid(row = 0, column = 0)
        self.e_title.grid(row = 0, column = 1)        
        self.lb_author.grid(row = 0, column = 2)
        self.e_author.grid(row = 0, column = 3)        
        
        self.lb_year.grid(row = 1, column = 0)
        self.e_year.grid(row = 1, column = 1)        
        self.lb_isbn.grid(row = 1, column = 2)
        self.e_isbn.grid(row = 1, column = 3)               
   
class BottomLeftFrame():
    def __init__(self, window, row, column):
        self.frame = Tk.Frame(window, borderwidth = 5)

        # The fill parameters won't work when we pack() the buttons ...
        # ...into this frame unless the sticky is set as below.
        self.frame.grid(row = row, column = column, sticky = "nsew")
        
        # The expand parameter is to ensure the listbox fills the frame in ... 
        # ...both directions.
        # (Although even without it, the listbox does expand horizontally [??]).
        self.listbox = Tk.Listbox(self.frame, selectmode = Tk.EXTENDED)
        self.listbox.pack(fill = Tk.BOTH, expand = 1)

        # TODO: add scrollbar for listbox

class BottomRightFrame():
    def __init__(self, window, row, column):
        self.frame = Tk.Frame(window, borderwidth = 5)
        
        # The anchor and fill parameters won't work when we ...
        # ... pack() the buttons into this frame unless the sticky is set as below.
        self.frame.grid(row = row, column = column, sticky = "nsew")
        
        self.viewall = Tk.Button(self.frame, text = "View All")
        self.search  = Tk.Button(self.frame, text = "Search Entry")
        self.add     = Tk.Button(self.frame, text = "Add Entry")
        self.update  = Tk.Button(self.frame, text = "Update")
        self.delete  = Tk.Button(self.frame, text = "Delete")
        self.close   = Tk.Button(self.frame, text = "Close")

        # Pack() from the top down (anchor = 'n') ...
        # ... and fill the horizontal width of the frame (fill = 'x').
        self.viewall.pack(anchor = 'n', fill='x')
        self.search.pack(anchor = 'n', fill='x')
        self.add.pack(anchor = 'n', fill='x')
        self.update.pack(anchor = 'n', fill='x')
        self.delete.pack(anchor = 'n', fill='x')
        self.close.pack(anchor = 'n', fill='x')
        
        
