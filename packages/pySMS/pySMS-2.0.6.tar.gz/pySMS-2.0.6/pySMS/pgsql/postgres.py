# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 08:11:44 2016

@author: doarni
"""

import os
import json
import pySMS.pgsql.cipher as cipher
import psycopg2
import traceback

from colorama import init, Fore
init(autoreset=True)

class Postgres():
    
    def __init___(self):
        self.path = os.path.dirname(os.path.realpath(__file__))

        self.con = None
        self.cur = None
        self._user = None
        self._pass = None
        self._host = None
        
        self.postgres_data = None
        
        
    def load_postgres_data(self):
        with open(os.path.dirname(os.path.realpath(__file__)) + '\\postgres_data.json', 'r') as fp:
            self.postgres_data = json.load(fp)
        self._user = cipher.decipher(self.postgres_data['data']['value1'].encode())
        self._pass = cipher.decipher(self.postgres_data['data']['value2'].encode())
        self._host = cipher.decipher(self.postgres_data['data']['value3'].encode())

    def test_connection(self, N=5):
        print(Fore.LIGHTYELLOW_EX + 'Testing connection to postgres')
        for i in range(0,N):
            try:
                self.con = psycopg2.connect("dbname=postgres user=" + self._user + " host=" + self._host + " password=" + self._pass)
                self.cur = self.con.cursor()
                print(Fore.LIGHTMAGENTA_EX + 'Connection Available!\n')
                self.con.close()
                break
            except Exception as e:
                log = format(str(e))
                log_ = traceback.format_exc()+'.\n'+log
                print(Fore.LIGHTRED_EX + 'Could not establish connection after [' + str(i + 1) + '] tries.')
                print(Fore.LIGHTRED_EX + 'Full Trackback: ' + Fore.LIGHTWHITE_EX + log_)

    def establish_connection(self):
        self.con = psycopg2.connect("dbname=postgres user=" + self._user + " host=" + self._host + " password=" + self._pass)
        self.cur = self.con.cursor()
        print(Fore.LIGHTGREEN_EX + 'Successfully Connected!\n')
        
        
    def close_connection(self):
        print(Fore.LIGHTYELLOW_EX + 'Closing connection to postgres')
        try:
            self.con.close()
            print(Fore.LIGHTGREEN_EX + 'Connection Closed.\n')            
        except:
            print(Fore.LIGHTRED_EX + 'Unable to close connection to host: ' + self._host)
        

    def execute(self, query):
        if self.con == None:
            print(Fore.LIGHTRED_EX + 'Unable to execute query. No connection has been established with the server.\n')
        else:
            self.cur.execute(query)
            self.con.commit()
            try:
                data = self.cur.fetchall()
                print(Fore.LIGHTMAGENTA_EX + 'Query Completed')
                return data
            except:
                print(Fore.LIGHTMAGENTA_EX + 'No data recieved')
            
    
