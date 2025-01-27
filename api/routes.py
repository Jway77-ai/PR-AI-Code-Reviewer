from datetime import datetime
from flask import Blueprint, request, jsonify
from groq import Groq
from .models import PR, Conversation
from .utils import get_all_prs_from_repo, get_files_diff, process_files_diff, analyze_code_with_llm, queryLLM, handle_date, get_raw_files_diff, process_pr
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
        if 'values' not in pr_list:
            return jsonify({'status': 'error', 'message': 'No PRs found'}), 400

        for pr_data in pr_list['values']:
            pr_id = str(pr_data.get('id'))  # Cast the PR ID to a string
            title = pr_data.get('title', 'No Title')
            status = pr_data.get('state')
            source_branch = pr_data['source']['branch']['name']
            target_branch = pr_data['destination']['branch']['name']
            lastCommitHash = pr_data['source']['commit']['hash']
            created_date = handle_date(pr_data.get('created_on'))
            last_modified = handle_date(pr_data.get('updated_on'))

            # Check if the PR already exists in the database
            existing_pr = PR.query.filter_by(pr_id=pr_id).first()
            if existing_pr:
                # Update existing PR with new information
                existing_pr.title = title
                existing_pr.status = status
                existing_pr.sourceBranchName = source_branch
                existing_pr.targetBranchName = target_branch
                existing_pr.last_modified = last_modified
                existing_pr.lastCommitHash = lastCommitHash
                db.session.add(existing_pr)
            else:
                # Process PR diff and feedback for new PRs
                raw_files_diff = get_raw_files_diff(pr_id)
                files_diff = get_files_diff(pr_id)
                processed_diff = process_files_diff(files_diff)
                prompt_file_path = os.path.join(os.path.dirname(__file__), 'prompttext')
                with open(prompt_file_path, 'r') as file:
                    prompt_text = file.read().strip()
                feedback = analyze_code_with_llm(prompt_text, processed_diff)

                # Insert new PR data
                new_pr_diff = PR(
                    pr_id=pr_id,
                    title=title,
                    status=status,
                    sourceBranchName=source_branch,
                    targetBranchName=target_branch,
                    lastCommitHash=lastCommitHash,
                    rawDiff = raw_files_diff,
                    content=processed_diff,
                    initialFeedback=feedback,
                    feedback=feedback,
                    created_date=created_date,
                    last_modified=last_modified
                )
                db.session.add(new_pr_diff)

            db.session.commit()

        return jsonify({'status': 'success', 'message': 'All PRs synced and saved successfully'}), 200
    except Exception as e:
        logging.error(f"Error syncing PRs: {e}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

# Api to receive payload from Bitbucket webhook for new PRs or updates to the PR
@main.route('/api/pr', methods=['POST'])
def handle_pr():
    data = request.json
    if 'pullrequest' not in data:
        return jsonify({'status': 'error', 'message': 'Pull request data not found'}), 400

    pr_data = data.get('pullrequest')
    pr_id = str(pr_data.get('id'))
    created_date = handle_date(pr_data.get('created_on'), to_sgt=True)
    updated_date = handle_date(pr_data.get('updated_on'), to_sgt=True)

    # Update the PR entry if this pr_id already exists
    pr_entry = PR.query.filter_by(pr_id=pr_id).first()
    if pr_entry:
        pr_entry.title = pr_data.get('title', 'No Title')
        pr_entry.status = pr_data['state']
        pr_entry.last_modified = updated_date
        if pr_entry.lastCommitHash != pr_data['source']['commit']['hash']:
            pr_entry.rawDiff, pr_entry.content, pr_entry.feedback = process_pr(pr_id, pr_entry.targetBranchName)
            pr_entry.lastCommitHash = pr_data['source']['commit']['hash']
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Pull request status updated successfully'}), 200
    else:
        target_branch = pr_data['destination']['branch']['name']
        logging.info(f"Processing PR: {pr_id}, Title: {pr_data.get('title', 'No Title')}, Status: {pr_data['state']}")
        try:
            raw_files_diff, processed_diff, feedback = process_pr(pr_id, target_branch)
            # Insert the fetched PR data into the PostgreSQL database
            new_pr_diff = PR(
                pr_id=pr_id,
                title=pr_data.get('title', 'No Title'),
                status=pr_data['state'], 
                sourceBranchName=pr_data['source']['branch']['name'],
                targetBranchName=pr_data['destination']['branch']['name'],
                lastCommitHash=pr_data['source']['commit']['hash'],
                rawDiff = raw_files_diff,
                content=processed_diff,
                initialFeedback=feedback,
                feedback=feedback,
                created_date=created_date,
                last_modified=updated_date
            )
            db.session.add(new_pr_diff)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Pull request processed and saved successfully'}), 200
        except Exception as e:
            logging.error(f"Error processing pull request: {e}")
            db.session.rollback()
            return jsonify({'error': 'Internal server error'}), 500

@main.route('/api/summary', methods=['GET'])
def summary():
    try:
        numEntriesToDisplay = int(os.getenv("NUMENTRIESTODISPLAY", 15))  # Display 15 by default
        
        # Query the latest entries, ordered by date_created in descending order
        latest_entries = PR.query.order_by(PR.last_modified.desc()).limit(numEntriesToDisplay).all()
        
        # Build the response while handling None values for date_created
        entries = []
        for entry in latest_entries:
            entries.append({
                'title': entry.title,
                'status':entry.status,
                'pr_id': entry.pr_id,
                'sourceBranchName': entry.sourceBranchName,
                'targetBranchName': entry.targetBranchName,
                'lastCommitHash': entry.lastCommitHash,
                'content': entry.content,
                'initialFeedback': entry.initialFeedback,
                'created_date': handle_date(entry.created_date, to_sgt=True, as_string=True),
                'last_modified': handle_date(entry.last_modified, to_sgt=True, as_string=True)
            })
        # Log the entries for debugging purposes
        logging.info(f"Entries: {entries}")
        
        return jsonify({'entries': entries}), 200
    except Exception as e:
        logging.error(f"Error fetching summary: {e}")
        logging.error(f"Error type: {type(e).__name__}")
        return jsonify({'error': 'Internal server error'}), 500

@main.route('/api/pr/<string:pr_id>', methods=['GET'])
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
                'date_created': conv.date_created.isoformat()
            } for conv in conversations]
            logging.info(f"Rawdiff: {pr_entry.rawDiff}")
            pr_data = {
                'pr_id': pr_entry.pr_id,
                'title': pr_entry.title,
                'status': pr_entry.status,
                'sourceBranchName': pr_entry.sourceBranchName,
                'targetBranchName': pr_entry.targetBranchName,
                'lastCommitHash': pr_entry.lastCommitHash,
                'rawDiff' : pr_entry.rawDiff,
                'content': pr_entry.content,
                'initialFeedback': pr_entry.initialFeedback,
                'feedback': pr_entry.feedback,
                'conversation_history': conversation_history,
                'created_date': handle_date(pr_entry.created_date, to_sgt=True, as_string=True),
                'last_modified': handle_date(pr_entry.last_modified, to_sgt=True, as_string=True)
            }
            return jsonify(pr_data), 200
        except Exception as e:
            logging.error(f"Error fetching PR {pr_id}: {e}")
            return jsonify({'error': 'Internal server error'}), 500
        
