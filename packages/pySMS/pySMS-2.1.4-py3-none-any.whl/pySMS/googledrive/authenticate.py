# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 11:45:04 2016

@author: doarni
"""

from pydrive.auth import GoogleAuth
import os

os.system('del /s /q credentials.txt')

class api():
    
    def __init__(self):
        self.gauth = GoogleAuth()
        self.gAuthO()        
        
    def gAuthO(self):
        self.gauth.LocalWebserverAuth()

if __name__ == '__main__':
    a = api()