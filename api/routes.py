from datetime import datetime
from flask import Blueprint, request, jsonify
from groq import Groq
from .models import PR, Conversation
from .utils import get_all_prs_from_repo, get_files_diff, process_files_diff, analyze_code_with_llm, queryLLM, convert_utc_to_gmt8
#from .extensions import db
from .index import db
import os
import requests
import logging
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

main = Blueprint('main', __name__)

@main.route('/api/sync_prs', methods=['POST'])
def sync_all_prs():
    try:
        pr_list = get_all_prs_from_repo()

        # Ensure 'values' key exists in the response
        if 'values' not in pr_list:
            return jsonify({'status': 'error', 'message': 'No PRs found'}), 400

        for pr_data in pr_list['values']:
            pr_id = str(pr_data.get('id', 'Unknown ID'))  # Cast the PR ID to a string
            title = pr_data.get('title', 'No Title')
            status = pr_data.get('state')

            source_branch = pr_data['source']['branch']['name']
            target_branch = pr_data['destination']['branch']['name']

            # Get the latest of 'created_on' and 'updated_on'
            created_on = datetime.fromisoformat(pr_data['created_on'].replace('Z', '+00:00'))
            updated_on = datetime.fromisoformat(pr_data['updated_on'].replace('Z', '+00:00'))

            # Use the latest date between created_on and updated_on
            latest_date = max(created_on, updated_on)

<<<<<<< HEAD
            # Convert to GMT +8 using the helper function
            latest_date_gmt8 = convert_utc_to_gmt8(latest_date)
=======
            # Insert new PR data with latest feedback
            new_pr_diff = PR(
                pr_id=pr_id,
                title=title,
                status=status,
                sourceBranchName=source_branch,
                targetBranchName=target_branch,
                content=processed_diff,
                feedback=feedback,  # Latest feedback
                date_created=datetime.now()
            )
            db.session.add(new_pr_diff)
            db.session.commit()
>>>>>>> parent of 997dfac (Clean routes.py and add new column for role in Conversation table)

<<<<<<< HEAD
            # Process PR diff and feedback (example processing)
