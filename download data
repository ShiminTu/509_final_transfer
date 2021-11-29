/*
download restaurants data with API
the data is json type
save it to google cloud storage
*/

from dotenv import load_dotenv
load_dotenv()

# Import additional required packages
import datetime as dt
import os
import requests
from google.cloud import storage
import json

# Retrieve data from URL
print('Downloading the restaurants data...')
response = requests.get('https://data.cityofchicago.org/resource/4ijn-s7e5.json')

# Save retrieved data to a local file
print('Saving restaurants data to a file...')

outfile_path = f'restaurants_{dt.date.today()}.json'
with open(outfile_path, mode='wb') as outfile:
    outfile.write(response.content)

with open(outfile_path, "r") as read_file:
    data = json.load(read_file)
result = [json.dumps(record) for record in data]

outfile_path1 = f'restaurants_{dt.date.today()}.json'
with open(outfile_path1, 'w') as obj:
    for i in result:
        obj.write(i+'\n')

# Upload local file of data to Google Cloud Storage
print('Uploading restaurants data to GCS...')
bucket_name = os.environ['PIPELINE_DATA_BUCKET'] 
blob_name = f'restaurants_{dt.date.today()}.json'

storage_robot = storage.Client()
bucket = storage_robot.bucket(bucket_name)
blob = bucket.blob(blob_name)
blob.upload_from_filename(outfile_path1)

print('Done.')
