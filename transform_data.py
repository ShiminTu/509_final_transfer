/*
import data in cloud storage to big query
*/


from dotenv import load_dotenv
load_dotenv()
import datetime as dt
import os
from google.cloud import storage
from google.cloud import bigquery

bucket_name = os.environ['PIPELINE_DATA_BUCKET']
blob_name = f'restaurants_{dt.date.today()}.json'
uri = 'gs://%s/%s' % (bucket_name, blob_name)

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of the table to create.
table_id = f'musa5092021.final.restaurants_{dt.date.today()}'

# create a bigquery load job config
job_config = bigquery.LoadJobConfig()
job_config.autodetect = True
job_config.create_disposition = 'CREATE_IF_NEEDED',
job_config.source_format = 'NEWLINE_DELIMITED_JSON',
job_config.write_disposition = 'WRITE_TRUNCATE',

load_job = client.load_table_from_uri(
    uri,
    table_id,
    location="US",  # Must match the destination dataset location.
    job_config=job_config,
)  # Make an API request.

load_job.result()  # Waits for the job to complete.

destination_table = client.get_table(table_id)
print("Loaded {} rows.".format(destination_table.num_rows))
