import wikipediaapi
import csv
import os

# Define a user agent
user_agent = 'LakshmiPriyaRamisetty/1.0 (https://medium.com/@lakshmi_priya_ramisetty)'

# Create a Wikipedia object with the specified user agent
wiki_wiki = wikipediaapi.Wikipedia(
    language='en', 
    user_agent=user_agent
)

def save_details_to_csv(categorymembers, csv_writer, level=0, max_level=2, limit=100):
    count = 0
    for c in categorymembers.values():
        if count >= limit:
            break
        if c.ns == wikipediaapi.Namespace.MAIN:
            page = wiki_wiki.page(c.title)
            csv_writer.writerow([c.title, page.summary, page.text, page.pageid, page.fullurl])
            print(f"Added details of '{c.title}'")
            count += 1
        elif c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
            count += save_details_to_csv(c.categorymembers, csv_writer, level=level + 1, max_level=max_level, limit=limit - count)
    return count

# Ensure the output directory exists
output_dir = 'wikipedia_details'
os.makedirs(output_dir, exist_ok=True)

# CSV file to store the details
csv_filename = os.path.join(output_dir, '/Users/laasya/Desktop/GitHub/Computer-Science---Information-Retrieval/computer_science_wiki.csv')

# List of computer science related categories to start from
categories = ["Computer_science", "Programming_languages", "Algorithms", "Data_structures"]

# Write to CSV
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['Topic', 'Summary', 'Full Content', 'Page ID', 'URL'])

    total_saved = 0
    for cat in categories:
        category_page = wiki_wiki.page(f"Category:{cat}")
        total_saved += save_details_to_csv(category_page.categorymembers, csv_writer)

print(f"Total pages saved: {total_saved}")
