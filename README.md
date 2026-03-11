# AI Resume Analyzer & Job Matcher

A beginner-friendly web application that analyzes resumes using AI and matches users with suitable jobs based on their skills.

## Project Goal

This application allows users to upload their resume (PDF) and receive:
- AI-powered skill extraction
- Resume scoring (0-100)
- Improvement suggestions
- Job matching based on extracted skills

## Technology Stack

### Frontend
- HTML5
- CSS3 (with modern styling)
- Vanilla JavaScript

### Backend
- Python 3.7+
- Flask (web framework)

### AI / NLP
- PyPDF2 (PDF text extraction)
- Custom skill extraction algorithms

### Other Libraries
- gunicorn (production server)

## Project Structure

```
resume-ai-project/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── resume_parser.py       # Resume parsing and skill extraction
├── job_matcher.py         # Job matching logic
├── README.md             # This file
├── templates/            # HTML templates
│   ├── index.html        # Home page with upload form
│   └── result.html       # Results page
├── static/               # Static assets
│   ├── style.css         # CSS styling
│   └── script.js         # JavaScript frontend logic
└── uploads/              # Temporary file uploads
```

## Features

### 1. Resume Upload
- Clean, user-friendly interface
- Drag-and-drop support
- File validation (PDF only, max 16MB)

### 2. AI Analysis
- **Skill Extraction**: Automatically detects technical skills from resume text
- **Resume Scoring**: Calculates a score (0-100) based on various factors
- **Improvement Suggestions**: Provides actionable tips to enhance the resume

### 3. Job Matching
- Matches extracted skills with job requirements
- Calculates match percentages
- Shows top 3 matching jobs with detailed information

### 4. Modern UI
- Responsive design for all devices
- Beautiful gradient styling
- Smooth animations and transitions
- Progress indicators

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or download the project**
   ```bash
   # If using git
   git clone <repository-url>
   cd resume-ai-project
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create required directories**
   ```bash
   mkdir uploads
   mkdir templates
   mkdir static
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open in browser**
   Navigate to `http://localhost:5000`

## Usage

1. **Upload Resume**
   - Click "Choose PDF File" or drag and drop your resume
   - Supported format: PDF only
   - Maximum file size: 16MB

2. **View Analysis**
   - Resume score (0-100)
   - Extracted technical skills
   - Improvement suggestions

3. **Job Matches**
   - Top 3 matching jobs
   - Match percentage for each job
   - Required skills vs. your skills

## API Endpoints

### Web Interface
- `GET /` - Home page with upload form
- `POST /upload` - Process resume upload
- `GET /result` - Display analysis results

### API Endpoint
- `POST /api/analyze` - Programmatic resume analysis
  ```json
  {
    "text": "resume text content",
    "include_jobs": true
  }
  ```

## Skill Detection

The system detects these common technical skills:
- **Programming Languages**: Python, Java, JavaScript, C++, C#, PHP, Ruby
- **Web Technologies**: HTML, CSS, React, Angular, Vue.js, Node.js
- **Databases**: SQL, MongoDB, PostgreSQL
- **Cloud/DevOps**: AWS, Docker, Kubernetes, Jenkins
- **Data Science**: Machine Learning, TensorFlow, PyTorch, Data Analysis
- **Tools**: Git, GitHub, Linux, JIRA

## Job Database

The application includes 10 pre-defined jobs:
1. Data Scientist
2. Backend Developer  
3. Frontend Developer
4. Full Stack Developer
5. Machine Learning Engineer
6. DevOps Engineer
7. Software Engineer
8. Data Analyst
9. Web Developer
10. Python Developer

## Customization

### Adding New Skills
Edit `resume_parser.py` and add skills to the `tech_skills` list.

### Adding New Jobs
Edit `job_matcher.py` and add new job objects to the `jobs` list.

### Modifying Scoring Algorithm
Update the `calculate_resume_score` method in `resume_parser.py`.

## Production Deployment

For production use:

1. **Use a production server**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Environment variables**
   - Set `FLASK_ENV=production`
   - Change the secret key in `app.py`

3. **Security considerations**
   - Add file type validation
   - Implement rate limiting
   - Add HTTPS support

## Troubleshooting

### Common Issues

1. **PDF not parsing correctly**
   - Ensure the PDF contains text (not scanned images)
   - Try a different PDF converter if needed

2. **No skills detected**
   - Check if skills are clearly listed in the resume
   - Verify skill spelling matches the predefined list

3. **Server errors**
   - Check if all dependencies are installed
   - Verify file permissions for uploads directory

### Debug Mode
Run with debug mode enabled:
```bash
export FLASK_DEBUG=1  # On Windows: set FLASK_DEBUG=1
python app.py
```

## Contributing

This project is designed to be beginner-friendly. Feel free to:
- Add new features
- Improve the UI
- Expand the job database
- Enhance the skill extraction algorithm

## License

This project is open source and available under the MIT License.

## Support

If you encounter any issues or have questions:
1. Check the troubleshooting section
2. Review the code comments
3. Test with different resume formats

---

**Happy Resume Analyzing! 🚀**