# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import yaml
import json
import log
import html
from models.dataset import Dataset
from dataset_downloader import DatasetDownloader


baseurl = "http://data.kartverket.no"

def build_datasets(username, password, name_filter=[]):
    next_link = "/download/content/geodataprodukter?korttype=All&aktualitet=All&datastruktur=All&dataskema=All"
    datasets = []
    while next_link:
        url = baseurl + next_link
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')

        pager_next = soup.find('li', {'class': 'pager-next'})
        temp = parse_datasets(res)
        for d in temp:
            if not any(x in d.name for x in name_filter):
                datasets.append(d)
        if pager_next:
            next_link = pager_next.find('a')['href']
        else:
            next_link = None

    datasets = add_download_directory(username, password, datasets)
    return datasets

def add_download_directory(username, password, datasets):

    dl = DatasetDownloader(username, password)
    for dataset in datasets:

        order_receipt = dl.order_dataset(dataset, limit=1)
        mydlsres = dl.kapi.get("http://data.kartverket.no/download/mine/downloads")
        log.html(mydlsres, filename="getdownloadurl")

        link  = html.get_download_url(mydlsres.text, order_receipt.order_id)

        dataset.download_link = link
    return datasets

def parse_datasets(res):
    soup = BeautifulSoup(res.text, 'html.parser')
    views = soup.findAll('div', {'class': 'views-row'})
    datasets = []
    for view in views:
        div = view.find('div', {'class': 'views-field-body'})
        if div != -1:
            el = div.find('a')
            datasetid = el['href'].replace("/download/content/", "")
            name = el.text            
            datasets.append(Dataset(datasetid, name))

    return datasets

def get_select_for_dataset(link):
    url = "http://data.kartverket.no"
    res = requests.get(url + '/' +link)
    log.html(res)
    line = next(line for line in res.text.split('\n') if
                line.startswith('jQuery.extend(Drupal.settings'))
    kms_widget = json.loads(
            line.replace('jQuery.extend(Drupal.settings, ', '').replace(');', '')
        ).get('kms_widget', {})    
    return kms_widget



def get_selection_file(name):
    url = "http://www.norgeskart.no/json"
    if name.startswith('dtm-dekning'):
        res = name.split('-')
        url += "/" + res[1] + '/' + res[0] + '/' + res[2] + '.geojson'

    elif name.startswith(('dtm-sjo')):
        res = name.split('-')
        url += "/dekning/sjo/celler/dtm50_" + res[2] + '.geojson'

    elif name.startswith(('raster')):
        url += "/dekning/" + "/".join(name.split('-')) + '.geojson'

    else: 
        url += '/norge/' +  name + '.json'
    res = requests.get(url)
    return json.loads(res.text)


def save_selection_file(directory, name, geojson):
    with open(directory + '/' + name, 'w') as fp:
        json.dump(geojson, fp)

if __name__ == '__main__':

    username = "username"
    password = "password"

    datasets = build_datasets(username, password, name_filter=[
        'Illustrasjonskart', 
        'Raster', 
        'kommuneinndeling', 
        'Digital terrengmodell', 
        'UTM 32', 
        'UTM 35', 
        'TEST',
        'N1000 Kartdata',
        'N500 Kartdata',
        'N250 Kartdata',
        'N5000 Kartdata'
        ] )


    with open('config/datasets.yaml', 'w') as fp:
        yaml.safe_dump([d.to_dict() for d in datasets], stream=fp, encoding='utf-8', allow_unicode=True)
