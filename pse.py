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
    all_urls = set()  # Set to hold all found URLs to avoid duplicates
    good_urls = []    # List to hold good URLs
    num_results_per_page = 10  # Change this to 10 for efficiency
    start_index = 1

    while len(good_urls) < 50:
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
            return good_urls  # Return what we have so far if there's an error

        # Extracting webpage URLs where images are found
        current_urls = [item['image']['contextLink'] for item in result.get('items', [])]

        # Filter and add to good_urls if not already seen and not in NA_urls
        for url in current_urls:
            if url not in all_urls and url not in NA_urls:
                all_urls.add(url)
                good_urls.append(url)
                if len(good_urls) >= 50:
                    break

        start_index += num_results_per_page  # Move to the next page of results

        if not current_urls:  # If no more results are found, break out of the loop
            break

    print("NO OF GOOD LINKS: " + str(len(good_urls)))
    print("NO OF BAD LINKS: " + str(len(all_urls) - len(good_urls)))

    return good_urls[:50]  # Return only the first 50 good URLs