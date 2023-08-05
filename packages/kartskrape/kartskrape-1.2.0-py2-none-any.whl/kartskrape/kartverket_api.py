# -*- coding: utf-8 -*-
from utils import log
import requests
from bs4 import BeautifulSoup
import os   
baseurl = "http://data.kartverket.no"


class KartverketApiHelper(object):

    def __init__(self, username, password):
        
        self.username = username
        self.password = password
        self.url = {
            'authenticate' : 'http://data.kartverket.no/download/content/velkommen?destination=node/134',
            'login_page' : 'http://data.kartverket.no/download/content/geodataprodukter'
        }

    def get_login_payload(self, username, password, form_build_id):
        return {
            'name': username,
            'pass': password,
            'form_build_id': form_build_id,
            'form_id':'user_login_block',
            'op':'Logg inn'
        }

    def get_login_page(self):
        res = requests.get(self.url['login_page'])
        return res

    def get_input_val(self, response, form_name):         
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            return soup.find('input', {'name' : form_name}).get('value')
        except:
            return None



    def get_form_build_id(self, response):
        return self.get_input_val(response, 'form_build_id')

    def get_form_id(self, response):
        return self.get_input_val(response, 'form_id')

    def get_form_product_id(self, response):
        return self.get_input_val(response, 'product_id')

    def get_form_token(self, response):
        return self.get_input_val(response, 'form_token')

    def get_form_action_by_id(self, response, idsel):
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            return soup.find('form').get('action')
        except:
            return None

    def build_datasets():
        next_link = "/download/content/geodataprodukter?korttype=All&aktualitet=All&datastruktur=All&dataskema=All"
        datasets = []

        while next_link:
            url = baseurl + next_link
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')

            pager_next = soup.find('li', {'class': 'pager-next'})
            datasets.append(parse_datasets(res))
            if pager_next:
                next_link = pager_next.find('a')['href']
            else:
                next_link = None
        

    def login(self):
        response = self.get_login_page()        
        form_build_id = self.get_form_build_id(response)
        if form_build_id:
            payload = self.get_login_payload(self.username, self.password, form_build_id)
            session = self.create_session()
            res = session.post(self.url['authenticate'], data = payload)
            self.cookies = session.cookies
            self.session = session
            return self.get_login_page()

        raise Exception("Login failed")

    def get(self, url, headers=None):

        if not headers:
            headers = {            
                'Cookie' : self.get_auth_cookie()
            }
        else:
            headers['Cookie'] = self.get_auth_cookie()

        return self.session.post(url)


    def get_auth_cookie(self):
        res = self.session.cookies.get_dict()
        cookie_str = ""
        for k in res:
            cookie_str = k + "=" + res[k]
        return cookie_str

    def post(self, url, payload, headers=None):
        if not headers:
            headers = {            
                'Cookie' : self.get_auth_cookie()
            }
        else:
            headers['Cookie'] = self.get_auth_cookie()

        return self.session.post(url, data=payload, headers=headers)
    
    def download_file(self, url, download_directory):
        file_name = url.split('/')[-1]

        local_filename = download_directory + "/" + url.split('/')[-1]
        r = self.session.get(url, stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk:
                    f.write(chunk)
        return file_name, local_filename

    def create_session(self):
        return requests.Session()
