import pandas as pd
from newsapi import NewsApiClient
from newsapi.newsapi_exception import NewsAPIException

# Init
newsapi = NewsApiClient(api_key='85b72d2c9d864c9a8b4e345bb327f872')

try:
    # /v2/everything for Government Policies and Steel Industry in India
    all_articles = newsapi.get_everything(q='steel industry government policy India',
                                          domains='economictimes.indiatimes.com,business-standard.com,livemint.com,pib.gov.in,steel.gov.in',
                                          from_param='2024-09-08',  # Date range within 30 days
                                          to='2024-10-06',
                                          language='en',
                                          sort_by='relevancy',
                                          page=1)

    # Print the response to check if any articles were found
    print("All Articles Response:", all_articles)

except NewsAPIException as e:
    print(f"Error: {e}")

# Extract relevant fields from the response for both 'all_articles'
def extract_articles_data(response):
    articles = []
    if response['status'] == 'ok' and response['totalResults'] > 0:
        for article in response['articles']:
            articles.append({
                'source': article['source']['name'],
                'author': article['author'],
                'title': article['title'],
                'description': article['description'],
                'url': article['url'],
                'publishedAt': article['publishedAt'],
                'content': article['content']
            })
    else:
        print("No articles found in response.")
    return articles

# Organize data from all articles
all_articles_data = extract_articles_data(all_articles)

# Convert to a DataFrame
if all_articles_data:
    df = pd.DataFrame(all_articles_data)
    print("DataFrame Preview:", df.head())

    # Save the DataFrame to a CSV file
    df.to_csv('steel_industry_govt_policies_india.csv', index=False)
    print("Data saved to 'steel_industry_govt_policies_india.csv'.")
else:
    print("No articles found, CSV file will not be generated.")
