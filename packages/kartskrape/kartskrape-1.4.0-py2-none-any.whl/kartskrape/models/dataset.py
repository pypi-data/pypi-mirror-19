# -*- coding: utf-8 -*-
# from config import urls

class Dataset(object):

    def __init__(self, datasetid, name, download_link=None):
        self.id = datasetid
        self.name = name
        self.url =  "http://data.kartverket.no/download/content/" + self.id
        self.download_link = download_link

    def to_dict(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'url' : self.url,
            'download_link' : self.download_link
        }