import json
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

# print(os.getenv('GPT_API'))

client = OpenAI(api_key=os.getenv('GPT_API'))

def analyse_json(data):
    
    with open('prompt.txt', 'r') as file:
        prompt_text = file.read().strip()

    # Step 2: Read the data from 'data.json'
    #with open('./output.json', 'r') as file:
        #data = json.load(file)
    code_text = json.dumps(data, indent=2)

    # Step 3: Combine the prompt, code, and prompt again in the specified structure
    combined_input = f"[{prompt_text}]\n\n[code]\n\n{code_text}\n\n[prompt]\n\n{prompt_text}"
    
    summary = client.chat.completions.create(
    model = "gpt-4-1106-preview",
    messages=[
        {
        "role": "user",
        "content": [
            {"type": "text", "text": f"{combined_input}"},
        ],
        }
    ],
    temperature = 0,
    top_p = 0,
    )
    return (summary.choices[0].message.content)
