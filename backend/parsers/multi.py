from concurrent.futures import ProcessPoolExecutor, as_completed
import time
import os

# Assuming these are your custom functions
from backend.parsers.extract import html_extract
from backend.parsers.clean import html_clean
from backend.parsers.analyse import analyse_json

def process_url(url, keywords):
    html_content = html_extract(url)
    data = html_clean(html_content, keywords)
    analysis_result = analyse_json(data)
    return analysis_result

def main(urls, keywords):
    # Dynamically set the number of workers based on the number of URLs and available CPU cores
    num_workers = min(len(urls), os.cpu_count() or 1)
    
    results = []
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        future_to_url = {executor.submit(process_url, url, keywords): url for url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as exc:
                print(f'{url} generated an exception: {exc}')
    return results

# Ensure this part of your script is protected by a main guard
#        'https://www.sephora.sg/products/sephora-collection-colorful-blush/v/01-shame-on-you',
#         'https://mecha.store/collections/keycaps/products/glorious-gpbt-celestial-fire-premium-keycaps',
#         'https://www.yesstyle.com/en/malnia-home-lettering-canvas-belt/info.html/pid.1087460223',
#         'https://secretlab.sg/products/titan-evo-2022-series?sku=R22SW-CnC',

if __name__ == '__main__':
    start_time = time.time()
    urls = [
        'https://www.amazon.sg/Meiji-Fresh-Milk-2L-Chilled/dp/B071NH8N9V/ref=sr_1_2_f3_0o_fs?crid=3IKYWPKFW2U0I&keywords=milk&qid=1707756420&sprefix=mi%2Caps%2C386&sr=8-2',
        'https://www.sephora.sg/products/sephora-collection-colorful-blush/v/01-shame-on-you',
        'https://mecha.store/collections/keycaps/products/glorious-gpbt-celestial-fire-premium-keycaps',
        'https://www.yesstyle.com/en/malnia-home-lettering-canvas-belt/info.html/pid.1087460223',
        'https://secretlab.sg/products/titan-evo-2022-series?sku=R22SW-CnC',
        # Add more URLs as needed
        ]
    keywords = ['name', 'price', 'description']
    results = main(urls, keywords)
    for result in results:
        print(result)
    print(f"--- Overall time {time.time() - start_time} seconds ---\n")


