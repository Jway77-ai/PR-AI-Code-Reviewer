import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve OAuth credentials from environment variables
BITBUCKET_KEY = os.getenv("BITBUCKET_KEY")  # Your OAuth consumer key
BITBUCKET_SECRET = os.getenv("BITBUCKET_SECRET")  # Your OAuth consumer secret

# Request URL for access token (using client credentials flow)
token_url = "https://bitbucket.org/site/oauth2/access_token"

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
    url = f"https://api.bitbucket.org/2.0/repositories/{BITBUCKET_WORKSPACE}/{BITBUCKET_REPO_SLUG}/pullrequests/8/diff"
    headers = {'Authorization': f'Bearer {access_token}'}

    # Make the request to get the pull request diff
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("PR details:")
        print("Processed:")
        diff_text = response.text
        print("Diff Text:", diff_text)

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
                # Skip diff chunks, we might add more processing here
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

        print("Detailed changes:", detailed_changes)
    else:
        print("Failed to get PR details:", response.status_code, response.text)
else:
    print("Failed to get access token:", response.status_code, response.text)
