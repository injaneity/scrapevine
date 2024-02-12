from htmlextract import html_extract
from htmlcleaner import html_clean
from htmlanalysis import analyse_json

import time
start_time = time.time()

url = 'https://secretlab.sg/products/titan-evo-2022-series?sku=R22SW-CnC'
keywords = ['name', 'price', 'description']

html_content = html_extract(url)

'''
file_path = './data.txt'
with open(file_path, 'r') as file:
    html_content = file.read()'''
    
data = html_clean(html_content, keywords)
print(analyse_json(data))

print("--- %s seconds ---\n" % (time.time() - start_time))