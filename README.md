# Table of contents
1. [Setting up the project](#setup)
2. [How to use the web app](#testing)

## Setup for Next.Js + Flask <a name="setup"></a>
### Clone the Repository
In your terminal, navigate to the desired project directory, and run:
1. ```git clone https://github.com/Jway77-ai/uob-hackathon-dragons.git```
2. ```cd uob-hackathon-dragons```
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

## How to use the web app <a name="testing"></a>
1. Navigate to the Bitbucket repo. [Sample repo for testing](https://bitbucket.org/debugging-dragons/webhook-codedoc/src/main/).
2. Create a branch, make your changes and commit them, make a pull request.
3. Navigate to the web app deployed on Vercel: https://uob-hackathon-dragons.vercel.app/
4. You should see your pull request on the dashboard. You may click "View" to see the provided feedback by the AI, and ask it any questions you may have.
5. Update your branch on Bitbucket based on the feedback. The PR feedback and status should be updated based on your changes.
