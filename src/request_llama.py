***REMOVED***quests

url = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.1-8B-Instruct"

token = ""

def llm(query):
    # print(query) 
    parameters = {
        "max_new_tokens": 5000,
        "temperature": 0.01,
        "top_k": 50,
        "top_p": 0.95,
        "return_full_text": False
        }
  
    prompt = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>You are a helpful and smart assistant. You accurately provide answer to the provided user query.<|eot_id|><|start_header_id|>user<|end_header_id|> Here is the query: ```{query}```.
        Provide precise and concise answer.<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
  
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
  
    prompt = prompt.replace("{query}", query)
  
    payload = {
        "inputs": prompt,
        "parameters": parameters
    }
  
    response = requests.post(url, headers=headers, json=payload)
    print("Raw API Response:", response.json())
    
    response = requests.post(url, headers=headers, json=payload)
    response_json = response.json()

    if 'error' in response_json:
        print(f"API Error: {response_json['error']}")
        return f"Error: {response_json['error']}"
    else:
    # Handle successful response
        response_text = response_json[0]['generated_text'].strip()
        return response_text
    # Commenting out the line that's causing the error
    # response_text = response.json()[0]['generated_text'].strip()
    # print(response_text)
    # Temporarily return the raw response for debugging
    return "Check the printed raw API response above for structure"

result = llm('write a python program to generate fibonacci series')

print(result)