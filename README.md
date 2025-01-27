# Table of contents
1. [Features](#features)
2. [Architecture and workflow](#workflow)
3. [Setting up the project](#setup)
4. [How to use AI Code Reviewer](#testing)
5. [Tech Stack](#stack)
6. [Further Improvements](#improvements)
7. [Links](#links)

## Features <a name="features"></a>
![image](![image](https://github.com/user-attachments/assets/43dca0f9-717a-4d52-b261-ab0cdc68069d)

1. Pull Request AI Code Reviewer is a web application that streamlines the pull request review process with the assistance of AI feedback.
2. The dashboard displays recently created pull requests. The user is able to see all relevant information regarding the pull request, like its status and the file differences when they click on it.
3. Each pull request is thoroughly reviewed by AI, with suggestions for improvements. The AI will provide feedback on syntax errors, logical errors, code quality/organization, error handling etc.
4. The user will be able to chat with the AI to ask further questions on the given feedback, clear any doubts they may have, or ask for more advice.
![image](![prStuff](https://github.com/user-attachments/assets/1846b105-38bd-4713-9539-c4f789684610)

## Architecture and workflow <a name="workflow"></a>
The workflow is designed to enhance code quality and streamline the review process through the following steps: 

![image](https://github.com/user-attachments/assets/ee51aec0-3286-4b57-88f1-63ac1109dffb)

1. **Pull Request Creation**: When a pull request (PR) is created or updated in Bitbucket, a webhook is triggered automatically.
2. **Webhook Trigger**: The webhook sends an HTTP request to our python flask server, providing details of the pull request like PR id.
3. **Retrieve PR details**: The actual PR diff is retrieved using Bitbucket API.
4. **PR Processing**: The server processes the relevant information, including the code diffs and metadata about the pull request. These data is sent to Groq LLM api, which will analyze the code changes and provide feedback on the code quality and logic, providing feedback and suggestions for improvement.
5. **Saving details to the database**: All the relevant information about the pull request is saved to a PostgresSQL database. This includes the feedback from the AI.
6. **Web app dashboard page**: When the user access the dash board on the web app, a number of past reviewed PRs will be fetched from the database to be displayed. The user can click on any of them to view the feedback provided by the AI as well as other PR details like the files changed.
7. **Web app PR details page/chatbot**: When the user clicks on any of the PRs in step 6, they can view all PR related details. They can also chat with the chatbot, and ask it questions regarding the feedback provided. The conversation for each PR is saved in the database, and will always maintain context of previous queries regarding that PR.

## Setup for Next.js + Flask <a name="setup"></a>
### Clone the Repository
In your terminal, navigate to the desired project directory, and run:
1. ```git clone https://github.com/Jway77-ai/PR-AI-Code-Reviewer.git```
2. ```cd PR-AI-Code-Reviewer```
* Note: Other than the setup below, you may have to install any other software you may be missing like Python, NodeJS, pip, npm etc.

### Backend Prerequisites
**Create a virtual environment for the project:**
#### On Windows
1. ```python -m venv venv```
2. ```.\venv\Scripts\activate```
#### On macOS/Linux
1. ```python3 -m venv venv```
2. ```source venv/bin/activate```

**Install the requirements in the virtual environment:**

```pip install -r requirements.txt```

### Frontend Prerequisites
#### Install pnpm
```npm i -g pnpm```

#### Install Dependencies: Install all necessary dependencies by running:
```pnpm install```

### Run the Development Server: 
**Start the NextJs development server with:**

```pnpm dev```

This command will start the NextJs with Flask app in development mode. Open http://localhost:3000 in your browser to view it.

## How to use Pull Request AI Code Reviewer <a name="testing"></a>
1. Navigate to the Bitbucket repo. [Sample repo for testing](https://bitbucket.org/debugging-dragons/webhook-codedoc/src/main/).
    - If you want to use your own Bitbucket repo, create a webhook and link it to this endpoint: https://PR-AI-Code-Reviewer.vercel.app/api/pr

       ![image](https://github.com/user-attachments/assets/332bb488-92b3-4246-96e6-1caf0372d5dc)

3. Create a branch, make your changes and commit them, make a pull request.
4. Navigate to the web app deployed on Vercel: https://PR-AI-Code-Reviewer.vercel.app/
5. You should see your pull request on the dashboard. You may click "View" to see the provided feedback by the AI, and ask it any questions you may have.
6. Update your branch on Bitbucket based on the feedback. The PR feedback and status should be updated based on your changes.

## Tech Stack <a name="stack"></a>
- Backend: Python Flask, PostgresSQL db
- Frontend: Next.js, React, Tailwind CSS
- LLM API: Groq
- Version Control Software: Github (source code), Bitbucket (sample repo with pull requests for our app to perform code reviews on)
- Deployment: Vercel

## Further Improvements <a name="improvements"></a>
If we do continue development on the app in the future, the following features are some possible improvements to be added.
- Update the app to work with other repos like Github and Bitbucket Server. Currently it is tailored for Bitbucket Cloud.
- Improved role-based chatbot for different functions and focus area.
- Allow the user to authenticate and log in with their Bitbucket accounts to grant the app permission to access their repo data. This allows us to access their pull requests without a webhook, and associate each pull request with a user so that they can only view the feedback for their pull requests and not other users'.
- Improve the UI, and add the ability to view more than 15 PRs on the dashboard at once, as well as search by PR id. Also improve on the layout of the PR feedback page.
- Improve the capability of the chatbot to perhaps also review the pull request not just based on the individual edited files but also based on the context of the other possibly related files in the repo too.

## Links <a name="links"></a>
- Pull Request AI Code Reviewer web app: https://PR-AI-Code-Reviewer.vercel.app/
- Bitbucket repo for testing: https://bitbucket.org/debugging-dragons/webhook-codedoc/src
