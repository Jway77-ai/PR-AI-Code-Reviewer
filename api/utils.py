import os
import logging
import requests
from groq import Groq

# Fetch values from environment variables
BITBUCKET_USERNAME = os.getenv("BITBUCKET_USERNAME")
BITBUCKET_REPO_SLUG = os.getenv("BITBUCKET_REPO_SLUG")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

def get_files_diff(pr_id):
    url = f"https://api.bitbucket.org/2.0/repositories/{BITBUCKET_USERNAME}/{BITBUCKET_REPO_SLUG}/pullrequests/{pr_id}/diff"
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        logging.error(f"Failed to retrieve PR diff: {response.status_code} - {response.text}")
        raise Exception("Failed to retrieve PR diff")

    diff_data = response.json()
    detailed_changes = []
    for file in diff_data.get('values', []):
        file_info = {'path': file['path'], 'lines_added': [], 'lines_removed': []}
        for line in file.get('lines', []):
            if line['type'] == 'add':
                file_info['lines_added'].append(line['content'])
            elif line['type'] == 'remove':
                file_info['lines_removed'].append(line['content'])
        detailed_changes.append(file_info)
    return detailed_changes

def process_files_diff(files_diff):
    # Implement your processing logic here
    return str(files_diff)  # Convert to string for storage

def analyze_code_with_llm(prompt, data):
    groq_API = os.getenv("GROQ_API_KEY")
    if not groq_API:
        raise ValueError("GROQ_API_KEY not set in environment variables")

    client = Groq(api_key=groq_API)

    if data is None:
        data = ""

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Please help to review the following pull request data: \n{data}"}
            ],
            model=os.getenv("GROQ_MODEL_NAME", "llama3-8b-8192"),
            temperature=0.5,
            max_tokens=8192,
            top_p=1,
            stop=None,
            stream=False,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        logging.error(f"Error in LLM analysis: {e}")
        raise