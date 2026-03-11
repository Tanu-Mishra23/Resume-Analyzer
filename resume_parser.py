import PyPDF2
import re
from typing import List, Dict, Tuple

class ResumeParser:
    """
    A class to parse PDF resumes and extract skills using NLP techniques.
    """
    
    def __init__(self):
        # Common tech skills to look for in resumes
        self.tech_skills = [
            'Python', 'Java', 'JavaScript', 'SQL', 'Machine Learning', 'React', 
            'Node.js', 'Data Analysis', 'HTML', 'CSS', 'Flask', 'Django', 
            'MongoDB', 'PostgreSQL', 'AWS', 'Docker', 'Git', 'GitHub',
            'TensorFlow', 'PyTorch', 'Angular', 'Vue.js', 'TypeScript',
            'REST API', 'GraphQL', 'DevOps', 'Kubernetes', 'Jenkins',
            'Agile', 'Scrum', 'JIRA', 'Linux', 'Ubuntu', 'Windows',
            'Microsoft Office', 'Excel', 'PowerPoint', 'Tableau', 'Power BI',
            'C++', 'C#', '.NET', 'PHP', 'Ruby', 'Rails', 'Swift', 'Kotlin'
        ]
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from a PDF file.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            str: Extracted text from the PDF
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""

                for page in pdf_reader.pages:
                    page_text = page.extract_text()
    
                    if page_text:   # prevent None error
                        text += page_text + " "
                        
                return text
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return ""
    
    def extract_skills(self, text: str) -> List[str]:
        """
        Extract technical skills from resume text.
        
        Args:
            text (str): Resume text
            
        Returns:
            List[str]: List of found skills
        """
        found_skills = []
        text_lower = text.lower()
        
        for skill in self.tech_skills:
            # Check for exact skill match (case insensitive)
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        return list(set(found_skills))  # Remove duplicates
    
    def calculate_resume_score(self, text: str, skills: List[str]) -> int:
        """
        Calculate a resume score based on various factors.
        
        Args:
            text (str): Resume text
            skills (List[str]): Extracted skills
            
        Returns:
            int: Resume score (0-100)
        """
        score = 0
        
        # Base score for having skills
        score += min(len(skills) * 5, 30)  # Max 30 points for skills
        
        # Check for important sections
        sections = ['education', 'experience', 'project', 'skill', 'achievement']
        for section in sections:
            if section in text.lower():
                score += 10  # 10 points for each important section
        
        # Check for contact information
        if '@' in text and ('.com' in text or '.edu' in text):
            score += 10  # 10 points for email
        
        if re.search(r'\d{10}', text.replace(' ', '').replace('-', '')):
            score += 10  # 10 points for phone number
        
        # Length bonus (longer resumes might have more content)
        if len(text) > 500:
            score += 10
        elif len(text) > 1000:
            score += 20
        
        return min(score, 100)
    
    def generate_suggestions(self, text: str, skills: List[str]) -> List[str]:
        """
        Generate improvement suggestions for the resume.
        
        Args:
            text (str): Resume text
            skills (List[str]): Extracted skills
            
        Returns:
            List[str]: List of suggestions
        """
        suggestions = []
        
        # Check for missing important sections
        sections = ['education', 'experience', 'project', 'skill', 'achievement']
        for section in sections:
            if section not in text.lower():
                suggestions.append(f"Add {section.title()} section to your resume")
        
        # Check for GitHub profile
        if 'github' not in text.lower():
            suggestions.append("Include GitHub profile link")
        
        # Check for LinkedIn
        if 'linkedin' not in text.lower():
            suggestions.append("Add LinkedIn profile link")
        
        # Check for quantifiable achievements
        if not re.search(r'\d+%|\d+\s*(years?|months?)|increased|decreased|improved', text.lower()):
            suggestions.append("Add measurable achievements with numbers and percentages")
        
        # Check skills count
        if len(skills) < 5:
            suggestions.append("Add more technical skills to showcase your expertise")
        
        # Check for project descriptions
        if 'project' not in text.lower():
            suggestions.append("Add project descriptions to demonstrate practical experience")
        
        return suggestions
    
    def parse_resume(self, pdf_path: str) -> Dict:
        """
        Main method to parse resume and return analysis.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            Dict: Dictionary containing analysis results
        """
        # Extract text from PDF
        text = self.extract_text_from_pdf(pdf_path)
        
        if not text:
            return {
                'error': 'Could not extract text from PDF',
                'skills': [],
                'score': 0,
                'suggestions': ['Please upload a valid PDF resume']
            }
        
        # Extract skills
        skills = self.extract_skills(text)
        
        # Calculate score
        score = self.calculate_resume_score(text, skills)
        
        # Generate suggestions
        suggestions = self.generate_suggestions(text, skills)
        
        return {
            'text': text,
            'skills': skills,
            'score': score,
            'suggestions': suggestions
        }
