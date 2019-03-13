# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 23:11:56 2019

@author: Masum Shaikh
"""
import os
import re
import sqlite3
from collections import namedtuple

def pattern_in_string_ci(pattern, text):
    if pattern is None:
        return True
    if type(pattern) is not str:
        pattern = str(pattern)
    if type(text) is not str:
        text = str(text)
    try_find = re.search(pattern, text, re.IGNORECASE)
    return try_find is not None

def stringify_if_not_None(x):
    return x if x is not None else str(x)

class Record(namedtuple('Record', ['title', 'author', 'year', 'isbn'])):
    # We want to check if a set of search criteria, eg [title='a', year=2000] ...
    # ... matches a 5-tuple such as is returned by the get_x() methods in Model
    def matches(self, five_tuple):
        return  pattern_in_string_ci(self.title, five_tuple[1]) \
                and pattern_in_string_ci(self.author, five_tuple[2]) \
                and pattern_in_string_ci(self.year, five_tuple[3]) \
                and pattern_in_string_ci(self.isbn, five_tuple[4])
    
    def sql_update_strings(self):
        sql_set_columns = []
        sql_parameters = []
        if (self.title is not None):
            sql_set_columns += ["title = ?"]
            sql_parameters += (self.title,)
        if (self.author is not None):
            sql_set_columns += ["author = ?"]
            sql_parameters += (self.author,)
        if (self.year is not None):
            sql_set_columns += ["year = ?"]
            sql_parameters += (self.year,)
        if (self.isbn is not None):
            sql_set_columns += ["isbn = ?"]
            sql_parameters += (self.isbn,)
        sql_set_columns = ",".join(sql_set_columns)        
        return sql_set_columns, sql_parameters
    
class Model():
    table_name = "book"
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn, cur = self.get_conn_and_cursor()
                
        sql_command = "CREATE TABLE IF NOT EXISTS {} (".format(Model.table_name)
        sql_command += "id INTEGER PRIMARY KEY, "
        sql_command += "title TEXT, "
        sql_command += "author TEXT, "
        sql_command += "year INTEGER, "
        sql_command += "ISBN INTEGER)"
        
        cur.execute(sql_command)
        self.commit_and_close()

    def add_record(self, record):
        self.conn, cur = self.get_conn_and_cursor()
        sql_command = "INSERT INTO {} VALUES (NULL, ?, ?, ?, ?)".format(Model.table_name)
        
        # Need to have at least book title populated before adding.
        if (record.title is None):
            raise # Will be caught by GUI
        cur.execute(sql_command, (record.title, record.author, record.year, record.isbn))
        self.commit_and_close()

    # fields_to_update has to be a Record            
    def update_records_with_id(self, ids, fields_to_update):
        self.conn, cur = self.get_conn_and_cursor()

        sql_set_columns, sql_parameters = fields_to_update.sql_update_strings()
        sql_mask = "(" + "?,"*(len(ids)-1)+"?)"
        sql_command = "UPDATE book SET {} WHERE id IN {}".format(sql_set_columns, sql_mask)
        sql_parameters += ids

        cur.execute(sql_command, sql_parameters)
        self.commit_and_close()

        
    def get_all_records(self):
        self.conn, cur = self.get_conn_and_cursor()
        cur.execute("SELECT * FROM {}".format(Model.table_name))
        rows = cur.fetchall()
        self.commit_and_close()
        return rows

    def num_records(self):
        self.conn, cur = self.get_conn_and_cursor()
        count = cur.execute("SELECT COUNT(*) FROM {}".format(Model.table_name))

        # count is a misnomer; it's not an int yet.
        # It's an sqlite cursor with one row. Hence the fetchone() and [0]
        num = count.fetchone()[0]
        self.commit_and_close()
        return num 
        
    def get_records_with_id(self, ids):
        self.conn, cur = self.get_conn_and_cursor()
        sql_mask = "(" + "?,"*(len(ids)-1)+"?)"
        sql_command = "SELECT * FROM {} WHERE id IN {}".format( 
                                                           Model.table_name, \
                                                           sql_mask);
        cur.execute(sql_command, ids)
        rows = cur.fetchall()
        self.commit_and_close()
        
        return rows
    
    def delete_records_with_id(self, ids):
        self.conn, cur = self.get_conn_and_cursor()
        sql_mask = "(" + "?,"*(len(ids)-1)+"?)"
        sql_command = "DELETE FROM {} WHERE id IN {}".format( \
                                                           Model.table_name, \
                                                           sql_mask);

        # TODO: how to enforce type-safety here?
        # ids can only be iterable
        # TODO: what if ids don't exist? (Apparently, nothing)
        cur.execute(sql_command, ids)
        self.commit_and_close()
            
    def find_matching_records(self, search_criteria):
        # r is just a tuple, not a Record, and the matches() method ...
        # ... is defined on Record
        return [r for r in self.get_all_records() if search_criteria.matches(r)]

    def populate_fake(self):
        if (os.path.exists("unittests.db")):
            os.remove("unittests.db")
            
        self.m = Model("unittests.db")
        # Add a bunch of records
        # Based on https://msdn.microsoft.com/en-us/windows/desktop/ms762271 ...
        # ... with fake ISBN-13 numbers.
        self.add_record(Record("XML Developer's Guide", "Gambardella, Matthew", 2000, 3304902872619))
        self.add_record(Record("Midnight Rain", "Ralls, Kim", 2000, 8280773308516))
        self.add_record(Record("Maeve Ascendant", "Corets, Eva", 2000, 7635451973929))
        self.add_record(Record("Oberon's Legacy", "Corets, Eva", 2001, 1503317573995))
        self.add_record(Record("The Sundered Grail", "Corets, Eva", 2001, 2835673347453))
        self.add_record(Record("Lover Birds", "Randall, Cynthia", 2000, 7479691608605))
        self.add_record(Record("Splish Splash", "Thurman, Paula", 2000, 6748882841314))
        self.add_record(Record("Creepy Crawlies", "Knorr, Stefan", 2000, 4796791387012))
        self.add_record(Record("Paradox Lost", "Kress, Peter", 2000, 8587815418968))
        self.add_record(Record("Microsoft .NET: The Programming Bible", "O'Brien, Tim", 2000, 6459795644823))
        self.add_record(Record("MSXML3: A Comprehensive Guide", "O'Brien, Tim", 2000, 9146816694215))
        self.add_record(Record("Visual Studio 7: A Comprehensive Guide", "Galos, Mike", 2001, 2211388125058))
    

    def get_conn_and_cursor(self):
        conn = sqlite3.connect(self.db_name)
        return conn, conn.cursor()
    
    def close_connection(self):
        self.conn.close()

    def commit_and_close(self):
        self.conn.commit()
        self.conn.close()

if __name__ == '__main__':
    m = Model("unittests.db")
    conn, cur = m.get_conn_and_cursor()
    m.populate_fake()
    print(m.get_all_records())
    conn.commit()
    conn.close()
    
