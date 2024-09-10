from flask import Blueprint, request, jsonify
from .models import PR
from .utils import get_files_diff, process_files_diff, analyze_code_with_llm
from .extensions import db
import os
import logging

main = Blueprint('main', __name__)

@main.route('/api/pr', methods=['POST'])
def handle_pr():
    data = request.json
    if 'pullrequest' not in data:
        return jsonify({'status': 'error', 'message': 'No pull request data found'}), 400

    pr_data = data['pullrequest']
    pr_id = pr_data['id']
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
        latest_entry = PR.query.order_by(PR.date_created.desc()).first()
        if not latest_entry:
            return jsonify({'message': 'No entries found in the database.'}), 404
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