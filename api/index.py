import os
import requests
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

# Set Gemini API key from environment variable for security
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

WIKI_API_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/"
WIKI_RANDOM_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"

app = Flask(__name__, static_folder="../static", static_url_path="")
CORS(app)

@app.route("/")
def root():
    return app.send_static_file("index.html")

@app.route('/api/search', methods=['GET'])
def search_article():
    query = request.args.get('query', '')
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    resp = requests.get(WIKI_API_URL + requests.utils.quote(query))
    if resp.status_code != 200:
        return jsonify({'error': 'Article not found'}), 404
    data = resp.json()
    title = data.get('title', '')
    extract = data.get('extract', '')
    if not extract:
        return jsonify({'error': 'No summary found'}), 404
    # Send to Gemini for brainrot summary
    summary = brainrot_summarize(title, extract)
    return jsonify({'title': title, 'summary': summary})

@app.route('/api/random', methods=['GET'])
def random_article():
    resp = requests.get(WIKI_RANDOM_URL)
    if resp.status_code != 200:
        return jsonify({'error': 'Random article not found'}), 404
    data = resp.json()
    title = data.get('title', '')
    extract = data.get('extract', '')
    if not extract:
        return jsonify({'error': 'No summary found'}), 404
    summary = brainrot_summarize(title, extract)
    return jsonify({'title': title, 'summary': summary})

@app.route('/api/summarize', methods=['POST'])
def summarize_article():
    data = request.get_json()
    title = data.get('title', '')
    extract = data.get('extract', '')
    if not extract:
        return jsonify({'error': 'No content to summarize'}), 400
    summary = brainrot_summarize(title, extract)
    return jsonify({'summary': summary})

def brainrot_summarize(title, text):
    prompt = f"Rewrite the following Wikipedia article summary in gen-z brainrot internet lingo, but keep the main facts and be educational and pedagogical. Do not preface, just get to the summary.Use a lot of dark humour and brainrot emojis.\n\nTitle: {title}\nSummary: {text}"
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"[Gemini error: {e}]"

if __name__ == '__main__':
    app.run(debug=True) 
