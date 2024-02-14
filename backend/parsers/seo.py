import requests
import os
from dotenv import load_dotenv
load_dotenv()

import time
start = time.time()

def google_site_search(query, site, api_key, cse_id, total_results=80):
    """
    Perform a Google site-restricted search and return URLs of web pages.
    
    :param query: The search query.
    :param site: The site to restrict the search to.
    :param api_key: The API key for Google Custom Search JSON API.
    :param cse_id: The Custom Search Engine ID.
    :param total_results: The total number of results to retrieve.
    :return: A list of URLs from the search results.
    """
    search_url = "https://www.googleapis.com/customsearch/v1"
    webpage_urls = []
    for start_index in range(1, total_results, 10):
        params = {
            'q': f"{query} site:{site}",
            'cx': cse_id,
            'key': api_key,
            'start': start_index,
            'num': min(10, total_results - len(webpage_urls))  # Adjust number of results per request
        }
        response = requests.get(search_url, params=params)
        if response.status_code == 200:
            result = response.json()
            # Extracting webpage URLs from the search results
            if 'items' in result:
                webpage_urls.extend([item['link'] for item in result['items']])
            # Check if there are no more results or we have reached the requested total
            if 'nextPage' not in result.get('queries', {}) or len(webpage_urls) >= total_results:
                break
        else:
            print(f"Error {response.status_code}: {response.json().get('error', {}).get('message', 'Unknown Issue')}")
            break

    return webpage_urls

# Example usage
api_key = os.getenv('PSE_API')
cse_id = os.getenv('PSE_ID')
query = "fashion"
site = 'charleskeith.com'  # Specify the site for the search
webpage_results = google_site_search(query, site, api_key, cse_id)

for url in webpage_results:
    print(url)

print(len(webpage_results))

print(f"--- {time.time() - start} seconds ---")
