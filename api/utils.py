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
from pytz import timezone, utc
from flask import jsonify

# Load environment variables from the .env file
load_dotenv()

def get_all_prs_from_repo():
    """
    Fetch all pull requests from Bitbucket repository, including all states and handling pagination.
    """
    try:
        # Get Bitbucket credentials from environment variables
        BITBUCKET_KEY = os.getenv("BITBUCKET_KEY")
        BITBUCKET_SECRET = os.getenv("BITBUCKET_SECRET")
        BITBUCKET_WORKSPACE = os.getenv("BITBUCKET_WORKSPACE")
        BITBUCKET_REPO_SLUG = os.getenv("BITBUCKET_REPO_SLUG")

        # Obtain access token
        token_url = "https://bitbucket.org/site/oauth2/access_token"
        token_response = requests.post(
            token_url,
            data={"grant_type": "client_credentials"},
            auth=HTTPBasicAuth(BITBUCKET_KEY, BITBUCKET_SECRET)
        )
        token_response.raise_for_status()
        access_token = token_response.json()["access_token"]

        # Set up for PR fetching
        headers = {'Authorization': f'Bearer {access_token}'}
        url = f"https://api.bitbucket.org/2.0/repositories/{BITBUCKET_WORKSPACE}/{BITBUCKET_REPO_SLUG}/pullrequests"
        params = {'state': 'ALL', 'pagelen': 50}
        
        all_prs = []

        # Fetch PRs with pagination
        while url:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            all_prs.extend(data['values'])
            url = data.get('next')
            params = {}  # Clear params for subsequent requests

        logging.info(f"Total PRs fetched: {len(all_prs)}")
        return {'values': all_prs}

    except requests.RequestException as e:
        logging.error(f"Error fetching PRs from Bitbucket: {e}")
        raise

def get_pr_from_repo(pr_id):
    #Improved try catch for error logging
    try:
        BITBUCKET_KEY = os.getenv("BITBUCKET_KEY")
        BITBUCKET_SECRET = os.getenv("BITBUCKET_SECRET")

        token_url = "https://bitbucket.org/site/oauth2/access_token"
        response = requests.post(
            token_url,
            data={"grant_type": "client_credentials"},
            auth=HTTPBasicAuth(BITBUCKET_KEY, BITBUCKET_SECRET)
        )
        if response.status_code == 200:
            access_token = response.json().get("access_token")
            BITBUCKET_WORKSPACE = os.getenv("BITBUCKET_WORKSPACE")
            BITBUCKET_REPO_SLUG = os.getenv("BITBUCKET_REPO_SLUG")
            url = f"https://api.bitbucket.org/2.0/repositories/{BITBUCKET_WORKSPACE}/{BITBUCKET_REPO_SLUG}/pullrequests/{pr_id}/diff"
            headers = {'Authorization': f'Bearer {access_token}'}

            reply = requests.get(url, headers=headers)
            if reply.status_code == 200:
                return reply
            else:
                logging.error(f"Failed to fetch PR: {reply.status_code}, {reply.text}")
                raise Exception(f"Failed to fetch PR: {reply.status_code}")
        else:
            logging.error(f"Failed to get access token: {response.status_code}, {response.text}")
            raise Exception("Failed to get access token")
    except Exception as e:
        logging.error(f"Error fetching PR from Bitbucket: {e}")
        raise

def get_file_contents(file_path, target_branch):
    try:
        BITBUCKET_KEY = os.getenv("BITBUCKET_KEY")
        BITBUCKET_SECRET = os.getenv("BITBUCKET_SECRET")

        token_url = "https://bitbucket.org/site/oauth2/access_token"
        response = requests.post(
            token_url,
            data={"grant_type": "client_credentials"},
            auth=HTTPBasicAuth(BITBUCKET_KEY, BITBUCKET_SECRET)
        )
        if response.status_code == 200:
            access_token = response.json().get("access_token")
            BITBUCKET_WORKSPACE = os.getenv("BITBUCKET_WORKSPACE")
            BITBUCKET_REPO_SLUG = os.getenv("BITBUCKET_REPO_SLUG")

            url = f"https://api.bitbucket.org/2.0/repositories/{BITBUCKET_WORKSPACE}/{BITBUCKET_REPO_SLUG}/src/{target_branch}/{file_path}"
            headers = {'Authorization': f'Bearer {access_token}'}
            
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.text
            elif response.status_code == 404:
                logging.info(f"File '{file_path}' is a new file.")
                return "<This is a new file with no original content.>"
            else:
                logging.error(f"Failed to fetch file content: {response.status_code}, {response.text}")
                return None
        else:
            logging.error(f"Failed to get access token: {response.status_code}, {response.text}")
            raise Exception("Failed to get access token")
    except Exception as e:
        logging.error(f"Error fetching file contents from Bitbucket: {e}")
        raise

