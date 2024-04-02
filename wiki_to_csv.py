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

def save_details_to_csv(categorymembers, csv_writer, current_category, level=0, max_level=2, limit=50):
    count = 0
    for c in categorymembers.values():
        if count >= limit:
            break
        if c.ns == wikipediaapi.Namespace.MAIN:
            page = wiki_wiki.page(c.title)
            # Writing category as the first column
            csv_writer.writerow([current_category, c.title, page.summary, page.text, page.pageid, page.fullurl])
            print(f"Added details of '{c.title}' in category '{current_category}'")
            count += 1
        elif c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
            count += save_details_to_csv(c.categorymembers, csv_writer, current_category, level=level + 1, max_level=max_level, limit=limit - count)
    return count

# Ensure the output directory exists
output_dir = 'wikipedia_details'
os.makedirs(output_dir, exist_ok=True)

# CSV file to store the details
csv_filename = os.path.join(output_dir, '/Users/laasya/Desktop/GitHub/Computer-Science---Information-Retrieval/WikiData.csv')

categories = [
    "Data_science", 
    "Machine_learning", 
    "Data_mining", 
    "Artificial_neural_networks", 
    "Big_data", 
    "Statistical_classification", 
    "Clustering_algorithms", 
    "Regression_analysis",
    "Data_visualization",
    "Business_intelligence",
    "Predictive_analytics",
    "Time_series_analysis",
    "Natural_language_processing",
    "Deep_learning",
    "Data_cleaning",
    "Data_transformation",
    "Dimensionality_reduction",
    "Feature_engineering",
    "Neural_networks",
    "Decision_trees",
    "Ensemble_learning",
    "Computer_vision", 
    "Pattern_recognition", 
    "Reinforcement_learning", 
    "Supervised_learning", 
    "Unsupervised_learning",
    "Algorithms", 
    "Data_structures"
    # Add or remove categories as needed
]

# Write to CSV
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    csv_writer = csv.writer(file)
    # Writing headers with Category as the first column
    csv_writer.writerow(['Category', 'Topic', 'Summary', 'Full Content', 'Page ID', 'URL'])

    total_saved = 0
    for cat in categories:
        category_page = wiki_wiki.page(f"Category:{cat}")
        total_saved += save_details_to_csv(category_page.categorymembers, csv_writer, cat)

print(f"Total pages saved: {total_saved}")
