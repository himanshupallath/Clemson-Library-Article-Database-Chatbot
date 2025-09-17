from flask import Flask, request, jsonify
import pandas as pd
import re

app = Flask(__name__)

# Load the data once
data = pd.read_csv('Clemson_Library_A_to_Z_database.csv')

def extract_keywords(query):
    # Use regular expressions to find keywords
    # This is a very simple heuristic: extract words following "on" or "about"
    match = re.search(r'\b(on|about)\b\s+(\w+)', query)
    if match:
        return [match.group(2)]
    else:
        return []

def search_articles(keywords):
    # Initialize an empty DataFrame to hold results
    results = pd.DataFrame()
    for keyword in keywords:
        filtered_data = data[data['database_name'].str.contains(keyword, case=False, na=False)]
        if not filtered_data.empty:
            results = pd.concat([results, filtered_data], ignore_index=True)
    results = results.drop_duplicates()
    return results[['database_name', 'database_url']].to_dict(orient='records')

@app.route('/gemini', methods=['POST'])
def gemini():
    content = request.json
    query = content['query']
    keywords = extract_keywords(query)
    results = search_articles(keywords)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    