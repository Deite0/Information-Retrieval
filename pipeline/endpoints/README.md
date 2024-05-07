# Google Cloud Storage (GCS) Bucket Reader Example

This guide demonstrates how to read data from a Google Cloud Storage (GCS) bucket blob and convert it into a pandas DataFrame using Python.

## Prerequisites

- Python 3.x
- Google Cloud SDK
- Google Cloud Storage enabled for your GCP project
- A service account key with Storage Object Viewer permissions
- A CSV file stored in a GCS bucket

## Setup

1. **Install Required Libraries:**

   Make sure you have the required Python libraries installed:

   ```bash
   pip install google-cloud-storage pandas
    ```
2. **Create a Service Account Key:**
    - Go to the Google Cloud Console.
    - Create a new service account or use an existing one with Storage Object Viewer permissions.
    - Download the service account key JSON file and save it in an appropriate location.
3. **Set the GOOGLE_APPLICATION_CREDENTIALS Environment Variable:**
    Update the path to your downloaded service account key file in the code:
    ```bash
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'path/to/your/key.json'
    ```
    Alternatively, set this variable directly in your shell before running the script:
    ```bash
    export GOOGLE_APPLICATION_CREDENTIALS='path/to/your/key.json'
    ```

## Further Information
For more detailed information on Google Cloud Storage, visit the [official documentation](https://cloud.google.com/storage/docs/).