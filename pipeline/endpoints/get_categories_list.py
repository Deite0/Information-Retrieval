from google.cloud import storage
import pandas as pd
from io import StringIO
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "pipeline/pubsub/analog-button-421413-e0072d12a2ba.json"

class GCSBucketReader:
    def __init__(self, bucket_name, blob_name):
        self.bucket_name = bucket_name
        self.blob_name = blob_name
        self.storage_client = storage.Client()
        self.df = None

    def read_data(self):
        """Reads data from a GCS bucket blob into a pandas DataFrame."""
        bucket = self.storage_client.bucket(self.bucket_name)
        blob = bucket.blob(self.blob_name)
        
        # Read the blob's content into a string.
        data = blob.download_as_text()
        
        # Use StringIO to convert the string data into a file-like object so it can be read into a DataFrame.
        self.df = pd.read_csv(StringIO(data), header=None)

    def get_categories_list(self):
        """Returns the DataFrame if it is not None."""
        if self.df is not None:
            return self.df
        else:
            print("Data not loaded. Please call read_data() first.")
            return None

# Usage
bucket_name = 'ir-datastore'
source_blob_name_processed = 'processed_categories.csv'
source_blob_name_unprocessed = 'unprocessed_categories.csv'

# Creating two instances for processed and unprocessed data
processed_reader = GCSBucketReader(bucket_name, source_blob_name_processed)
unprocessed_reader = GCSBucketReader(bucket_name, source_blob_name_unprocessed)

# Reading data
processed_reader.read_data()
unprocessed_reader.read_data()

# Getting categories lists
processed_data = processed_reader.get_categories_list()
unprocessed_data = unprocessed_reader.get_categories_list()

# Example to display data
print("Processed Data:", processed_data)
print("Unprocessed Data:", unprocessed_data)
