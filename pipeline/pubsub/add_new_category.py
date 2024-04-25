from google.cloud import pubsub_v1
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS']='pipeline/pubsub/analog-button-421413-6b359e87de4a.json'

publisher = pubsub_v1.PublisherClient()

project_id = "analog-button-421413"
topic_name = "add-category"

topic_path = publisher.topic_path(project_id, topic_name)

data = u'{"category_name":"Data science "}'

# Data must be a bytestring
data = data.encode("utf-8")

future = publisher.publish(topic_path, data=data)
print(future.result())

print("Published messages.")