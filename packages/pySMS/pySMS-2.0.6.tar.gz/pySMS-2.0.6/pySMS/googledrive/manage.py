# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 11:03:43 2016

@author: doarni
"""


from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import os

class api():
    
    def __init__(self):
        self.gauth = GoogleAuth()
        self.drive = None
        self.credFile = os.path.dirname(os.path.realpath(__file__)) + "\\credentials.txt"
        self.loadCredFile()
        
    def loadCredFile(self):
        self.gauth.LoadCredentialsFile(self.credFile)
        if self.gauth.credentials is None:
            self.gauth.LocalWebserverAuth()
        elif self.gauth.access_token_expired:
            self.gauth.Refresh()
        else:
            self.gauth.Authorize()
        self.gauth.SaveCredentialsFile(self.credFile)
        self.drive = GoogleDrive(self.gauth)

    def createFolder(self, title):
        folder_metadata = {'title' : title,'mimeType' : 'application/vnd.google-apps.folder'}
        folder = self.drive.CreateFile(folder_metadata)
        folder.Upload()
        return folder 

    def uploadToDrive(self, _path, fname):              
        file1 = self.drive.CreateFile({'title': fname, "parents": [{"kind": "drive#fileLink", "id": '0BzqXAFBoentOVkd4dWh1U05yQzA'}]})
        file1.SetContentFile(_path)
        file1.Upload()     
       
    def trashJsonDataFile(self):
        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file1 in file_list:
            if file1['mimeType'] == 'application/vnd.google-apps.folder':
                if file1['title'] == 'updates':
                    file_list2 = self.drive.ListFile({'q': "'%s' in parents and trashed=false" % file1['id']}).GetList()
                    for file2 in file_list2: 
                        if file2['title'] == 'VERSION_KEYS.json':
                            file2.Trash()
                            
                    
    def downloadFile(self, filename):
        file_id = '0BzqXAFBoentOVkd4dWh1U05yQzA'
        file_list2 = self.drive.ListFile({'q': "'%s' in parents and trashed=false" % file_id}).GetList()
        for file2 in file_list2: 
            if file2['title'] == filename + '.zip':
                fileZip = self.drive.CreateFile({'id': file2['id']})
                fileZip.GetContentFile(filename + '.zip')

    def getAllFiles(self):
        list = []
        file_id = '0BzqXAFBoentOVkd4dWh1U05yQzA'
        file_list2 = self.drive.ListFile({'q': "'%s' in parents and trashed=false" % file_id}).GetList()
        for file2 in file_list2: 
            list.append({'_title': file2['title'], '_id': file2['id']})
        return list

