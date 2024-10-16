from flask import Flask, request, jsonify, send_from_directory
import subprocess
import os
import requests

app = Flask(__name__)

UPLOAD_FOLDER = './pdf_files_to_parse'
OUTPUT_FOLDER = './output_files'
GITHUB_REPO = "benjisho/pdf-parser"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Store the GitHub token in an environment variable for security

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return "PDF Parser API is running. Use /upload to upload a PDF file."

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdfFile' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['pdfFile']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Trigger GitHub Actions to parse the PDF
        github_api_url = f"https://api.github.com/repos/{GITHUB_REPO}/dispatches"
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {GITHUB_TOKEN}"
        }
        payload = {
            "event_type": "parse_pdf"
        }

        response = requests.post(github_api_url, headers=headers, json=payload)
        if response.status_code != 204:
            return jsonify({"error": "Failed to trigger GitHub Actions"}), 500

        return jsonify({"message": "PDF uploaded and parsing triggered successfully"}), 200

@app.route('/output/<filename>', methods=['GET'])
def download_file(filename):
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    if os.path.exists(output_path):
        return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)
    else:
        return jsonify({"error": "Output file not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)