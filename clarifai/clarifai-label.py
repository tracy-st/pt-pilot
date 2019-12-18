import numpy as np
import glob
import json
import csv
import types
import sys
import httplib2
import datetime

from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
from clarifai.rest import UserError
from clarifai.rest import ModelOutputConfig, ModelOutputInfo

# ADD CREDENTIALS HERE
api_key = 'API_KEY'

from clarifai.rest import ClarifaiApp
app = ClarifaiApp()

# Globals
timestamp = str(datetime.datetime.now())
csv_file_name = "pilot_" + timestamp + "_clarifai-label.csv"
http = httplib2.Http()

def store_csv(csv_input):
    with open(csv_file_name, 'a') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        try:
            csv_writer.writerow(csv_input)
        except UnicodeEncodeError:  
            csv_writer.writerow(["ERROR"])
            
imgnames = sorted(glob.glob("images/*.png"))

for i in imgnames:
    out = app.tag_files([i])
    json_str = json.dumps(out)
    data = json.loads(json_str)
    concepts = data['outputs'][0]['data']['concepts']

    url = data['outputs'][0]['input']['data']['image']['url']
    query = i
    all_labels = ''

    for i in concepts:
        name = str(i['name'])
        value = str(i['value'])
        all_labels += name + ' , ' + value + ', '
        
    csv_response = [url, all_labels]
    store_csv(csv_response)
