#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml
import os
import requests
import datasets
from utils import log
from kartverket_api import KartverketApiHelper
from models.dataset import Dataset
from models.receipt import OrderReceipt
import selection
import json
from config import urls

class DatasetDownloader(object):

    def __init__(self, username, password, download_directory=None):
        self.data_dir = self.setup_data_dir(download_directory)
        self.datasets = datasets.load()
        res = self.login(username, password)

    def login(self, username, password):
        self.kapi = KartverketApiHelper(username, password)
        res = self.kapi.login()

    def setup_data_dir(self, data_dir):
        if not data_dir:
            data_dir = 'data'
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        return data_dir

    def confirm_bestilling(self, checkout_id, res):
        form_build_id = self.kapi.get_form_build_id(res)
        form_token = self.kapi.get_form_token(res)
        form = self.bestilling_forms.get_confirm_form(form_build_id, form_token)
        return self.kapi.post(urls.kartverket["download-checkout"] + checkout_id + "/checkout", form)

    def order(self, dataset, limit=None):
        res = self.kapi.get(dataset.url)

        
        form_build_id = self.kapi.get_form_build_id(res)
        form_token = self.kapi.get_form_token(res)
        form_id = self.kapi.get_form_id(res)
        product_id = self.kapi.get_form_product_id(res)
        widget = self.get_select_for_dataset(res)
        files = selection.build_file_names(widget)

        max_files = 50
        res = None
        n = len(files)
        if limit:
            max_files = limit
            n = 1

        for i in xrange(0, n, max_files):
            files[i:i+max_files]
            res = self.post_files_bestilling(files[i:i+max_files], product_id, form_token, form_id,  dataset.url)
        
        return files


    def get_select_for_dataset(self, res):
        line = next(line for line in res.text.split('\n') if
                    line.startswith('jQuery.extend(Drupal.settings'))
        kms_widget = json.loads(
                line.replace('jQuery.extend(Drupal.settings, ', '').replace(');', '')
            ).get('kms_widget', {})    
        return kms_widget


    def post_files_bestilling(self, files, product_id, form_token, form_id,  url):

        filer_string = "[\"" + "\", \"".join(files) + "\"]"
        data = {
            "product_id": product_id,
            "form_token": form_token,
            "form_id": form_id,
            "line_item_fields[field_selection][und][0][value]" : filer_string,
            "line_item_fields[field_selection_text][und][0][value]" : len(files),
            "quantity" : len(files),
            "op" : "Legg i kurv"
        }

        return self.kapi.post(url, data)
    
    def post_fortsett_bestilling(self, res):

        url = "http://data.kartverket.no"
        form_action = self.kapi.get_form_action_by_id(res, "commerce-checkout-form-checkout")
        form_build_id = self.kapi.get_form_build_id(res)
        form_token = self.kapi.get_form_token(res)
        url = url + form_action
        order_id = form_action.split('/')[3]

        payload = {
            'op' : 'Fortsett', 
            'form_build_id': form_build_id,
            'form_token' : form_token,
            'form_id' : 'commerce_checkout_form_checkout'
            }

        res = self.kapi.post(url, payload)
        return res, order_id


    def download_files(self, dataset, files):
        for file in files:
            self.kapi.download_file(dataset.download_path + "/" + file)

    def order_dataset(self, dataset, limit=None):
        files = self.order(dataset, limit)
        html_res = self.kapi.get(urls.kartverket["download-checkout"])
        html_res, order_id = self.post_fortsett_bestilling(html_res)
        return OrderReceipt(order_id, dataset, files, html_res)

    def download(self, dataset, download_directory):
        order_receipt = self.order_dataset(dataset)
        for link in order_receipt.download_links():
            file_name, path = self.kapi.download_file(link, download_directory)
            print file_name, path