def get_raw_files_diff(pr_id):
    response = get_pr_from_repo(pr_id)
    if response.status_code != 200:
        logging.error(f"Failed to retrieve PR diff: {response.status_code}, {response.text}")
        raise Exception("Failed to retrieve PR diff!!")
    else:
        return response.text

def get_files_diff(pr_id, target_branch):
    """
    Gets the file diff from bitbucket based on the given pr_id, and extracts the required data into 'detailed_changes'.
    'detailed_changes' is a list of files that have changed. For each file, there is a dict containing the path of the file,
    a list of lines added, and a list of lines removed.
    Example of files_diff:
    files_diff = [
    {'path': "main.py",
        'original_contents': ["print('Remove me')]"],
        'lines_added': ["print('Hello, world!')", "print('Bye, world!')"],
        'lines_removed': ["print('Remove me')]"]
        }, 
    {'path': "quickMaths.py",
        'original_contents': ["a = 5"],
        'lines_added': ["x = 1", "y = 2", "z = 3"],
        'lines_removed': []
        }
    ]
    """
    response = get_pr_from_repo(pr_id)
    if response.status_code != 200:
        logging.error(f"Failed to retrieve PR diff: {response.status_code}, {response.text}")
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
                    original_contents = get_file_contents(file_path, target_branch)
                    detailed_changes.append({
                        'path': file_path,
                        'original_contents': original_contents,
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
            original_contents = get_file_contents(file_path, target_branch)
            detailed_changes.append({
                'path': file_path,
                'original_contents': original_contents,
                'lines_added': lines_added,
                'lines_removed': lines_removed
            })
        return detailed_changes

def process_files_diff(files_diff):
    """
    Formats the files_diff into a string, removing lines that appear in both lines_added and lines_removed as those lines are unchanged.
    """
    formatted_string = "\n".join(
        f"Path: {item['path']}\n"
        f"Original Contents of file:\n" + item['original_contents'] + "\n"
        f"Lines Added:\n" + "\n".join(f"  {line}" for line in item['lines_added'] if line not in item['lines_removed']) + "\n"
        f"Lines Removed:\n" + "\n".join(f"  {line}" for line in item['lines_removed'] if line not in item['lines_added'])
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
                {"role": "user", "content": f"Please help to review the following pull request data. For each modified file, I have provided the original contents of that file, as well as the lines added and removed: \n{data}"}
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
    """
    Further queries to Groq AI. Provide context and a user query.
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

def handle_date(date_input, to_sgt=False, as_string=False):
    """
    Handle date conversion from string to datetime and optionally to SGT.
    """
    # If input is a string, parse it to datetime
    if isinstance(date_input, str):
        dt = datetime.fromisoformat(date_input.rstrip('Z')).replace(tzinfo=utc)
    elif isinstance(date_input, datetime):
        dt = date_input.replace(tzinfo=utc) if date_input.tzinfo is None else date_input
    else:
        raise ValueError("Input must be a string or datetime object")

    # Convert to SGT if requested
    if to_sgt:
        sgt = timezone('Asia/Singapore')
        dt = dt.astimezone(sgt)

    # Return as string if requested, else return datetime object
    if as_string:
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    return dt

def process_pr(pr_id, target_branch):
    try:
        # Fetch the PR diff from Bitbucket
        raw_files_diff = get_raw_files_diff(pr_id)
        files_diff = get_files_diff(pr_id, target_branch)
        processed_diff = process_files_diff(files_diff)

        # Example LLM analysis (optional)
        prompt_file_path = os.path.join(os.path.dirname(__file__), 'prompttext')
        with open(prompt_file_path, 'r') as file:
            prompt_text = file.read().strip()
        feedback = analyze_code_with_llm(prompt_text, processed_diff)
        return raw_files_diff, processed_diff, feedback
    except FileNotFoundError:
        logging.error(f"Prompt file not found: {prompt_file_path}")
        raise Exception(f"Error processing pull request: Prompt file not found: {prompt_file_path}")
    except Exception as e:
        logging.error(f"Error processing pull request: {e}")
        raise Exception(f"Error processing pull request: {e}")