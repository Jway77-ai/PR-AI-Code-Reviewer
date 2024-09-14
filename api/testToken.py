import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

BITBUCKET_KEY = os.getenv("BITBUCKET_KEY")  # Your OAuth consumer key
BITBUCKET_SECRET = os.getenv("BITBUCKET_SECRET")  # Your OAuth consumer secret
print("key", BITBUCKET_KEY)
print("secret", BITBUCKET_SECRET)

# Request URL for access token (using client credentials flow)
token_url = "https://bitbucket.org/site/oauth2/access_token"

# Request the access token
response = requests.post(
    token_url,
    data={"grant_type": "client_credentials"},
    auth=HTTPBasicAuth(BITBUCKET_KEY, BITBUCKET_SECRET)
)
print(response)
# Extract the access token from the response
access_token = response.json().get("access_token")

if access_token:
    print("Access token:", access_token)

    BITBUCKET_WORKSPACE = os.getenv("BITBUCKET_WORKSPACE")
    BITBUCKET_REPO_SLUG = os.getenv("BITBUCKET_REPO_SLUG")
    ACCESS_TOKEN = access_token
    url = f"https://api.bitbucket.org/2.0/repositories/{BITBUCKET_WORKSPACE}/{BITBUCKET_REPO_SLUG}/pullrequests/5/diff"
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}

    response = requests.get(url, headers=headers)
    print("PR details:")
    print(response.json())

else:
    print("Failed to get access token")


