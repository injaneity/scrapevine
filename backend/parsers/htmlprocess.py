import json
import re
from bs4 import BeautifulSoup

def remove_duplicate_dicts(lst):
    """
    Remove duplicate dictionaries from a list. Dictionaries are considered
    duplicates if they have the same key-value pairs, regardless of order.
    """
    seen = set()
    unique_dicts = []
    for d in lst:
        # Ensure the element is a dictionary and not a string or other type
        if isinstance(d, dict):
            # Create a frozenset of items for immutability and hashability
            items = frozenset(d.items())
            if items not in seen:
                seen.add(items)
                unique_dicts.append(d)
    return unique_dicts

def filter_json_object(obj, retain_keywords):
    if isinstance(obj, dict):
        return {
            k: filter_json_object(v, retain_keywords)
            for k, v in obj.items()
            if any(keyword in k.lower() for keyword in retain_keywords)
        }
    elif isinstance(obj, list):
        return [filter_json_object(item, retain_keywords) for item in obj]
    else:
        return obj

def extract_elements_and_clean_json(html_content, output_file_path):
    soup = BeautifulSoup(html_content, 'html.parser')
    relevant_elements = {}

    title_tag = soup.find('title')
    if title_tag:
        relevant_elements['title'] = [title_tag.get_text(strip=True)]

    for key in ['price', 'name', 'description']:
        elements = soup.find_all(class_=re.compile(f'\\b{key}\\b', re.IGNORECASE)) + \
                   soup.find_all(id=re.compile(f'\\b{key}\\b', re.IGNORECASE))
        relevant_elements[key] = [elem.get_text(strip=True) for elem in elements]

    retain_keywords = ['name', 'title', 'description', 'price']
    json_objects = re.findall(r'\{.*?\}', html_content, re.DOTALL)
    cleaned_objects = []

    for obj_str in json_objects:
        try:
            parsed_obj = json.loads(obj_str)
            filtered_obj = filter_json_object(parsed_obj, retain_keywords)
            if filtered_obj:  # Ensure the filtered object is not empty
                cleaned_objects.append(filtered_obj)
        except json.JSONDecodeError:
            continue
        
    cleaned_objects = remove_duplicate_dicts(cleaned_objects)
        
    combined_data = {
        "relevant_elements": relevant_elements,
        "cleaned_json_objects": cleaned_objects
    }
    
    with open(output_file_path, 'w', encoding='utf-8') as out_file:
        json.dump(combined_data, out_file, ensure_ascii=False, indent=4)

# Example usage
file_path = './data.txt'
with open(file_path, 'r') as file:
    html_content = file.read()
    
soup = BeautifulSoup(html_content, 'html.parser')

output_file_path = './output_file.json'  # Specify your output file path here

# Assuming the HTML content is loaded into `html_content`
extract_elements_and_clean_json(html_content, output_file_path)

print(f"Cleaned JSON objects have been saved to {output_file_path}")
