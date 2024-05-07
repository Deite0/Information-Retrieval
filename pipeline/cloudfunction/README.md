# Update Categories and Trigger Dataflow - README

## Overview

This Python script is a Google Cloud Function that updates a list of categories stored in a Google Cloud Storage bucket. It's triggered by a Google Cloud Pub/Sub message, which contains new category data. The function updates a CSV file by adding a new category if it's not already present. Optionally, it can trigger a downstream process.

## Prerequisites

1. **Google Cloud SDK**: Install and authenticate the SDK for your project.
2. **Google Cloud Storage**:
    - Create a bucket where the `unprocessed_categories.csv` file will be stored.
    - Ensure that this bucket has appropriate permissions for read and write access.
3. **Google Cloud Pub/Sub**: Create a topic to publish new category information.

## Setup Instructions

### Step 1: Installing Dependencies

Ensure that the following Python libraries are installed:

```bash
pip install google-cloud-storage google-cloud-pubsub
```
### Step 2: Set Up Google Cloud Storage

1. Create a Cloud Storage bucket with a unique name.
2. Upload a CSV file containing the initial categories data.

```bash
# Create a new bucket (replace with your unique bucket name)
gsutil mb gs://your-bucket-name

# Prepare and upload an initial CSV file
echo "initial_category_name" > unprocessed_categories.csv
gsutil cp unprocessed_categories.csv gs://your-bucket-name/
```

### Step 3: Deploy Cloud Function
Create and deploy the Cloud Function that listens to your Pub/Sub topic.
```bash
gcloud functions deploy update_categories_and_trigger_dataflow \
    --runtime python39 \
    --trigger-topic your-pubsub-topic \
    --entry-point update_categories_and_trigger_dataflow
```

### Pub/Sub Message Structure
Messages sent to your Pub/Sub topic should have this JSON structure:
```bash
{
  "category_name": "new_category"
}
```

### How it Works
1. Trigger: The function is triggered by Pub/Sub messages.
2. Decoding: It decodes the base64-encoded Pub/Sub message and converts it to JSON.
3. New Category: The new category is retrieved from the message.
4. Update Process:
    - Downloads the existing categories.csv file from Google Cloud Storage.
    - Checks if the new category is already present.
    - Adds it to the file if not present, then uploads the updated file.

### Troubleshooting
1. Permissions: Ensure that the service account has the right permissions to read/write to the storage bucket.
2. CSV File Missing: Ensure that the categories.csv file exists in the specified bucket before invoking the function.
3. Google Cloud Function Logs: Check the logs if the function isn't working as expected, and ensure the correct Pub/Sub message structure.
