from concurrent.futures import ProcessPoolExecutor, as_completed
import time
import os

# Assuming these are your custom functions
from seo import product_search
from extract import html_extract
from clean import html_clean
from analyse import analyse_json

def process_url(url, keywords):
    html_content = html_extract(url)
    data = html_clean(html_content, keywords)
    analysis_result = analyse_json(data)
    return analysis_result

def main(url, tags, keywords):
    urls = product_search(tags, url)
    # Dynamically set the number of workers based on the number of URLs and available CPU cores
    num_workers = min(len(urls), os.cpu_count() or 1)
    
    results = []
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_url = {executor.submit(process_url, url, keywords): url for url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as exc:
                print(f'{url} generated an exception: {exc}')
    return results

# if __name__ == '__main__':
#     start_time = time.time()
#     url = "amazon.sg"
#     tags = ["coat", "red"]
#     keywords = ["material", "colour"]
#     results = main(url, tags, keywords)
#     for result in results:
#         print(result)
#     print(f"--- Overall time {time.time() - start_time} seconds ---\n")


