import json
import base64
from google.cloud import storage, pubsub_v1

def update_categories_and_trigger_dataflow(data, context):
    """Triggered by a Pub/Sub message."""
    pubsub_message = data
    print("------ Raw Pub/Sub Message ------", pubsub_message)
    pubsub_message = base64.b64decode(pubsub_message['data']).decode('utf-8')
    print("------ After Decoding Message ------", pubsub_message, type(pubsub_message))
    pubsub_message_json = json.loads(pubsub_message)
    print("----- Loading to json -----", pubsub_message_json)
    new_category = pubsub_message_json["category_name"]
    print("------ New Category ------", new_category)
    
    # Initialize Cloud Storage client
    print("------ Initialising GCS Client ------")
    storage_client = storage.Client()
    bucket_name = 'ir-datastore'
    file_name = 'categories.csv'
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)

    # Download the current CSV and check for existing categories
    current_data = blob.download_as_text()
    current_lines = current_data.split('\n')
    existing_categories = set(current_lines[1:])  # Excluding the first line (assuming it may contain headers)

    if new_category not in existing_categories:
        new_data = current_data + f"\n{new_category}"
        # Upload the updated CSV
        print(f"Writing to file - {bucket_name}/{file_name}")
        blob.upload_from_string(new_data, content_type='text/csv')
        print("Added new category:", new_category)
        # Optionally trigger Dataflow or notify another service
        # For this example, we'll publish to another topic that Dataflow is subscribed to
        # publisher = pubsub_v1.PublisherClient()
        # topic_path = publisher.topic_path('your-project-id', 'your-topic-for-dataflow')
        # publisher.publish(topic_path, data=b'CSV updated')
    else:
        print("Category already exists:", new_category)
