#from htmlextract import html_extract
from backend.parsers.clean import html_clean
from backend.parsers.analyse import analyse_json
from asyncextract import html_extract

import time
start_time = time.time()

url = 'https://secretlab.sg/products/titan-evo-2022-series?sku=R22SW-CnC'
keywords = ['name', 'price', 'description']

html_content = html_extract(url)

print("--- extract time %s seconds ---\n" % (time.time() - start_time))
current_time = time.time()

'''
file_path = './data.txt'
with open(file_path, 'r') as file:
    html_content = file.read()'''
    
data = html_clean(html_content, keywords)
print("--- clean time %s seconds ---\n" % (time.time() - current_time))
current_time = time.time()

print(analyse_json(data))
print("--- analysis time %s seconds ---\n" % (time.time() - current_time))

print("--- %s seconds ---\n" % (time.time() - start_time))