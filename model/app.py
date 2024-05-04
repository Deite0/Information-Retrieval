from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
import joblib
import re
import nltk
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
nltk.download('stopwords')

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Welcome to the API! Use /query?q=your_query to search."

def preprocess(text):
    # Ensure text is a string
    if not isinstance(text, str):
        return ""

    # Simple preprocessing: lowercasing and removing non-alphabetic characters
    text = re.sub(r'\W+', ' ', text.lower())
    tokens = word_tokenize(text)
    return ' '.join([token for token in tokens if token not in stopwords.words('english')])

# Load the saved model and matrix
vectorizer = joblib.load('tfidf_vectorizer.joblib')
tfidf_matrix = joblib.load('tfidf_matrix.joblib')
df = pd.read_csv('pipeline/dataflow/WikiData.csv')  # Ensure the DataFrame is available for lookup

def find_relevant_content(query, threshold=0.1):
    processed_query = preprocess(query)  
    query_vector = vectorizer.transform([processed_query])
    similarity = cosine_similarity(query_vector, tfidf_matrix)
    max_similarity = max(similarity[0])
    
    if max_similarity < threshold:
        return "Sorry, I don't have information on that topic."
    
    index = similarity.argmax()
    return df.iloc[index]['Summary']

@app.route('/query', methods=['GET'])
def answer_query():
    user_input = request.args.get('q', '')
    response = find_relevant_content(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
