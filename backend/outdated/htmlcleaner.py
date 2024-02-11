from bs4 import BeautifulSoup
import re

# Assuming `html_content` is your loaded HTML data
file_path = './data.txt'

# Open the file and read its content
with open(file_path, 'r') as file:
    html_content = file.read()
    
soup = BeautifulSoup(html_content, 'html.parser')
    
# required for shopee
#for script in soup.find_all('script'):
    #script.decompose()

# Remove style tags
for style in soup.find_all('style'):
    style.decompose()
    
for tag in soup.find_all(True):
    for attribute in list(tag.attrs):
        if not tag[attribute] or tag[attribute] == "":
            del tag[attribute]
    
for tag_with_href in soup.find_all(href=True):
    del tag_with_href['href']  # Remove the 'href' attribute
    
print('here 1')

# Remove meta tags
for meta in soup.find_all('meta'):
    meta.decompose()

for link in soup.find_all('link'):
    link.decompose()
    
for img_tag in soup.find_all('img'):
    img_tag.decompose()

# Find and remove all <svg> tags
for svg_tag in soup.find_all('svg'):
    svg_tag.decompose()
    
print('here 2')

for path_tag in soup.find_all('path'):
    path_tag.decompose()
    
# Convert back to HTML string if needed
cleaned_html = str(soup)
cleaned_html = re.sub(r'[^\x00-\x7F]+', '', cleaned_html)

pattern = r'\b[A-Fa-f0-9]{32,}\b'  # Adjust the number {32,} as per your requirement
cleaned_html = re.sub(pattern, '', cleaned_html)

pattern = r'"[a-z-]+-live-\d+":\d+[,]?'
cleaned_html = re.sub(pattern, '', cleaned_html)

patterns = [r'\btrue\b', r'\bfalse\b']
for pattern in patterns:
    cleaned_html = re.sub(pattern, '', cleaned_html, flags=re.IGNORECASE)
    
pattern = r'"https?://[^\s"]+?"'
# Replace the matched URLs with an empty string
cleaned_html = re.sub(pattern, '', cleaned_html)

pattern = r'"\w*label\w*":[^,}]*,?'
# Assuming `clean_html` or `json_content` is your content stored in a variable
cleaned_html = re.sub(pattern, '', cleaned_html)

# Pattern to match long numeric sequences, including negative numbers and arrays
numeric_sequence_pattern = r'-?\d{7,}(?:,\d{1,10})+'

# Combine both patterns with | operator to match either
combined_pattern = f'{numeric_sequence_pattern}'

# Assuming `clean_html` is your HTML content
cleaned_html = re.sub(combined_pattern, '', cleaned_html)
    
# Replace the repetitive sequences with an empty string or a single instance as needed
pattern = r'(,"":)+' 
cleaned_html = re.sub(pattern, '', cleaned_html)

# Save the cleaned HTML to a file
with open('cleaned_data.txt', 'w', encoding='utf-8') as file:
    file.write(cleaned_html)
