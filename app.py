from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/latest-news")
def latest_news():
    url = "https://news.google.com/rss"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "xml")
        items = soup.find_all("item")[:10]
        
        news = []
        for item in items:
            enclosure = item.find("media:thumbnail") or item.find("enclosure")
            thumb_url = enclosure.get("url") if enclosure else None
            news.append({
                "title": item.title.text,
                "link": item.link.text,
                "enclosure": thumb_url
            })
        return jsonify(news)
    except:
        return jsonify([{"title": "News loading...", "link": "#", "enclosure": None}] * 10)

if __name__ == "__main__":
    app.run()