# Maintain convo history
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
            date_created=datetime.now(),  # Use current time
            role = data.get('role', 'User')
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
            'role': conv.role,
            'message': conv.message,
            'date_created': conv.date_created.isoformat()
        } for conv in conversations]

        return jsonify({'conversations': response}), 200
    except Exception as e:
        logging.error(f"Error fetching conversations: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@main.route('/api/pr/<string:pr_id>/content', methods=['GET'])
def get_content(pr_id):
    try:
        pr_entry = PR.query.filter_by(pr_id=pr_id).first()
        if pr_entry is None:
            return jsonify({'error': 'PR not found'}), 404
        return jsonify({'contents': pr_entry.content}), 200
    except Exception as e:
        logging.error(f"Error fetching PR contents {pr_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@main.route('/api/pr/<string:pr_id>/feedback', methods=['GET'])
def get_feedback(pr_id):
    try:
        pr_entry = PR.query.filter_by(pr_id=pr_id).first()
        if pr_entry is None:
            return jsonify({'error': 'PR not found'}), 404
        return jsonify({'contents': pr_entry.feedback}), 200
    except Exception as e:
        logging.error(f"Error fetching PR contents {pr_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 

# Groq API interaction route
@main.route('/api/pr/<string:pr_id>/groq-response', methods=['POST'])
def groq_response(pr_id):
    try:
        # Extract JSON data from the request
        data = request.json
        user_message = data.get('message')

        # Check if the message exists
        if not user_message:
            logging.error("No message provided by user")
            return jsonify({'error': 'No message provided'}), 400

        # Groq API key from environment variables
        groq_api_key = os.getenv('GROQ_API_KEY')
        if not groq_api_key:
            logging.error("GROQ_API_KEY missing in environment")
            return jsonify({'error': 'API key missing'}), 500

        # Groq API endpoint and request details
        groq_url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            'Authorization': f'Bearer {groq_api_key}',
            'Content-Type': 'application/json'
        }

        # Load the prompt from the file
        prompt_file_path = os.path.join(os.path.dirname(__file__), 'groqPrompt')
        if not os.path.exists(prompt_file_path):
            return jsonify({'error': 'Prompt file not found'}), 404
        
        with open(prompt_file_path, 'r') as file:
            prompt_text = file.read().strip()

        pr_entry = PR.query.filter_by(pr_id=pr_id).first()
        if pr_entry is None:
            return jsonify({'error': 'PR not found'}), 404
        if not pr_entry.initialFeedback:
            pr_entry.initialFeedback = pr_entry.feedback
        prompt_text += "\nPull request contents: " + pr_entry.content + "\nYour initial feedback of the pull request: " + pr_entry.initialFeedback + "\nConversation history between you and the user about the code and feedback:\n"

        # Retrieve all messages related to this pr_id
        pr_chat_history = [{
            'role': conv.role,
            'message': conv.message,
            'date_created': conv.date_created.isoformat()
        } for conv in sorted(pr_entry.convo, key=lambda x: x.date_created)]
        
        # Convert chat history to string and append to prompt
        pr_chat_history_str = ""
        for entry in pr_chat_history:
            entry_str = f"'Role': {entry['role']}\n'Message': '{entry['message']}'\n'Date_created': '{entry['date_created']}'\n"
            pr_chat_history_str += entry_str + "\n" 
        prompt_text += pr_chat_history_str

        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": prompt_text},
                {"role": "user", "content": user_message}
            ]
        }

        # Make a POST request to Groq API
        logging.info(f"Sending message to Groq API: {user_message}")
        response = requests.post(groq_url, headers=headers, json=payload)

        # Check for successful response from Groq API
        if response.status_code == 200:
            bot_response = response.json().get('choices', [])[0]['message']['content']
            logging.info(f"Received response from Groq API: {bot_response}")
            return jsonify({'response': bot_response}), 200
        else:
            logging.error(f"Failed to get response from Groq API, status code: {response.status_code}, response: {response.text}")
            return jsonify({'error': 'Failed to get response from Groq API'}), 500

    except Exception as e:
        logging.error(f"Error in groq_response: {e}")
        return jsonify({'error': str(e)}), 500
