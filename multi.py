# Assuming these are your custom functions
from extract import extract_html
from clean import clean_html
from analyse import analyse_html

def process_url(url, keywords):
    html_content = extract_html(url)
    if html_content:
        data = clean_html(html_content, keywords)
        analysis = analyse_html(data, keywords)
        return analysis
    return None

# from concurrent.futures import ThreadPoolExecutor, as_completed
# import os
# from seo import product_search
# def main(url, tags, keywords):
#     urls = product_search(tags, url)
#     # Dynamically set the number of workers based on the number of URLs and available CPU cores
#     num_workers = min(len(urls), os.cpu_count() or 1)
    
#     results = []
#     with ThreadPoolExecutor(max_workers=num_workers) as executor:
#         future_to_url = {executor.submit(process_url, url, keywords): url for url in urls}
#         for future in as_completed(future_to_url):
#             url = future_to_url[future]
#             try:
#                 result = future.result()
#                 results.append(result)
#             except Exception as exc:
#                 print(f'{url} generated an exception: {exc}')
#     return results

# import time
# if __name__ == '__main__':
#     start_time = time.time()
#     url = "amazon.sg"
#     tags = ["coat", "red"]
#     keywords = ["material", "colour"]
#     results = main(url, tags, keywords)
#     for result in results:
#         print(result)
#     print(f"--- Overall time {time.time() - start_time} seconds ---\n")


