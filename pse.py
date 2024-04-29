import requests
import os
from dotenv import load_dotenv
load_dotenv()

def product_search(tags, link):
    search_url = "https://www.googleapis.com/customsearch/v1"
    all_webpage_urls = []  # List to hold all found URLs, including duplicates
    unique_webpage_urls = []  # List to hold unique URLs
    num_results_per_page = 5
    for page_num in range(0, 1):
        start_index = (page_num * num_results_per_page) + 1
        params = {
            'q': f"{tags} site:{link}",
            'cx': os.getenv("PSE_ID"),
            'searchType': 'image',
            'key': os.getenv("PSE_API"),
            'start': start_index,
            'num': num_results_per_page
        }
        response = requests.get(search_url, params=params)
        if response.status_code == 200:
            result = response.json()
        else:
            print(f"Error {response.status_code}: {response.reason}")
            return ""

        # Extracting webpage URLs where images are found
        all_webpage_urls.extend([item['image']['contextLink'] for item in result.get('items', [])])

    # Identifying duplicates
    duplicates = []
    for url in all_webpage_urls:
        if url in unique_webpage_urls:
            duplicates.append(url)
        else:
            unique_webpage_urls.append(url)

    # Printing out duplicates and total count of duplicates removed
    print("DUPLICATE LINKS:\n" + str(duplicates))
    print("NO OF DUPLICATE: " + str(len(duplicates)))
    
    print("UNIQUE LINKS:\n" + str(unique_webpage_urls))
    print("NO OF UNIQUE: " + str(len(unique_webpage_urls)))

    return unique_webpage_urls