=======
        return jsonify({'status': 'success', 'message': 'All PRs synced and saved successfully'}), 200
    except Exception as e:
        logging.error(f"Error syncing PRs: {e}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@main.route('/api/pr', methods=['POST'])
def handle_pr():
    data = request.json

    # Check if "state" exists at the top level and "pullrequest" exists in the request data
    if 'state' not in data:
        return jsonify({'status': 'error', 'message': 'State not found in the request data'}), 400

    if 'pullrequest' not in data:
        return jsonify({'status': 'error', 'message': 'Pull request data not found'}), 400

    # Access the pullrequest object and state
    pr_data = data.get('pullrequest')

    pr_id = pr_data.get('id')
    if pr_id is None:
        return jsonify({'status': 'error', 'message': 'PR ID not found'}), 400
    # If this pr_id already exists, update it instead
    pr_entry = PR.query.filter_by(pr_id=pr_id).first()
    if pr_entry:
        pr_entry.title = pr_data.get('title', 'No Title')
        pr_entry.status = pr_data['state']
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Pull request status updated successfully'}), 200
    else:
        title = pr_data.get('title', 'No Title')
        source_branch = pr_data['source']['branch']['name']
        target_branch = pr_data['destination']['branch']['name']
        status = pr_data['state']

        logging.info(f"Processing PR: {pr_id}, Title: {title}, Status: {status}")

        try:
            # Fetch the PR diff from Bitbucket
>>>>>>> parent of 2d5ba4e (Backend: Cast pr_id to string in /api/pr)
            files_diff = get_files_diff(pr_id)
            processed_diff = process_files_diff(files_diff)

            # Example LLM analysis (optional)
            prompt_file_path = os.path.join(os.path.dirname(__file__), 'prompttext')
            with open(prompt_file_path, 'r') as file:
                prompt_text = file.read().strip()
            feedback = analyze_code_with_llm(prompt_text, processed_diff)

            # Insert or update the PR in the database
            new_pr_diff = PR(
                pr_id=pr_id,
                title=title,
                status=status,
                sourceBranchName=source_branch,
                targetBranchName=target_branch,
                content=processed_diff,
                feedback=feedback,
                date_created=latest_date_gmt8  # Use the latest date in GMT +8
            )

            # Use merge to either insert or update existing records
            db.session.merge(new_pr_diff)
            db.session.commit()

        return jsonify({'status': 'success', 'message': 'All PRs synced and saved successfully'}), 200

    except Exception as e:
        logging.error(f"Error syncing PRs: {e}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@main.route('/api/pr', methods=['POST'])
def handle_pr():
    data = request.json

    # Check if "state" exists at the top level and "pullrequest" exists in the request data
    if 'state' not in data:
        return jsonify({'status': 'error', 'message': 'State not found in the request data'}), 400

    if 'pullrequest' not in data:
        return jsonify({'status': 'error', 'message': 'Pull request data not found'}), 400

    # Access the pullrequest object and state
    pr_data = data.get('pullrequest')
    status = data.get('state')  # Getting the 'state' from the main body
    
    pr_id = pr_data.get('id')
    if pr_id is None:
        return jsonify({'status': 'error', 'message': 'PR ID not found'}), 400

    title = pr_data.get('title', 'No Title')
    source_branch = pr_data['source']['branch']['name']
    target_branch = pr_data['destination']['branch']['name']

    # Handle date fields
    created_on = datetime.fromisoformat(pr_data['created_on'].replace('Z', '+00:00'))
    updated_on = datetime.fromisoformat(pr_data['updated_on'].replace('Z', '+00:00'))

    # Use the latest date between created_on and updated_on
    latest_date = max(created_on, updated_on)

    # Convert the latest date to GMT +8 using the helper function
    latest_date_gmt8 = convert_utc_to_gmt8(latest_date)

    logging.info(f"Processing PR: {pr_id}, Title: {title}, Status: {status}, Date: {latest_date_gmt8}")

    try:
        # Fetch the PR diff from Bitbucket
        files_diff = get_files_diff(pr_id)
        processed_diff = process_files_diff(files_diff)

        # Example LLM analysis (optional)
        prompt_file_path = os.path.join(os.path.dirname(__file__), 'prompttext')
        with open(prompt_file_path, 'r') as file:
            prompt_text = file.read().strip()
        feedback = analyze_code_with_llm(prompt_text, processed_diff)

        # Insert the fetched PR data into the PostgreSQL database
        new_pr_diff = PR(
            pr_id=pr_id,
            title=title,
            status=status,  # Now fetching status from 'state' field in the main body
            sourceBranchName=source_branch,
            targetBranchName=target_branch,
            content=processed_diff,
            feedback=feedback,
            date_created=latest_date_gmt8  # Use the latest date converted to GMT +8
        )
        db.session.add(new_pr_diff)
        db.session.commit()

        return jsonify({'status': 'success', 'message': 'Pull request processed and saved successfully'}), 200
    except FileNotFoundError:
        logging.error(f"Prompt file not found: {prompt_file_path}")
        return jsonify({'error': 'Prompt file not found'}), 404
    except Exception as e:
        logging.error(f"Error processing pull request: {e}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@main.route('/api/summary', methods=['GET'])
def summary():
    try:
        numEntriesToDisplay = int(os.getenv("NUMENTRIESTODISPLAY", 15))  # Display 15 by default
        
        # Query the latest entries, ordered by date_created in descending order
        latest_entries = PR.query.order_by(PR.date_created.desc()).limit(numEntriesToDisplay).all()
        
        # Build the response while handling None values for date_created
        entries = []
        for entry in latest_entries:
            # Retrieve created_on and updated_on fields from the entry
            created_on = entry.date_created  # Assuming date_created stores the latest date already

            # Convert to GMT +8 timezone using the helper function
            date_gmt8 = convert_utc_to_gmt8(created_on) if created_on else None

            entries.append({
                'title': entry.title,
                'status': entry.status,
                'pr_id': entry.pr_id,
                'sourceBranchName': entry.sourceBranchName,
                'targetBranchName': entry.targetBranchName,
                'content': entry.content,
                'feedback': entry.feedback,
                'date_created': date_gmt8.isoformat() if date_gmt8 else None  # Handle None here
            })
        # Log the entries for debugging purposes
        logging.info(f"Entries: {entries}")
        
        return jsonify({'entries': entries}), 200
    except Exception as e:
        logging.error(f"Error fetching summary: {e}")
        logging.error(f"Error type: {type(e).__name__}")
        return jsonify({'error': 'Internal server error'}), 500

@main.route('/api/latest', methods=['GET'])
def latest():
    try:
        latest_entry = PR.query.order_by(PR.date_created.desc()).first()
        logging.error(latest_entry)
        if not latest_entry:
            return jsonify({'message': 'No entries found in the database.'}), 200

        # Convert date to GMT +8 using the helper function
        date_gmt8 = convert_utc_to_gmt8(latest_entry.date_created) if latest_entry.date_created else None

        return jsonify({'entry': {
            'title': latest_entry.title,
            'status': latest_entry.status,
            'pr_id': latest_entry.pr_id,
            'sourceBranchName': latest_entry.sourceBranchName,
            'targetBranchName': latest_entry.targetBranchName,
            'content': latest_entry.content,
            'feedback': latest_entry.feedback,
            'date_created': date_gmt8.isoformat() if date_gmt8 else None  # Convert to GMT +8
        }}), 200
    except Exception as e:
        logging.error(f"Error fetching summary: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@main.route("/api/healthchecker", methods=["GET"])
def healthchecker():
    return {"status": "success", "message": "Integrate Flask Framework with Next.js"}

@main.route('/api/pr/<string:pr_id>', methods=['GET', 'POST'])
def pr_entry(pr_id):
    if request.method == 'GET':
        try:
            pr_entry = PR.query.filter_by(pr_id=pr_id).first()
            if pr_entry is None:
                return jsonify({'error': 'PR not found'}), 404

            # Fetch conversation history (if needed)
            conversations = Conversation.query.filter_by(pr_id=pr_id).order_by(Conversation.date_created.asc()).all()
            conversation_history = [{
                'id': conv.id,
                'message': conv.message,
                'date_created': convert_utc_to_gmt8(conv.date_created).isoformat() if conv.date_created else None  # Convert using utility function
            } for conv in conversations]

            # Convert PR date to GMT +8
            date_gmt8 = convert_utc_to_gmt8(pr_entry.date_created) if pr_entry.date_created else None

            pr_data = {
                'pr_id': pr_entry.pr_id,
                'title': pr_entry.title,
                'status': pr_entry.status,
                'sourceBranchName': pr_entry.sourceBranchName,
                'targetBranchName': pr_entry.targetBranchName,
                'content': pr_entry.content,
                'feedback': pr_entry.feedback,
                'conversation_history': conversation_history,
                'date_created': date_gmt8.isoformat() if date_gmt8 else None  # Convert using utility function
            }
            return jsonify(pr_data), 200
        except Exception as e:
            logging.error(f"Error fetching PR {pr_id}: {e}")
            return jsonify({'error': 'Internal server error'}), 500

    elif request.method == 'POST':  # Handle POST for querying the AI
        try:
            user_query = request.form.get('user_query')
            if not user_query:
                return jsonify({'error': 'No user query provided'}), 400

            # Load the prompt from the file
            prompt_file_path = os.path.join(os.path.dirname(__file__), 'furtherPrompt')
            if not os.path.exists(prompt_file_path):
                return jsonify({'error': 'Prompt file not found'}), 404
            
            with open(prompt_file_path, 'r') as file:
                prompt_text = file.read().strip()

            # Fetch the PR entry from the DB
            pr_entry = PR.query.filter_by(pr_id=pr_id).first()
            if pr_entry is None:
                return jsonify({'error': 'PR not found'}), 404

            # Create the AI prompt with PR details
            prompt_text += f"\nPull request contents: {pr_entry.content}\nYour previous feedback: {pr_entry.feedback}"
            new_feedback = queryLLM(prompt_text, user_query)

            # Update PR feedback in the database
            pr_entry.feedback = new_feedback
            db.session.commit()

            return jsonify({'status': 'success', 'feedback': new_feedback}), 200
        except FileNotFoundError:
            logging.error(f"Prompt file not found: {prompt_file_path}")
            return jsonify({'error': 'Prompt file not found'}), 404
        except Exception as e:
            logging.error(f"Error processing PR {pr_id}: {e}")
            db.session.rollback()
            return jsonify({'error': 'Internal server error'}), 500

<<<<<<< HEAD
=======
    if request.method == 'GET':
        try:
            pr_entry = PR.query.filter_by(pr_id=pr_id).first()
            if pr_entry is None:
                return jsonify({'error': 'PR not found'}), 404
            pr_data = {
                'pr_id': pr_entry.pr_id,
                'title': pr_entry.title,
                'status':pr_entry.status,
                'sourceBranchName': pr_entry.sourceBranchName,
                'targetBranchName': pr_entry.targetBranchName,
                'content': pr_entry.content,
                'feedback': pr_entry.feedback,
                'date_created': pr_entry.date_created.isoformat()
            }
            return jsonify(pr_data), 200
        except Exception as e:
            logging.error(f"Error fetching PR {pr_id}: {e}")
            return jsonify({'error': 'Internal server error'}), 500
    else: # POST new comment/qn to the AI
        user_query = request.form.get('user_query')
        prompt_file_path = os.path.join(os.path.dirname(__file__), 'furtherPrompt')
        # Get prompt and context (PR content and previous feedback) before querying
        with open(prompt_file_path, 'r') as file:
            prompt_text = file.read().strip()
        try:
            pr_entry = PR.query.filter_by(pr_id=pr_id).first()
            if pr_entry is None:
                return jsonify({'error': 'PR not found'}), 404
            prompt_text += "\nPull request contents: " + pr_entry.content + "\n Your previous feedback: " + pr_entry.feedback
            newFeedback = queryLLM(prompt_text, user_query)
            # TODO: Need to update PR entry in the DB
            return jsonify({'status': 'success', 'feedback': newFeedback}), 200
        except FileNotFoundError:
            logging.error(f"Prompt file not found: {prompt_file_path}")
            return jsonify({'error': 'Prompt file not found'}), 404
        except Exception as e:
            logging.error(f"Error fetching PR {pr_id}: {e}")
            return jsonify({'error': 'Internal server error'}), 500
        
#Capture latest feedback
>>>>>>> parent of 997dfac (Clean routes.py and add new column for role in Conversation table)
@main.route('/api/pr/<string:pr_id>/feedback', methods=['POST'])
def update_feedback(pr_id):
    data = request.json
    new_feedback = data.get('feedback')

    if not new_feedback:
        return jsonify({'status': 'error', 'message': 'No feedback provided'}), 400

    try:
        pr_entry = PR.query.filter_by(pr_id=pr_id).first()
        if not pr_entry:
            return jsonify({'status': 'error', 'message': 'PR not found'}), 404

        # Update the latest feedback in the PR table
        pr_entry.feedback = new_feedback
        db.session.commit()

        return jsonify({'status': 'success', 'message': 'Feedback updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error updating feedback: {e}")
        return jsonify({'error': 'Internal server error'}), 500
    
#maintain convo history
@main.route('/api/pr/<string:pr_id>/conversation', methods=['POST'])
def add_conversation(pr_id):
    data = request.json

    if 'message' not in data:
        return jsonify({'status': 'error', 'message': 'Message is missing'}), 400

    try:
        pr_entry = PR.query.filter_by(pr_id=pr_id).first()
        if not pr_entry:
            return jsonify({'status': 'error', 'message': 'PR not found'}), 404

        # Add a new conversation entry
        new_conversation = Conversation(
            pr_id=pr_id,
            message=data.get('message'),
<<<<<<< HEAD
<<<<<<< HEAD
            date_created=convert_utc_to_gmt8(datetime.utcnow())  # Use utility function to convert to GMT +8
=======
            date_created=datetime.now()  # Use current time
>>>>>>> parent of 997dfac (Clean routes.py and add new column for role in Conversation table)
=======
            date_created=datetime.now(),  # Use current time
            role = "User"
>>>>>>> parent of 346d1ac (Update implementation to save the roles in the chatbot conversation)
        )
        db.session.add(new_conversation)
        db.session.commit()

        return jsonify({'status': 'success', 'message': 'Conversation added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error adding conversation: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@main.route('/api/pr/<string:pr_id>/conversations', methods=['GET'])
def get_conversations(pr_id):
    try:
        conversations = Conversation.query.filter_by(pr_id=pr_id).order_by(Conversation.date_created.asc()).all()

        response = [{
            'id': conv.id,
            'message': conv.message,
            'date_created': convert_utc_to_gmt8(conv.date_created).isoformat() if conv.date_created else None  # Convert using utility function
        } for conv in conversations]

        return jsonify({'conversations': response}), 200
    except Exception as e:
        logging.error(f"Error fetching conversations: {e}")
        return jsonify({'error': 'Internal server error'}), 500

# Groq API interaction route
@main.route('/api/groq-response', methods=['POST'])
def groq_response():
    try:
        # Extract JSON data from the request
        data = request.json
        user_message = data.get('message')

        # Check if the message exists
        if not user_message:
            logging.error("No message provided by user")
            return jsonify({'error': 'No message provided'}), 400

        # Groq API key and model name from environment variables
        groq_api_key = os.getenv('GROQ_API_KEY')
        groq_model_name = os.getenv('GROQ_MODEL_NAME', 'llama3-8b-8192')  # Use environment variable with fallback
        
        if not groq_api_key:
            logging.error("GROQ_API_KEY missing in environment")
            return jsonify({'error': 'API key missing'}), 500

        # Groq API endpoint and request details
        groq_url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            'Authorization': f'Bearer {groq_api_key}',
            'Content-Type': 'application/json'
        }
<<<<<<< HEAD
        payload = {
            "model": groq_model_name,
=======

        # Load the prompt from the file
        prompt_file_path = os.path.join(os.path.dirname(__file__), 'groqPrompt')
        if not os.path.exists(prompt_file_path):
            return jsonify({'error': 'Prompt file not found'}), 404
        
        with open(prompt_file_path, 'r') as file:
            prompt_text = file.read().strip()

        pr_entry = PR.query.filter_by(pr_id=pr_id).first()
        if pr_entry is None:
            return jsonify({'error': 'PR not found'}), 404
        prompt_text += "\nPull request contents: " + pr_entry.content + "\nYour initial feedback of the pull request: " + pr_entry.initialFeedback + "\nConversation history between you and the user about the code and feedback:\n"

        pr_chat_history = [{
            'id': conv.id,
            'message': conv.message,
            'date_created': conv.date_created.isoformat()
        } for conv in Conversation.query.filter_by(pr_id=pr_id).order_by(Conversation.date_created.asc()).all()]

        pr_chat_history_str = ""
        for entry in pr_chat_history:
            entry_str = f"'id': {entry['id']}\n'message': '{entry['message']}'\n'date_created': '{entry['date_created']}'\n"
            pr_chat_history_str += entry_str + "\n" 
        prompt_text += pr_chat_history_str

        payload = {
            "model": "llama3-8b-8192",  # Confirm that this is the correct model
>>>>>>> parent of 997dfac (Clean routes.py and add new column for role in Conversation table)
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }

        # Make a POST request to Groq API
        logging.info(f"Sending message to Groq API: {user_message}")
        response = requests.post(groq_url, headers=headers, json=payload)

        # Check for successful response from Groq API
        if response.status_code == 200:
            response_data = response.json()
            bot_response = response_data['choices'][0]['message']['content']
            logging.info(f"Received response from Groq API: {bot_response}")
            return jsonify({'response': bot_response}), 200
        else:
            error_message = f"Failed to get response from Groq API. Status code: {response.status_code}, Response: {response.text}"
            logging.error(error_message)
            return jsonify({'error': error_message}), response.status_code

    except Exception as e:
        error_message = f"Error in groq_response: {str(e)}"
        logging.error(error_message)
        return jsonify({'error': error_message}), 500