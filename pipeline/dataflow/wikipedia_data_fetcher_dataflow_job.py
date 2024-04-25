import wikipediaapi
from google.cloud import storage, bigquery
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'pipeline/pubsub/analog-button-421413-6b359e87de4a.json'

class WikipediaDataFetcher:
    def __init__(self, user_agent, bucket_name, category_file, bigquery_dataset, bigquery_table, max_level=2, limit=2):
        self.wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent=user_agent)
        self.bucket_name = bucket_name
        self.category_file = category_file
        self.bigquery_dataset = bigquery_dataset
        self.bigquery_table = bigquery_table
        self.max_level = max_level
        self.limit = limit
        self.client = storage.Client()
        self.bqclient = bigquery.Client()

    def read_categories(self):
        bucket = self.client.get_bucket(self.bucket_name)
        blob = bucket.blob(self.category_file)
        data = blob.download_as_text()
        categories = data.split('\n')[2:]  # Skip the first line which is the header
        categories = [line for line in categories if line]  # Filter out any empty lines
        return categories

    def save_details_to_bigquery(self, categorymembers, current_category, level=0):
        count = 0
        rows_to_insert = []
        for c in categorymembers.values():
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
                print(f"Added details of '{c.title}' in category '{current_category}'")
                count += 1
            elif c.ns == wikipediaapi.Namespace.CATEGORY and level < self.max_level:
                count += self.save_details_to_bigquery(c.categorymembers, current_category, level=level + 1)
        
        if rows_to_insert:
            errors = self.bqclient.insert_rows_json(
                f"{self.bigquery_dataset}.{self.bigquery_table}", rows_to_insert
            )
            if errors:
                print(f"Encountered errors while inserting rows: {errors}")
        return count


    def run(self):
        categories = self.read_categories()
        total_saved = 0
        for cat in categories:
            print(f"Fetching category: {cat}")  # Log the formatted category name
            category_page = self.wiki_wiki.page(f"Category:{cat}")

            if not category_page.exists():
                print(f"Category does not exist: {cat}")
                continue

            category_members = category_page.categorymembers
            if not category_members:
                print(f"No category members found for: {cat}")
                continue

            total_saved += self.save_details_to_bigquery(category_members, cat)
            print(f"Total entries saved: {total_saved}")


user_agent = 'InformationRetrieval/1.0 (https://medium.com/@lakshmi_priya_ramisetty)'
if __name__ == '__main__':
    fetcher = WikipediaDataFetcher(
        user_agent=user_agent,
        bucket_name='ir-datastore',
        category_file='categories.csv',
        bigquery_dataset='WikiData',
        bigquery_table='WikiDataset'
    )
    fetcher.run()
