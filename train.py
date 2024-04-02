import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download NLTK stopwords
nltk.download('punkt')
nltk.download('stopwords')

# Load data
df = pd.read_csv('/Users/laasya/Desktop/GitHub/Computer-Science---Information-Retrieval/WikiData.csv')

# Preprocessing
stop_words = set(stopwords.words('english'))

import re

def preprocess(text):
    # Remove LaTeX-like or MathML expressions
    # Targeting patterns like {\displaystyle ...} and \mu -like LaTeX commands
    clean_text = re.sub(r'\{\\displaystyle [^\}]+\}', '', text)
    clean_text = re.sub(r'\\[a-zA-Z]+\{[^}]*\}', '', clean_text)
    clean_text = re.sub(r'\\[a-zA-Z]+', '', clean_text)

    word_tokens = word_tokenize(clean_text.lower())
    filtered_text = [word for word in word_tokens if word not in stop_words and word.isalpha()]
    return " ".join(filtered_text)

df['processed_summary'] = df['Summary'].apply(preprocess)


df['processed_summary'] = df['Summary'].apply(preprocess)

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['processed_summary'])

# def retrieve_info(query):
#     processed_query = preprocess(query)
#     query_vec = vectorizer.transform([processed_query])
#     similarity = cosine_similarity(query_vec, tfidf_matrix)
    
#     # Get the index of the most similar summary
#     idx = similarity.argmax()

#     return df.iloc[idx]['Topic'], df.iloc[idx]['Summary']
def clean_summary(summary):
    # Remove complex LaTeX/MathML expressions
    summary = re.sub(r'\{\\displaystyle [^\}]+\}', '', summary)
    summary = re.sub(r'\{[^}]*\}', '', summary)
    summary = re.sub(r'\\[a-zA-Z]+\{[^}]*\}', '', summary)
    summary = re.sub(r'\\[a-zA-Z]+', '', summary)
    return summary

def retrieve_info(query):
    processed_query = preprocess(query)
    query_vec = vectorizer.transform([processed_query])
    similarity = cosine_similarity(query_vec, tfidf_matrix)
    
    # Get the index of the most similar summary
    idx = similarity.argmax()
    topic = df.iloc[idx]['Topic']
    summary = clean_summary(df.iloc[idx]['Summary'])

    return topic, summary

# Example usage
topic, summary = retrieve_info("What is AVL Tree?")
print(f"Topic: {topic}\nSummary: {summary}")

while True:
    user_input = input("Ask me something about computer science: ")
    if user_input.lower() == 'quit':
        break
    topic, summary = retrieve_info(user_input)
    print(f"Topic: {topic}\nSummary: {summary}\n")
