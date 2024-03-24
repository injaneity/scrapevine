import json
import re
from bs4 import BeautifulSoup

# part 1: extract all elements with keyword

def keyword_unique(json_obj):
    # Check if the top-level JSON object is a list
    if isinstance(json_obj, list):
        # Remove duplicates from the list and apply recursion for each element
        seen = set()
        cleaned_list = []
        for item in json_obj:
            if item not in seen:
                seen.add(item)
                cleaned_list.append(keyword_unique(item))
        return cleaned_list
    elif isinstance(json_obj, dict):  # If the element is a dictionary
        # Apply the function recursively to each value in the dictionary
        for key in json_obj:
            json_obj[key] = keyword_unique(json_obj[key])
        return json_obj
    else:
        # Return the element itself if it's neither a dict nor a list
        return json_obj

def keyword_data(html_content, keywords):
    soup = BeautifulSoup(html_content, 'html.parser')
    data = {}

    # Extract title
    title_tag = soup.find('title')
    if title_tag:
        data['title'] = title_tag.get_text(strip=True)

    # Initialize lists for each keyword
    for keyword in keywords:
        data[keyword] = []

    # Extract elements with class or ID values matching keywords
    for keyword in keywords:
        elements = soup.find_all(class_=re.compile(f'\\b{keyword}\\b', re.IGNORECASE)) + \
                   soup.find_all(id=re.compile(f'\\b{keyword}\\b', re.IGNORECASE))
        for element in elements:
            data[keyword].append(element.get_text(strip=True))
            
    data = keyword_unique(data)

    return data
        

# part 2: extract and clean all json objects

def json_filter(obj, retain_keywords, exclude_keywords):
    if isinstance(obj, dict):
        return {
            k: json_filter(v, retain_keywords, exclude_keywords)
            for k, v in obj.items()
            if (any(keyword.lower() in k.lower() for keyword in retain_keywords) or not retain_keywords) and
            not any(exclude_keyword.lower() in k.lower() for exclude_keyword in exclude_keywords) and
            not isinstance(v, bool)
        }
    elif isinstance(obj, list):
        return [json_filter(item, retain_keywords, exclude_keywords) for item in obj]
    else:
        return obj
    

def json_unique(lst):
    seen = set()
    unique_dicts = []
    for d in lst:
        if isinstance(d, dict):
            # Convert dictionary items to a format that can be hashed
            items = tuple((k, tuple(v) if isinstance(v, list) else v) for k, v in d.items())
            if items not in seen:
                seen.add(items)
                # Convert back the items to dictionary format to maintain original data structure
                unique_dicts.append({k: v if not isinstance(v, tuple) else list(v) for k, v in items})
    return unique_dicts

def json_obj_data(html_content, include_terms, exclude_terms):
    data = []  # Initialize as a list to collect JSON objects

    # Extract all JSON data (enclosed within {})
    json_objects = re.findall(r'\{.*?\}', html_content, re.DOTALL)
    for object_str in json_objects:
        try:
            parsed_object = json.loads(object_str)
            # Pass object into json filter
            clean_object = json_filter(parsed_object, include_terms, exclude_terms)
            if clean_object:
                data.append(clean_object)  # Collect clean objects
        except json.JSONDecodeError:
            continue

    unique_data = json_unique(data)  # Remove duplicates from the list
    
    return unique_data


def clean_html(html_content, keywords):
    
    keywords.append("price")
    keywords.append("name")
    
    exclude_terms = ['childCategory', 'itemNamein', 'promotionname', 'assetname']
    
    combined_data = {
        "html_elements": keyword_data(html_content, keywords),
        "json_objects": json_obj_data(html_content, keywords, exclude_terms)
    }

    # Tokenize the JSON string
    # Each character in the JSON string is considered a token in this context
    
    print("CLEANED HTML:", json.dumps(combined_data))

    with open('./output.json', 'w', encoding='utf-8') as out_file:
        json.dump(combined_data, out_file, ensure_ascii=False, indent=4)
    return(combined_data)
        
# Example usage
# '''
# file_path = './data.txt'
# with open(file_path, 'r') as file:
#     html_content = file.read()

# # Assuming the HTML content is loaded into `html_content`
# keywords = ['name', 'price', 'description']
# html_clean(html_content, keywords)

# print(f"Cleaned JSON objects have been saved to JSON file")
# '''