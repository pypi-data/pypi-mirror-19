# -*- coding: utf-8 -*-
import requests
import json

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


def build_file_names(selection):

    service_layer = selection['service_layer']
    dataformat = selection['dataformat']
    selection_type = selection['selection_type']
    selection_details = selection['selection_details']
    service_name = selection['service_name']

    if not service_name:
        return [selection_details]

    selection_file = get_selection_file(service_name)
    files = []
    if selection_file:
        for f in selection_file['features']:    
            fname = f['properties']['n']
            fid = f.get('id')
            files.append(make_file_name(service_layer, fid, fname, selection_details, dataformat))
        return files
    
    return selection_details


def make_file_name(service_layer, fid, fname, selection_details, dataformat):
    filename = service_layer
    if fid:
        filename +=  u'_' + str(fid) 
    filename += u'_' + fname +  selection_details + '_' + dataformat +'.zip'
    filename = filename.replace(u'ø', u'o').replace(u'Ø',u'O')
    filename = filename.replace(u'æ', u'e').replace(u'Æ',u'E')
    filename = filename.replace(u'å', u'a').replace(u'Å',u'A').replace(' ', '_')
    return filename
 