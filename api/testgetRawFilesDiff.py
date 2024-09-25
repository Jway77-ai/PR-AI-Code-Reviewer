import os
import logging
import requests
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth
from pytz import timezone, utc

# Load environment variables from the .env file
load_dotenv()

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

def get_raw_files_diff(pr_id):
    response = get_pr_from_repo(pr_id)
    if response.status_code != 200:
        logging.error(f"Failed to retrieve PR diff: {response.status_code}, {response.text}")
        raise Exception("Failed to retrieve PR diff!!")
    else:
        return response.text

print(get_raw_files_diff(41))

