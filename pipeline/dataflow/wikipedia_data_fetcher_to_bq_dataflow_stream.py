import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io import ReadFromPubSub
from apache_beam.io.gcp.bigquery import WriteToBigQuery
import wikipediaapi
import json
import base64
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'pipeline/pubsub/analog-button-421413-6b359e87de4a.json'

class FetchWikipediaData(beam.DoFn):
    def __init__(self, user_agent, max_level, limit):
        self.user_agent = user_agent
        self.max_level = max_level
        self.limit = limit
        self.wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent=self.user_agent)

    def process(self, element, level=0):
        category = element.decode('utf-8')
        category = json.loads(category)
        category = category["category_name"]
        print("Category Name:", category)
        category_page = self.wiki_wiki.page(f"Category:{category}")
        if not category_page.exists():
            print(f"Category does not exist: {category}")
            return
        
        # Fetch and yield the data rows directly from this method
        rows_to_insert = self.save_details_to_bigquery(category_page.categorymembers, category)
        # print(rows_to_insert)

        print(f"Adding rows for category {category}")
        for row in rows_to_insert:
            yield row

    def save_details_to_bigquery(self, category_page, current_category, level=0):
        rows_to_insert = []
        count = 0
        for c in category_page.values():
            if count >= self.limit:
                break
            try:
                if c.ns == wikipediaapi.Namespace.MAIN:
                    page = self.wiki_wiki.page(c.title)
                    row = {
                        "Category": current_category,
                        "Topic": c.title,
                        "Summary": page.summary,
                        "Full_Content": page.text,
                        "Page_ID": page.pageid,
                        "URL": page.fullurl
                    }
                    rows_to_insert.append(row)
                    count += 1
                elif c.ns == wikipediaapi.Namespace.CATEGORY and level < self.max_level:
                    subcategory_rows = self.save_details_to_bigquery(c.categorymembers, current_category, level=level + 1)
                    rows_to_insert.extend(subcategory_rows)
            except Exception as e:
                print(f"Failed to fetch page {c.title}: {str(e)}. Skipping...")
        return rows_to_insert

def run():
    project_id = 'analog-button-421413'
    topic_name = "test-topic-sub"
    subscription = f'projects/{project_id}/subscriptions/{topic_name}'
    bigquery_dataset = 'WikiData'
    bigquery_table = 'test'
    
    options = PipelineOptions(
        runner='DirectRunner',
        # runner='DataflowRunner',
        project=project_id,
        region='us-central1',
        job_name='wikipedia-data-fetch',
        streaming=True
    )

    with beam.Pipeline(options=options) as p:
        wikipedia_data = (p
                          | 'Read from Pub/Sub' >> ReadFromPubSub(subscription=subscription)
                          | 'Fetch Data' >> beam.ParDo(FetchWikipediaData(user_agent='Your User Agent', max_level=2, limit=2))
                         )

        # Writing to BigQuery
        wikipedia_data | 'Write to BigQuery' >> WriteToBigQuery(
            table=f'{project_id}:{bigquery_dataset}.{bigquery_table}',
            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
            method="STREAMING_INSERTS"
        )

if __name__ == '__main__':
    run()
