#from htmlextract import html_extract
from clean import html_clean
from analyse import analyse_json
from backend.parsers.archive.asyncextract import html_extract

import time
start_time = time.time()

url = 'https://secretlab.sg/products/titan-evo-2022-series?sku=R22SW-CnC'
keywords = ['name', 'price', 'description']

html_content = html_extract(url)

print("--- extract time %s seconds ---\n" % (time.time() - start_time))
current_time = time.time()
    
data = html_clean(html_content, keywords)
print("--- clean time %s seconds ---\n" % (time.time() - current_time))
current_time = time.time()

print(analyse_json(data))
print("--- analysis time %s seconds ---\n" % (time.time() - current_time))

print("--- %s seconds ---\n" % (time.time() - start_time))