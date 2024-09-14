import os
import logging
import requests
from groq import Groq
from .index import db
from .models import PR
from datetime import datetime
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth

# Load environment variables from the .env file
load_dotenv()

# Retrieve OAuth credentials from environment variables
BITBUCKET_KEY = os.getenv("BITBUCKET_KEY")  # Your OAuth consumer key
BITBUCKET_SECRET = os.getenv("BITBUCKET_SECRET")  # Your OAuth consumer secret
# Request URL for access token (using client credentials flow)
token_url = "https://bitbucket.org/site/oauth2/access_token"

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

    # Request the access token
    response = requests.post(
        token_url,
        data={"grant_type": "client_credentials"},
        auth=HTTPBasicAuth(BITBUCKET_KEY, BITBUCKET_SECRET)
    )

    # Check if the response was successful
    if response.status_code == 200:
        # Extract the access token from the response
        access_token = response.json().get("access_token")
        print("Access token:", access_token)

        # Retrieve repository details from environment variables
        BITBUCKET_WORKSPACE = os.getenv("BITBUCKET_WORKSPACE")
        BITBUCKET_REPO_SLUG = os.getenv("BITBUCKET_REPO_SLUG")

        # URL to get the pull request diff
        url = f"https://api.bitbucket.org/2.0/repositories/{BITBUCKET_WORKSPACE}/{BITBUCKET_REPO_SLUG}/pullrequests/{pr_id}/diff"
        headers = {'Authorization': f'Bearer {access_token}'}

        # Make the request to get the pull request diff
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            logging.error(f"Failed to retrieve PR diff: {response.status_code} - {response.text}")
            raise Exception("Failed to retrieve PR diff!!")

        else:
            diff_text = response.text
            detailed_changes = []
            current_file = None
            lines_added = []
            lines_removed = []

            for line in diff_text.splitlines():
                if line.startswith("diff --git"):
                    if current_file:
                        # Strip the 'a/' prefix from the path
                        file_path = current_file.replace('a/', '').replace('b/', '')
                        detailed_changes.append({
                            'path': file_path,
                            'lines_added': lines_added,
                            'lines_removed': lines_removed
                        })
                    current_file = line.split(" ")[2]
                    lines_added = []
                    lines_removed = []
                elif line.startswith("@@"):
                    pass
                elif line.startswith("+"):
                    if not (line.startswith("++ ") or line.startswith("+++") or line.startswith("new file mode")):  # Exclude metadata lines
                        lines_added.append(line[1:])
                elif line.startswith("-"):
                    if not (line.startswith("-- ") or line.startswith("---") or line.startswith("deleted file mode")):  # Exclude metadata lines
                        lines_removed.append(line[1:])

            if current_file:
                # Strip the 'a/' prefix from the path
                file_path = current_file.replace('a/', '').replace('b/', '')
                detailed_changes.append({
                    'path': file_path,
                    'lines_added': lines_added,
                    'lines_removed': lines_removed
                })
            return detailed_changes
    else:
        print("Failed to get access token:", response.status_code, response.text)


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

def queryLLM(context, user_query):
    groq_API = os.getenv("GROQ_API_KEY")
    if not groq_API:
        raise ValueError("GROQ_API_KEY not set in environment variables")
    client = Groq(api_key=groq_API)

    if data is None:
        data = ""

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": user_query}
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