from flask import Flask, request, jsonify, send_from_directory
from news_scraper import com_article
from sentiment_analysis import ana_sentiment
from text_to_speech import hindi_trans
from rake_nltk import Rake
import nltk
import traceback
import os

# Ensure NLTK stopwords are downloaded
nltk.download("stopwords")

app = Flask(__name__)

# Define directory to store audio files
AUDIO_FOLDER = "audio"
os.makedirs(AUDIO_FOLDER, exist_ok=True)

@app.route("/", methods=["GET"])
def home():
    """ Home route to check API status """
    return jsonify({"message": "API is working!"})

def extract_keywords(text):
    """ Extract keywords from a given text using RAKE algorithm. """
    try:
        rake = Rake()
        rake.extract_keywords_from_text(text)
        return rake.get_ranked_phrases()[:5]
    except Exception as e:
        print("❌ ERROR extracting keywords:", str(e))
        traceback.print_exc()
        return []

@app.route("/fetch_news_data", methods=["GET"])
def get_news():
    """ Fetch news articles, analyze sentiment, and extract keywords. """
    company_name = request.args.get("company")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if not company_name:
        return jsonify({"error": "Company name is required"}), 400

    try:
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

    except Exception as e:
        print("❌ ERROR in /fetch_news_data:", str(e))
        traceback.print_exc()
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

@app.route("/text_2_speech", methods=["POST"])
def generate_tts():
    """ Convert text to Hindi speech and return the generated audio file URL. """
    data = request.json
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "Text is required"}), 400

    try:
        filename = hindi_trans(text)  # Generates a unique filename
        return jsonify({"audio_file": f"/audio/{filename}"})  # Return correct path
    except Exception as e:
        print("❌ ERROR in /text_2_speech:", str(e))
        traceback.print_exc()
        return jsonify({"error": "Text-to-Speech Error", "details": str(e)}), 500

@app.route("/audio/<filename>")
def serve_audio(filename):
    """ Serve generated audio files. """
    return send_from_directory(AUDIO_FOLDER, filename)

if __name__ == "__main__":
    print("🚀 Flask API is starting on port 10000...")
    app.run(host="0.0.0.0", port=10000, debug=True)

