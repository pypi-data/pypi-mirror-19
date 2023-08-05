# -*- coding: utf-8 -*-
import datetime 

class OrderReceipt(object):

    def __init__(self, order_id, dataset, files, html_result):
        self.order_id = order_id
        self.dataset = dataset
        self.files = files
        self.html = html_result
        # self.expires = datetime.now() + timedelta(hours=23, minutes=45)

    def download_links(self):
        print 
        return [self.dataset.download_link + '/' + f for f in self.files]