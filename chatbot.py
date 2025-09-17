import pandas as pd
import streamlit as st
import requests
import os
import google.generativeai as genai
from dotenv import load_dotenv
from flask import Flask, request, jsonify

load_dotenv()

API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(
    api_key=API_KEY
)

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

app = Flask(__name__)

# Load the data once, assuming the CSV is formatted correctly and indexed for quick search
data = pd.read_csv('path_to_your_csv.csv')

def search_articles(query):
    # Simple case-insensitive filter searching in 'database_name'
    results = data[data['database_name'].str.contains(query, case=False, na=False)]
    if not results.empty:
        return results[['database_name', 'database_url']].to_dict(orient='records')
    return []

@app.route('/gemini', methods=['POST'])
def gemini():
    content = request.json
    query = content['query']
    results = search_articles(query)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)