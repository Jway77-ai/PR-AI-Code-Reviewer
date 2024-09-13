import os
import logging
import requests
from groq import Groq
from .index import db
from .models import PR
from datetime import datetime

# Fetch values from environment variables
BITBUCKET_USERNAME = os.getenv("BITBUCKET_USERNAME")
BITBUCKET_REPO_SLUG = os.getenv("BITBUCKET_REPO_SLUG")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

def get_files_diff(pr_id):
    """
    Gets the file diff from bitbucket based on the given pr_id, and extracts the required data into 'detailed_changes'.
    'detailed_changes' is a list of files that have changed. For each file, there is a dict containing the path of the file,
    a list of lines added, and a list of lines removed.
    Example of files_diff:
    files_diff = [
    {'path': "src/main.py",
        'lines_added': ["print('Hello, world!')", "print('Bye, world!')"],
        'lines_removed': ["print('Remove me')]"]
        }, 
    {'path': "src/quickMaths.py",
        'lines_added': ["x = 1", "y = 2", "z = 3"],
        'lines_removed': []
        }
    ]
   url = f"https://api.bitbucket.org/2.0/repositories/{BITBUCKET_USERNAME}/{BITBUCKET_REPO_SLUG}/pullrequests/{pr_id}/diff"
    """
    url = f"https://bitbucket.org/{BITBUCKET_USERNAME}/{BITBUCKET_REPO_SLUG}/pull-requests/{pr_id}/diff"
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
    """
    Formats the files_diff into a string
    """    
    formatted_string = "\n".join(
    f"Path: {item['path']}\n"
    f"Lines Added:\n" + "\n".join(f"  {line}" for line in item['lines_added']) + "\n"
    f"Lines Removed:\n" + "\n".join(f"  {line}" for line in item['lines_removed'])
    for item in files_diff
)
    return formatted_string

def analyze_code_with_llm(prompt, data):
    """
    Sends the data and prompt to Groq AI.
    """
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

def insert_dummy_pr():
    # Create a new PR instance
    dummy_pr = PR(
        pr_id="12345",
        sourceBranchName="feature/branch",
        targetBranchName="main",
        content="""Path: src/main.py
                Lines Added:
                    print('Hello, world!')
                    print('Bye, world!')
                Lines Removed:
                    print('Remove me')
                Path: src/quickMaths.py
                Lines Added:
                    x = 1
                    y = 2
                    z = 3
                Lines Removed:
                    """,
        feedback="Well done!.",
        date_created=datetime.utcnow()
    )

    # Add and commit the new PR to the database
    try:
        db.session.add(dummy_pr)
        db.session.commit()
        print("Dummy PR inserted successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Error inserting dummy PR: {e}")