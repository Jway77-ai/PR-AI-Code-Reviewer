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
    url = f"https://api.bitbucket.org/2.0/repositories/{BITBUCKET_WORKSPACE}/{BITBUCKET_REPO_SLUG}/pullrequests/5/diff"
    headers = {'Authorization': f'Bearer {access_token}'}

    # Make the request to get the pull request diff
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("PR details:")
        print(response.text)
    else:
        print("Failed to get PR details:", response.status_code, response.text)
else:
    print("Failed to get access token:", response.status_code, response.text)
