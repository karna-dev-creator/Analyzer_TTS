import requests
import os

NEWS_API_KEY = os.getenv("NEWS_API_KEY")  # Get API key from environment variables

def com_article(company_name, start_date=None, end_date=None):
    if not NEWS_API_KEY:
        print("❌ Error: NEWS_API_KEY is missing!")
        return []

    url = f"https://newsapi.org/v2/everything?q={company_name}&apiKey={NEWS_API_KEY}&language=en"

    if start_date:
        url += f"&from={start_date}"
    if end_date:
        url += f"&to={end_date}"

    print(f"🔍 Fetching NewsAPI: {url}")  # Log the request URL

    response = requests.get(url)

    if response.status_code != 200:
        print(f"❌ NewsAPI Error: {response.status_code} - {response.text}")
        return []

    data = response.json()

    if "articles" not in data or not data["articles"]:
        print("⚠️ No articles found from NewsAPI")
        return []

    print(f"✅ Articles Found: {len(data['articles'])}")
    return [
        {
            "title": item.get("title", "No title"),
            "summary": item.get("description", "No summary"),
            "link": item.get("url", "#"),
            "publishedAt": item.get("publishedAt", "Unknown"),
            "source": item["source"].get("name", "Unknown")
        }
        for item in data["articles"][:10]  # Get top 10 articles
    ]
