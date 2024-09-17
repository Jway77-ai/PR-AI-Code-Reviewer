import os

# Clear specific environment variables
os.environ.pop('BITBUCKET_KEY', None)
os.environ.pop('BITBUCKET_SECRET', None)
os.environ.pop('BITBUCKET_WORKSPACE', None)
os.environ.pop('BITBUCKET_REPO_SLUG', None)
