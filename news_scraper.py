import requests

NEWS_API_KEY = "69831002870340c5a08ce259c555f639" 

def com_article(company_name, start_date=None, end_date=None):
    url = f"https://newsapi.org/v2/everything?q={company_name}&apiKey={NEWS_API_KEY}"

    #  add date filters only if provided
    if start_date:
        url += f"&from={start_date}"
    if end_date:
        url += f"&to={end_date}"

    # set language filter
    url += "&language=en"

    response = requests.get(url)
    if response.status_code != 200:
        print("Error fetching news:", response.text) 
        return []

    data = response.json()

    if "articles" not in data or not data["articles"]:
        return []  # eeturn empty list if no articles are found

    articles = []

    for item in data["articles"][:10]:  # get top 10 articles
        articles.append({
            "title": item.get("title", "No title available"),
            "summary": item.get("description", "No summary available"),
            "link": item.get("url", "#"),
            "publishedAt": item.get("publishedAt", "Unknown date"),
            "source": item["source"].get("name", "Unknown source")
        })

    return articles
