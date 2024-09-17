import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Flask app configuration
app = Flask(__name__)

# Get the DATABASE_URL from environment variables (default to SQLite if not set)
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///test.db')

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL  # Use the local SQLite database for testing
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Bitbucket API configuration
BITBUCKET_KEY = os.getenv('BITBUCKET_KEY')
BITBUCKET_SECRET = os.getenv('BITBUCKET_SECRET')
BITBUCKET_WORKSPACE = os.getenv('BITBUCKET_WORKSPACE')
BITBUCKET_REPO_SLUG = os.getenv('BITBUCKET_REPO_SLUG')
BITBUCKET_URL = f"https://api.bitbucket.org/2.0/repositories/{BITBUCKET_WORKSPACE}/{BITBUCKET_REPO_SLUG}/pullrequests"

# PR Model
class PR(db.Model):
    __tablename__ = 'PR'
    id = db.Column(db.Integer, primary_key=True)
    pr_id = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(200), nullable=True)
    sourceBranchName = db.Column(db.String(200), nullable=False)
    targetBranchName = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=True)
    feedback = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime)

def get_access_token():
    """Get an OAuth access token using key and secret."""
    token_url = "https://bitbucket.org/site/oauth2/access_token"
    auth = (BITBUCKET_KEY, BITBUCKET_SECRET)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'client_credentials'}

    try:
        response = requests.post(token_url, headers=headers, data=data, auth=auth)
        response.raise_for_status()  # Raise an error for bad responses
        access_token = response.json().get('access_token')
        if not access_token:
            raise Exception("Failed to obtain access token")
        return access_token
    except requests.RequestException as e:
        print(f"Error obtaining access token: {e}")
        return None

def fetch_data_from_bitbucket():
    """Fetch pull request data from Bitbucket using an access token."""
    access_token = get_access_token()
    if not access_token:
        print("Could not get access token. Exiting.")
        return

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    try:
        # Fetch pull request data from Bitbucket
        response = requests.get(BITBUCKET_URL, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the JSON response
        data = response.json()

        # Extract pull request details and save to local database
        for pr in data.get('values', []):
            new_pr = PR(
                pr_id=str(pr['id']),
                title=pr.get('title', 'No Title'),
                sourceBranchName=pr['source']['branch']['name'],
                targetBranchName=pr['destination']['branch']['name'],
                content=pr.get('description', ''),
                date_created=pr['created_on']
            )
            db.session.add(new_pr)

        db.session.commit()
        print("Pull request data fetched and saved successfully.")

    except requests.RequestException as e:
        print(f"Error fetching data from Bitbucket: {e}")
    except Exception as e:
        db.session.rollback()
        print(f"Error saving data to the database: {e}")

if __name__ == '__main__':
    with app.app_context():
        fetch_data_from_bitbucket()
