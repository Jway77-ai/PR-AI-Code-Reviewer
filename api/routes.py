from flask import Blueprint, request, jsonify
from .models import PR
from .utils import get_files_diff, process_files_diff, analyze_code_with_llm, queryLLM
#from .extensions import db
from .index import db
import os
import logging
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

main = Blueprint('main', __name__)

@main.route('/api/pr', methods=['POST'])
def handle_pr():
    data = request.json
    if 'pullrequest' not in data:
        return jsonify({'status': 'error', 'message': 'No pull request data found'}), 400

    pr_data = data['pullrequest']
<<<<<<< HEAD
    pr_id = pr_data.get('id')
    title = pr_data.get('title', 'No Title') 
=======
    pr_id = pr_data['id']
>>>>>>> parent of c57bc78 (Backend - Added Title)
    source_branch = pr_data['source']['branch']['name']
    target_branch = pr_data['destination']['branch']['name']
    
    try:
        files_diff = get_files_diff(pr_id)
        files_diff = process_files_diff(files_diff)
        
        prompt_file_path = os.path.join(os.path.dirname(__file__), 'prompttext')
        with open(prompt_file_path, 'r') as file:
            prompt_text = file.read().strip()

        feedback = analyze_code_with_llm(prompt_text, files_diff)

        new_pr_diff = PR(pr_id=pr_id, sourceBranchName=source_branch, targetBranchName=target_branch, content=files_diff, feedback=feedback)
        db.session.add(new_pr_diff)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Pull request processed successfully'}), 200
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
        numEntriesToDisplay = int(os.getenv("NUMENTRIESTODISPLAY", 15))
        latest_entries = PR.query.order_by(PR.date_created.desc()).limit(numEntriesToDisplay).all()

        if not latest_entries:
            logging.info("No entries found in the database.")

        entries = [{
            'id': entry.id,
            'pr_id': entry.pr_id,
            'sourceBranchName': entry.sourceBranchName,
            'targetBranchName': entry.targetBranchName,
            'content': entry.content,
            'feedback': entry.feedback,
            'date_created': entry.date_created.isoformat()
        } for entry in latest_entries]

        logging.info(f"Fetched {len(entries)} entries from the database.")
        return jsonify({'entries': entries}), 200
    except Exception as e:
        logging.error(f"Error fetching summary: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@main.route('/api/latest', methods=['GET'])
def latest():
    try:
        latest_entry = PR.query.order_by(PR.date_created.desc()).first()
        logging.error(latest_entry)
        if not latest_entry:
            return jsonify({'message': 'No entries found in the database.'}), 200
        return jsonify({'entry': {
            'id': latest_entry.id,
            'pr_id': latest_entry.pr_id,
            'sourceBranchName': latest_entry.sourceBranchName,
            'targetBranchName': latest_entry.targetBranchName,
            'content': latest_entry.content,
            'feedback': latest_entry.feedback,
            'date_created': latest_entry.date_created.isoformat()
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
            pr_data = {
                'id': pr_entry.id,
                'pr_id': pr_entry.pr_id,
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