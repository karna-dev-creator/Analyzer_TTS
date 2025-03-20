from flask import Flask, request, jsonify
from news_scraper import com_article
from sentiment_analysis import ana_sentiment
from text_to_speech import hindi_trans
from rake_nltk import Rake
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# home route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "api is working!"})

# extract keywords from news articles
def extract_keywords(text):
    rake = Rake()
    rake.extract_keywords_from_text(text)
    return rake.get_ranked_phrases()[:5]

#  get news articles with keywords and sentiment analysis
@app.route("/fetch_news_data", methods=["GET"])
def get_news():
    company_name = request.args.get("company")
    start_date = request.args.get("start_date") 
    end_date = request.args.get("end_date")

    if not company_name:
        return jsonify({"error": "Company name is required"}), 400

    articles = com_article(company_name, start_date, end_date)
    if not articles:
        return jsonify({"error": "No articles found"}), 404

    sentiment_count = {"Positive": 0, "Negative": 0, "Neutral": 0}

    for article in articles:
        article["sentiment"] = ana_sentiment(article["title"])
        article["keywords"] = extract_keywords(article["title"])
        sentiment_count[article["sentiment"]] += 1

    return jsonify({
        "company": company_name,
        "articles": articles,
        "sentiment_distribution": sentiment_count
    })

# text-to-speech in hindi
@app.route("/text_2_speech", methods=["POST"])
def generate_tts():
    data = request.json
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "Text is required"}), 400

    filename = hindi_trans(text)
    return jsonify({"audio_file": filename})

if __name__ == "__main__":
    print("🚀 Flask API is starting on Render...")
    app.run(host="0.0.0.0", port=10000, debug=True)
