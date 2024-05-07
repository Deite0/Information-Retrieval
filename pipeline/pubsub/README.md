# Pub/Sub Publisher Example

This guide demonstrates how to publish a message to a Google Cloud Pub/Sub topic using Python.

## Prerequisites

- Python 3.x
- Google Cloud SDK
- A valid GCP project with Pub/Sub enabled
- A service account key with Pub/Sub publish permissions

## Setup

1. **Install Google Cloud Pub/Sub Library:**

   Make sure you have the `google-cloud-pubsub` library installed:

   ```bash
   pip install google-cloud-pubsub
    ```
2. **Create a Service Account Key:**
    - Go to the Google Cloud Console.
    - Create a new service account or use an existing one with the necessary permissions.
    - Download the service account key JSON file and save it in an appropriate location.
3. **Set the GOOGLE_APPLICATION_CREDENTIALS Environment Variable:**
Update the path to your downloaded service account key file in the code:
    ```bash
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/key.json'
    ```
    Alternatively, set this variable directly in your shell before running the script:
    ```bash
    export GOOGLE_APPLICATION_CREDENTIALS='path/to/your/key.json'
    ```

## Further Information
For more detailed information on Google Cloud Pub/Sub, visit the [official documentation](https://cloud.google.com/pubsub/docs).