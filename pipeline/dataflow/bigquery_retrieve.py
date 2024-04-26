import pandas as pd
from google.cloud import bigquery
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'pipeline/pubsub/analog-button-421413-e0072d12a2ba.json'

def fetch_data_to_dataframe():
    client = bigquery.Client()

    # Define your SQL query
    query = """
        SELECT * 
        FROM `analog-button-421413.WikiData.WikiData-Main` 
        WHERE TIMESTAMP_TRUNC(_PARTITIONTIME, DAY) = TIMESTAMP("2024-04-26")
        LIMIT 100
    """

    query_job = client.query(query)  # Make an API request.

    df = query_job.to_dataframe()

    print(df.head())

    return df

if __name__ == '__main__':
    df = fetch_data_to_dataframe()
