import requests

NEWS_API_KEY = "69831002870340c5a08ce259c555f639"

def com_article(company_name, start_date=None, end_date=None):
    """
    Fetches the latest news articles related to a company using NewsAPI.
    
    Parameters:
        company_name (str): The company name or keyword to search for.
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.
    
    Returns:
        list: A list of dictionaries containing news article details.
    """
    # Base API URL
    url = f"https://newsapi.org/v2/everything?q={company_name}&apiKey={NEWS_API_KEY}"

    # Add date filters if provided
    if start_date:
        url += f"&from={start_date}"
    if end_date:
        url += f"&to={end_date}"

    # Set language filter and sorting method
    url += "&language=en&sortBy=publishedAt"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad HTTP responses (4xx, 5xx)

        data = response.json()

        # Check if articles exist
        if "articles" not in data or not data["articles"]:
            print("No articles found.")
            return []

        articles = []

        # Get top 10 articles
        for item in data["articles"][:10]:
            articles.append({
                "title": item.get("title", "No title available"),
                "summary": item.get("description", "No summary available"),
                "link": item.get("url", "#"),
                "publishedAt": item.get("publishedAt", "Unknown date"),
                "source": item["source"].get("name", "Unknown source")
            })

        return articles

    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []
