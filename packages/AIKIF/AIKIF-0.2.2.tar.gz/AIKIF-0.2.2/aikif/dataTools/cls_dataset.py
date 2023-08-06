#!/usr/bin/python3
# -*- coding: utf-8 -*-
# cls_dataset.py

class DataSet(object):
    """
    A dataset contains a list of data tables. This can be
    a database schema, website, a folder on an operating 
    system containing a list of files. (Excel files are 
    handled separately - probably not worth wrapping them
    here as well.
    """
    def __init__(self, name, dataset_type, creds=''):
        """
        a dataset_type can be the following:
        folder  = folder on hard drive
        table   = database table
        website = a list of pages (each page can also be a dataset)
        dataset = can be a recursive call for folders or webpages
        """
        self.name = name
        self.dataset_type = dataset_type
        self.datatables = []
        self.connection = None
        if len(creds) == 3:
            self.schema = creds[0]
            self.username = creds[1]
            self.password = creds[2]

        
    def __str__(self):
        return self.name + ' contains the tables \n' + self.list_tables() 
    
    def login(self, schema, username, password):
        """
        connect here - use the other classes cls_oracle, cls_mysql, etc
        otherwise this has the credentials used to access a share folder
        """
        self.schema = schema
        self.username = username
        self.password = password
        self.connection = schema
        
    def logout(self):
        print('Logging out')
        self.connection = None
    
    def list_tables(self, delim='\n'):
        """
        return a list of data tables as a string
        """
        return delim.join([tbl for tbl in self.datatables])
        
    def add(self, table):	
        self.datatables.append(table)

