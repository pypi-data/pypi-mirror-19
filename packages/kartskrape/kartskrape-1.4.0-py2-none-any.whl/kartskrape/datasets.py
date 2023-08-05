# -*- coding: utf-8 -*-
import yaml
import os
from models.dataset import Dataset

def load():
    datasets = dict()
    path = os.path.dirname(__file__) + "/config/datasets.yaml"  

    with open(path, "r") as f:
        dsets = yaml.load(f)
        for d in dsets:
            datasets[d['id']] = Dataset(d['id'], d['name'], download_link=d.get('download_link'))
    return datasets