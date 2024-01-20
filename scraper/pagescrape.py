# import requests
# from bs4 import BeautifulSoup
# import re

# def scrape(url):
#     headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
#     }
#     response = requests.get(url, headers=headers)

#     if response.status_code != 200:
#         print(response.status_code)
#         return("Failed to retrieve the website")
    
#     soup = BeautifulSoup(response.content, 'html.parser')
#     clean = soup.body.get_text(strip=True).replace("\n", "")
#     print("--------------")
    
#     pattern = r'[a-zA-Z]{15,}|\d{15,}|[^\w\s]{15,}|[<>?!]'
#     clean = re.sub(pattern, '', clean)
    
#     pattern = r'[\$€¥]\d+(?:[:.]\d{2})?'
#     prices = re.findall(pattern, clean)
    
#     for price in prices:
#         converted_price = ''.join(re.findall(r'\d+', price))
#         if int(converted_price) != 0:
#             return clean, price
        
#     return clean


# urls = []
# #1 love bonito
# urls.append('https://www.lovebonito.com/sg/mira-knit-midi-dress.html')

# #2 shopee
# urls.append('https://shopee.sg/Nintendo-Switch-Used-Games-Collection-02-(Choose-Your-Game)-i.4396874.23083613314?publish_id=&sp_atk=b053ba83-48ce-4690-8b27-d44ff2f3af39&xptdk=b053ba83-48ce-4690-8b27-d44ff2f3af39')

# #3 pazzion
# urls.append('https://www.pazzion.com/collections/shoes-flats/products/elaia-point-toe-ballerina-flats?variant=42287420899571')

# #4 h&m
# urls.append('https://www2.hm.com/en_sg/productpage.1200597001.html')

# #5 amazon
# urls.append('https://www.amazon.sg/ProCase-MacBook-Release-13-inch-Keyboard/dp/B07K87DFY3/ref=sr_1_5?crid=6D4ASC65XN6M&keywords=macbook+case&qid=1705478996&sprefix=macbook+ca%2Caps%2C350&sr=8-5')

# #6 cos
# urls.append('https://www.cos-singapore.com/products/cos-oversized-quilted-mens-crossbody-bag-black-singapore351tgszvc-p-24.html')

# #7 stanley
# urls.append('https://www.stanley1913.com/products/clean-slate-quencher-h2-0-flowstate%E2%84%A2-tumbler-40-oz-1')

# #8 nike
# urls.append('https://www.nike.com/sg/t/air-jordan-1-low-shoes-6Q1tFM/553558-161')
  
# for url in urls:
#     print(scrape(url))