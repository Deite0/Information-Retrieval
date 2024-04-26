import wikipediaapi
import csv
import os

class WikipediaDataFetcher:
    def __init__(self, user_agent, category_file, output_file, max_level=2, limit=10000):
        self.wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent=user_agent)
        self.category_file = category_file
        self.output_file = output_file
        self.max_level = max_level
        self.limit = limit

    def read_categories(self):
        categories = []
        with open(self.category_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip the header
            for row in reader:
                categories.append(row[0])
        return categories

    def save_details_to_csv(self, categorymembers, csv_writer, current_category, level=0):
        count = 0
        for c in categorymembers.values():
            if count >= self.limit:
                break
            if c.ns == wikipediaapi.Namespace.MAIN:
                page = self.wiki_wiki.page(c.title)
                csv_writer.writerow([current_category, c.title, page.summary, page.text, page.pageid, page.fullurl])
                print(f"Added details of '{c.title}' in category '{current_category}'")
                count += 1
            elif c.ns == wikipediaapi.Namespace.CATEGORY and level < self.max_level:
                count += self.save_details_to_csv(c.categorymembers, csv_writer, current_category, level=level + 1)
        return count

    def run(self):
        categories = self.read_categories()

        file_exists = os.path.isfile(self.output_file)

        with open(self.output_file, mode='a', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            if not file_exists:
                csv_writer.writerow(['Category', 'Topic', 'Summary', 'Full Content', 'Page ID', 'URL'])

            total_saved = 0
            for cat in categories:
                category_page = self.wiki_wiki.page(f"Category:{cat}")
                total_saved += self.save_details_to_csv(category_page.categorymembers, csv_writer, cat)

            print(f"Total pages saved: {total_saved}")

# Usage
user_agent = 'LakshmiPriyaRamisetty/1.0 (https://medium.com/@lakshmi_priya_ramisetty)'
fetcher = WikipediaDataFetcher(
    user_agent=user_agent,
    category_file='pipeline/dataflow/categories.csv',
    output_file='pipeline/dataflow/WikiData2.csv'
)
fetcher.run()
