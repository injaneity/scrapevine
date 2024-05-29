import requests
import os
from dotenv import load_dotenv
load_dotenv()



NA_urls = [
    "https://www.lovebonito.com/sg/faq",
    "https://www.lovebonito.com/sg/global/wardrobe-staples-feb",
    "https://www.lovebonito.com/sg/terms-and-conditions",
    "https://www.lovebonito.com/sg/global/festive-gift-guide-draft",
    "https://www.lovebonito.com/sg/welcome-home-lbcommunity",
    "https://www.lovebonito.com/sg/general-size-charts"
]



def product_search(tags, link):
    search_url = "https://www.googleapis.com/customsearch/v1"
    all_urls = []  # List to hold all found URLs
    num_results_per_page = 5
    for page_num in range(0, 14):
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
            print(f"ERROR {response.status_code}: {response.reason}")
            return ""

        # Extracting webpage URLs where images are found
        all_urls.extend([item['image']['contextLink'] for item in result.get('items', [])])

    # Identifying duplicates
    bad_urls = []
    good_urls = []
    for url in all_urls:
        if url in good_urls or url in NA_urls:
            bad_urls.append(url)
        else:
            good_urls.append(url)

    print("NO OF BAD LINKS: " + str(len(bad_urls)))
    print("NO OF GOOD LINKS: " + str(len(good_urls)))

    # Trim good_urls if necessary
    if len(good_urls) > 50:
        good_urls = good_urls[:50]

    return good_urls

