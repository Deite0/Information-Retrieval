import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions, SetupOptions
from apache_beam.options.value_provider import ValueProvider
from apache_beam.io import ReadFromText
from apache_beam.io.gcp.bigquery import WriteToBigQuery
import wikipediaapi
import os

class TemplateOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_value_provider_argument('--user_agent', type=str, help='User agent for Wikipedia API')
        parser.add_value_provider_argument('--categories_bucket', type=str, help='Google Cloud Storage bucket for categories')
        parser.add_value_provider_argument('--category_file', type=str, help='File name for categories in GCS bucket')
        parser.add_value_provider_argument('--bigquery_dataset', type=str, help='BigQuery dataset name')
        parser.add_value_provider_argument('--bigquery_table', type=str, help='BigQuery table name')

class FetchWikipediaData(beam.DoFn):
    def __init__(self, user_agent, max_level, limit):
        self.user_agent = user_agent.get()
        self.max_level = max_level
        self.limit = limit
        self.wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent=self.user_agent)

    def process(self, element, level=0):
        category, _ = element
        category_page = self.wiki_wiki.page(f"Category:{category}")
        if not category_page.exists():
            return
        
        rows_to_insert = self.save_details_to_bigquery(category_page.categorymembers, category)
        for row in rows_to_insert:
            yield row

    def save_details_to_bigquery(self, category_page, current_category, level=0):
        rows_to_insert = []
        count = 0
        for c in category_page.values():
            if count >= self.limit:
                break
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
        return rows_to_insert

def run(argv=None):
    pipeline_options = PipelineOptions(argv)
    custom_options = pipeline_options.view_as(TemplateOptions)
    google_cloud_options = pipeline_options.view_as(GoogleCloudOptions)
    google_cloud_options.project = 'analog-button-421413'
    google_cloud_options.job_name = 'wikipedia-data-fetcher'
    google_cloud_options.staging_location = 'gs://ir-dataflow/staging'
    google_cloud_options.temp_location = 'gs://ir-dataflow/tmp'
    google_cloud_options.region = 'us-east1'
    pipeline_options.view_as(SetupOptions).save_main_session = True

    with beam.Pipeline(options=pipeline_options) as p:
        categories = (p 
                      | 'Read Categories' >> ReadFromText(f'gs://{custom_options.categories_bucket.get()}/{custom_options.category_file.get()}')
                      | 'Skip Header' >> beam.Filter(lambda x: not x.startswith('Category'))
                      | 'Initial Category Setup' >> beam.Map(lambda x: (x, 0)))

        wikipedia_data = (categories 
                          | 'Fetch Data' >> beam.ParDo(FetchWikipediaData(custom_options.user_agent, max_level=2, limit=2)))

        wikipedia_data | 'Write to BigQuery' >> WriteToBigQuery(
            table=f'{google_cloud_options.project}:{custom_options.bigquery_dataset.get()}.{custom_options.bigquery_table.get()}',
            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
            method="STREAMING_INSERTS"
        )

if __name__ == '__main__':
    import sys
    # run()
    run([
        '--user_agent=InformationRetrieval/1.0',
        '--categories_bucket=ir-datastore',  
        '--category_file=unprocessed_categories.csv',
        '--bigquery_dataset=WikiData',  
        '--bigquery_table=test',  
        '--runner=DataflowRunner',  
        '--project=analog-button-421413',
        '--region=us-east1',
        '--temp_location=/tmp',  
        '--staging_location=/tmp',  
        '--setup_file=pipeline/dataflow/setup.py'
    ])
