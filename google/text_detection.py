from base64 import b64encode

import googleapiclient.discovery
import argparse
import base64
import csv
import httplib2
import datetime
import json
import os
import glob
from apiclient.discovery import build
from oauth2client.client import GoogleCredentials
from google.protobuf.json_format import MessageToJson

# Globals
timestamp = str(datetime.datetime.now())
json_file_name = "ocr_1000_sample_" + timestamp + "-ocr.json"
csv_file_name = "ocr_1000_sample_" + timestamp + "-ocr.csv"
http = httplib2.Http()
CREDENTIALS_FILE = "pt-ocr-cred.json"
imgnames = sorted(glob.glob("images/*.jpg"))


def store_json(json_input):
    with open(json_file_name, "a") as f:
        f.write(json_input)
        f.write('\n')


def store_csv(csv_input):
    with open(csv_file_name, 'a') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        try:
            csv_writer.writerow(csv_input)
        except UnicodeEncodeError:  # TODO: handle unicode OR just run with Python 3 :)
            csv_writer.writerow(["ERROR"])

# Connect to the Google Cloud-ML Service
credentials = GoogleCredentials.from_stream(CREDENTIALS_FILE)
service = googleapiclient.discovery.build('vision', 'v1', credentials=credentials)
credentials.authorize(http)

# Read file and convert it to a base64 encoding

# Read file and convert it to a base64 encoding
for i in imgnames:
    with open(i, "rb") as f:
        image_data = f.read()
        encoded_image_data = b64encode(image_data).decode('UTF-8')

    batch_request = [{
        'image': {
            'content': encoded_image_data
        },
        'features': [{
            'type': 'TEXT_DETECTION',
            'maxResults': 100
        }]
    }]

    request = service.images().annotate(body={'requests': batch_request})

    # Send the request to Google
    response = request.execute()

    # Check for errors
    if 'error' in response:
        raise RuntimeError(response['error'])

     # Prepare parsing of responses into relevant fields
    query = i
    comma = ''
    all_labels = ''
    all_text = ''

    # Check for errors
    if 'error' in response:
        raise RuntimeError(response['error'])

    try:
        texts = response['responses'][0]['textAnnotations']
        for text in texts:
            text = response['responses'][0]['textAnnotations'][0]['description']
            # text_val = text['description']
            print('Found text: "%s"' % text)
            # all_text = text + ', '
    except KeyError:
            text = " "
            print("N/A text found")

    print('\n= = = = = Image Processed = = = = =\n')

    response["query"] = i
    csv_response = [query, text, comma]

    response = json.dumps(response, indent=3)
    store_json(response)
    store_csv(csv_response)
