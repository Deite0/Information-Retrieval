from google.cloud import pubsub_v1
import json
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS']='pipeline/pubsub/analog-button-421413-6b359e87de4a.json'

import os

from google.cloud import pubsub_v1

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'pipeline/pubsub/analog-button-421413-e0072d12a2ba.json'

class PubSubPublisher:
    def __init__(self, project_id, topic_name):
        """Initialize the Pub/Sub client and set up the topic path."""
        
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(project_id, topic_name)

    def publish_message(self, category_name):
        """Publish a message to the specified Pub/Sub topic with a variable."""
        # Create a dictionary with the category name
        message_dict = {"category_name": category_name}
        
        # Convert dictionary to JSON string
        message_json = json.dumps(message_dict)

        # Data must be a bytestring
        data = message_json.encode("utf-8")
        
        future = self.publisher.publish(self.topic_path, data=data)
        return future.result()  # Wait for the message to be published and return the result

# Usage
project_id = "analog-button-421413"
topic_name = "add-category"
publisher = PubSubPublisher(project_id, topic_name)

category_name = "Organic_chemistry"
publisher.publish_message(category_name)
print(f"Published '{category_name}'")
