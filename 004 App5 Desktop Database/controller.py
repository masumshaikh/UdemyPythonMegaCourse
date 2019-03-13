# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 20:51:25 2019

@author: Masum Shaikh
"""

import tkinter as Tk
import tkinter.messagebox

from view import View
from model import Model
from model import Record

class Controller():
    
    def __init__(self):
        self.root = Tk.Tk()
        self.model = Model("unittests.db")
        self.view = View(self.root)
        
    def run(self):
        self.root.title("Desktop Database App")
        self.root.protocol("WM_DELETE_WINDOW", self.close_application)

        # Apparently you're not supposed to use bindings?
        # But I think you have to, if you're trying to keep View and Controller separate
        # https://stackoverflow.com/questions/28089035/tkinter-event-binding-remains-after-application-terminates
        self.view.bottomrightframe.viewall.bind("<Button>", self.viewall)
        self.view.bottomrightframe.search.bind("<Button>", self.search)
        self.view.bottomrightframe.add.bind("<Button>", self.add)
        self.view.bottomrightframe.update.bind("<Button>", self.update)
        self.view.bottomrightframe.delete.bind("<Button>", self.delete)
        self.view.bottomrightframe.close.bind("<Button>", self.close_application)
        
        self.root.mainloop()

    def viewall(self, event = None):
        self.show_items_in_listbox(self.model.get_all_records())

    def search(self, event):
        title, author, year, isbn = self.get_field_values()
        search_criteria = Record(title, author, year, isbn)
        self.show_items_in_listbox(self.model.find_matching_records(search_criteria))

    def update(self, event):
        title, author, year, isbn = self.get_field_values()
        fields_to_change = Record(title, author, year, isbn)

        values = [self.view.bottomleftframe.listbox.get(idx) for idx in self.view.bottomleftframe.listbox.curselection()]
        ids_to_update = Controller.extract_ids_from_listbox_selection(values)
        
        try:
            self.model.update_records_with_id(ids_to_update, fields_to_change)
            self.viewall()
        except:
            Tk.messagebox.showinfo("Cannot update.", \
                                   "You need to select a record to update!")
            return "break"           

    def add(self, event):
        title, author, year, isbn = self.get_field_values()
        
        try:
            self.model.add_record(Record(title, author, year, isbn))        
            self.viewall()
        except:
            Tk.messagebox.showinfo("Book not valid.", \
                                   "You need to add a book with a title!")
            return "break" 

    def delete(self, event):
        # Get list containing ID(s) of selected Listbox item(s)
        # call self.model.delete_records_with_id()
        values = [self.view.bottomleftframe.listbox.get(idx) for idx in self.view.bottomleftframe.listbox.curselection()]
        ids_to_delete = Controller.extract_ids_from_listbox_selection(values)
        self.model.delete_records_with_id(ids_to_delete)
        self.viewall()

    def close_application(self, event = None):
        self.model.close_connection()
        self.root.destroy()

    def get_field_values(self):
        title = Controller.string_value_or_none(self.view.topframe.title.get())
        author = Controller.string_value_or_none(self.view.topframe.author.get())
        year = Controller.int_value_or_none(self.view.topframe.year.get())
        isbn = Controller.int_value_or_none(self.view.topframe.isbn.get())
        
        return title, author, year, isbn

    def show_items_in_listbox(self, items):
        self.view.bottomleftframe.listbox.delete(0, Tk.END)
        for book in items:
            self.view.bottomleftframe.listbox.insert(Tk.END, book)

    @staticmethod
    def extract_ids_from_listbox_selection(records):
        return [record[0] for record in records]

    @staticmethod
    def string_value_or_none(some_string):
        return some_string if len(some_string) > 0 else None
    
    @staticmethod
    def int_value_or_none(stringified_int):
        try:
            return int(stringified_int)
        except:
            return None

if __name__ == '__main__':
    c = Controller()
    c.model.populate_fake()
    c.run()
