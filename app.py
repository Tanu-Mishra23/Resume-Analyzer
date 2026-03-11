from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import os
import uuid
from werkzeug.utils import secure_filename
from resume_parser import ResumeParser
from job_matcher import JobMatcher

import spacy
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    """Check if the file has an allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Home page with upload form"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    """Handle resume upload and processing"""
    try:
        # Check if file was uploaded
        if 'resume' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['resume']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only PDF files are allowed'}), 400
        
        # Generate unique filename
        filename = str(uuid.uuid4()) + '.pdf'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save file
        file.save(filepath)
        
        # Parse resume
        parser = ResumeParser()
        result = parser.parse_resume(filepath)
        
        if 'error' in result:
            return jsonify(result), 400
        
        # Find matching jobs
        matcher = JobMatcher()
        matching_jobs = matcher.find_matching_jobs(result['skills'])
        
        # Store results in session
        session['analysis_result'] = result
        session['matching_jobs'] = matching_jobs
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except:
            pass  # Ignore cleanup errors
        
        return jsonify({
            'success': True,
            'redirect': url_for('show_results')
        })
        
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/result')
def show_results():
    """Show analysis results"""
    # Get results from session
    analysis_result = session.get('analysis_result')
    matching_jobs = session.get('matching_jobs')
    
    if not analysis_result:
        return redirect(url_for('index'))
    
    return render_template('result.html', 
                         analysis_result=analysis_result,
                         matching_jobs=matching_jobs)

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for programmatic access"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text']
        
        # Parse text directly (without PDF)
        parser = ResumeParser()
        skills = parser.extract_skills(text)
        score = parser.calculate_resume_score(text, skills)
        suggestions = parser.generate_suggestions(text, skills)
        
        result = {
            'skills': skills,
            'score': score,
            'suggestions': suggestions
        }
        
        # Find matching jobs if requested
        if data.get('include_jobs', False):
            matcher = JobMatcher()
            matching_jobs = matcher.find_matching_jobs(skills)
            result['matching_jobs'] = matching_jobs
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({'error': 'File too large. Maximum size is 16MB'}), 413

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    print("Starting AI Resume Analyzer...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
