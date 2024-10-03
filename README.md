# Setup for Next.Js + Flask
## Clone the Repository
In your terminal, navigate to the desired project directory, and run:
1. ```git clone https://github.com/Jway77-ai/uob-hackathon-dragons.git```
2. ```cd uob-hackathon-dragons```
* Note: Other than the setup below, you may have to install any other software you may be missing like Python, NextJS, Javascript etc.

## Backend Prerequisites
**Create a virtual environment for the project:**
### On Windows
1. ```python -m venv venv```
2. ```.\venv\Scripts\activate```
### On macOS/Linux
1. ```python3 -m venv venv```
2. ```source venv/bin/activate```

**Install the requirements in the virtual environment:**

```pip install -r requirements.txt```

## Frontend Prerequisites
### Install pnpm
```npm i -g pnpm```

### Install Dependencies: Install all necessary dependencies by running:
```pnpm install```

## Run the Development Server: 
**Start the NextJs development server with:**

```pnpm dev```

This command will start the NextJs with Flask app in development mode. Open http://localhost:3000 in your browser to view it.
