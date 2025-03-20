import requests
import os

API_KEY = os.getenv("GNEWS_API_KEY")  # Load API key from environment variables

def com_article(company_name, start_date=None, end_date=None):
    if not API_KEY:
        print("❌ Error: API key not found.")
        return []

    url = f"https://gnews.io/api/v4/search?q={company_name}&apikey={API_KEY}&lang=en"

    print(f"🔍 Fetching articles from: {url}")  # Debugging line

    response = requests.get(url)

    print(f"🔎 API Status Code: {response.status_code}")  # Debugging line
    print(f"📜 API Response: {response.text}")  # Debugging line

    if response.status_code != 200:
        print("❌ API Error:", response.text)
        return []

    data = response.json()

    if "articles" not in data or not data["articles"]:
        print("❌ No articles found in API response.")  # Debugging line
        return []

    articles = []
    for item in data["articles"][:10]:  # Get top 10 articles
        articles.append({
            "title": item.get("title", "No title available"),
            "summary": item.get("description", "No summary available"),
            "link": item.get("url", "#"),
            "publishedAt": item.get("publishedAt", "Unknown date"),
            "source": item["source"].get("name", "Unknown source")
        })

    print(f"✅ Articles fetched successfully: {len(articles)} articles found.")  # Debugging line
    return articles
