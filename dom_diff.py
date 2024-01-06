# Import necessary libraries
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
import json

# Initialize Flask app
app = Flask(__name__)

# Perplexity API key
perplexity_api_key = "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"

# Perplexity API endpoint
perplexity_api_url = "https://api.perplexity.ai/chat/completions"

# Function to get DOM from a URL
def get_dom(url):
    response = requests.get(url)
    return response.text

# Function to compare two DOMs and generate natural language description using Perplexity
def compare_and_describe(before_dom, after_dom):
    # Parse HTML DOMs
    before_soup = BeautifulSoup(before_dom, 'html.parser')
    after_soup = BeautifulSoup(after_dom, 'html.parser')

    # Compare DOMs and identify changes
    # TODO: Implement a more sophisticated DOM comparison logic here

    # For now, let's assume some sample changes
    changes = [
        "Sidebar is present in the second DOM.",
        "Close button is available in the second DOM.",
        "Menu options are available in the second DOM."
    ]

    # Generate natural language description
    description = "\n".join(changes)

    # Use Perplexity to enhance the description
    perplexity_payload = {
        "model": "mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "Be precise and concise."},
            {"role": "user", "content": description}
        ]
    }

    perplexity_headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {perplexity_api_key}"
    }

    perplexity_response = requests.post(perplexity_api_url, json=perplexity_payload, headers=perplexity_headers)

    if perplexity_response.status_code == 200:
        perplexity_result = perplexity_response.json()
        enhanced_description = perplexity_result.get('choices', [{}])[0].get('message', description)
        return enhanced_description
    else:
        # If Perplexity request fails, return the original description
        return description

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling form submission
@app.route('/compare', methods=['POST'])
def compare():
    # Get URLs from the form
    before_url = request.form['before_url']
    after_url = request.form['after_url']

    # Get DOMs from the URLs
    before_dom = get_dom(before_url)
    after_dom = get_dom(after_url)

    # Compare DOMs and generate enhanced description using Perplexity
    description = compare_and_describe(before_dom, after_dom)

    return render_template('result.html', description=description)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
