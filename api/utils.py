def get_all_prs_from_repo():
    """
    Fetch all pull requests from Bitbucket repository.
    """
    try:
        BITBUCKET_KEY = os.getenv("BITBUCKET_KEY")
        BITBUCKET_SECRET = os.getenv("BITBUCKET_SECRET")
        BITBUCKET_WORKSPACE = os.getenv("BITBUCKET_WORKSPACE")
        BITBUCKET_REPO_SLUG = os.getenv("BITBUCKET_REPO_SLUG")

        # Obtain access token
        token_url = "https://bitbucket.org/site/oauth2/access_token"
        response = requests.post(
            token_url,
            data={"grant_type": "client_credentials"},
            auth=HTTPBasicAuth(BITBUCKET_KEY, BITBUCKET_SECRET)
        )
        if response.status_code == 200:
            access_token = response.json().get("access_token")

            # URL to get all pull requests
            url = f"https://api.bitbucket.org/2.0/repositories/{BITBUCKET_WORKSPACE}/{BITBUCKET_REPO_SLUG}/pullrequests"
            headers = {'Authorization': f'Bearer {access_token}'}

            # Make the request to fetch all PRs
            reply = requests.get(url, headers=headers)
            if reply.status_code == 200:
                return reply.json()
            else:
                logging.error(f"Failed to fetch PRs: {reply.status_code}, {reply.text}")
                raise Exception(f"Failed to fetch PRs: {reply.status_code}")
        else:
            logging.error(f"Failed to get access token: {response.status_code}, {response.text}")
            raise Exception("Failed to get access token")
    except Exception as e:
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
    response = get_pr_from_repo(pr_id)
    if response.status_code != 200:
        logging.error(f"Failed to retrieve PR diff: {response.status_code}, {response.text}")
        raise Exception("Failed to retrieve PR diff!!")
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
