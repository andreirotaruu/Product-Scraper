from flask import Flask, jsonify, request, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['GET'])
def scrape_website():  # just used to grab title and info so far, going to add more soon to grab price/ name of product. 
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.title.string if soup.title else 'No title found'
        headings = [h.text.strip() for h in soup.find_all(['h1', 'h2', 'h3'])]

        return jsonify({
            'url': url,
            'title': title,
            'headings': headings[:10]
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
