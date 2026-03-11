from typing import List, Dict, Tuple

class JobMatcher:
    """
    A class to match resume skills with job requirements and calculate match scores.
    """
    
    def __init__(self):
        # Job database with required skills
        self.jobs = [
            {
                'title': 'Data Scientist',
                'company': 'Tech Corp',
                'skills': ['Python', 'Machine Learning', 'SQL', 'Data Analysis', 'TensorFlow'],
                'description': 'Analyze complex data and build machine learning models',
                'salary_range': '$80k - $120k'
            },
            {
                'title': 'Backend Developer',
                'company': 'Web Solutions Inc',
                'skills': ['Python', 'Flask', 'SQL', 'REST API', 'Docker'],
                'description': 'Develop and maintain server-side applications',
                'salary_range': '$70k - $100k'
            },
            {
                'title': 'Frontend Developer',
                'company': 'Digital Agency',
                'skills': ['JavaScript', 'React', 'HTML', 'CSS', 'TypeScript'],
                'description': 'Create beautiful and responsive user interfaces',
                'salary_range': '$65k - $95k'
            },
            {
                'title': 'Full Stack Developer',
                'company': 'Startup Hub',
                'skills': ['Python', 'JavaScript', 'React', 'Node.js', 'SQL', 'HTML', 'CSS'],
                'description': 'Work on both frontend and backend development',
                'salary_range': '$85k - $130k'
            },
            {
                'title': 'Machine Learning Engineer',
                'company': 'AI Innovations',
                'skills': ['Python', 'Machine Learning', 'TensorFlow', 'PyTorch', 'Data Analysis'],
                'description': 'Design and implement machine learning systems',
                'salary_range': '$90k - $140k'
            },
            {
                'title': 'DevOps Engineer',
                'company': 'Cloud Systems',
                'skills': ['Docker', 'Kubernetes', 'AWS', 'Linux', 'Jenkins', 'Git'],
                'description': 'Manage deployment pipelines and infrastructure',
                'salary_range': '$75k - $115k'
            },
            {
                'title': 'Software Engineer',
                'company': 'Enterprise Tech',
                'skills': ['Python', 'Java', 'SQL', 'Git', 'REST API'],
                'description': 'Develop scalable software solutions',
                'salary_range': '$70k - $110k'
            },
            {
                'title': 'Data Analyst',
                'company': 'Analytics Pro',
                'skills': ['Python', 'SQL', 'Data Analysis', 'Excel', 'Tableau'],
                'description': 'Analyze data and create business insights',
                'salary_range': '$60k - $90k'
            },
            {
                'title': 'Web Developer',
                'company': 'Creative Studio',
                'skills': ['HTML', 'CSS', 'JavaScript', 'React', 'Node.js'],
                'description': 'Build modern web applications',
                'salary_range': '$55k - $85k'
            },
            {
                'title': 'Python Developer',
                'company': 'Python Solutions',
                'skills': ['Python', 'Django', 'Flask', 'SQL', 'REST API'],
                'description': 'Develop Python-based applications and APIs',
                'salary_range': '$65k - $100k'
            }
        ]
    
    def calculate_match_score(self, resume_skills: List[str], job_skills: List[str]) -> int:
        """
        Calculate match score between resume skills and job requirements.
        
        Args:
            resume_skills (List[str]): Skills extracted from resume
            job_skills (List[str]): Skills required for the job
            
        Returns:
            int: Match score (0-100)
        """
        if not job_skills:
            return 0
        
        # Count matching skills (case insensitive)
        resume_skills_lower = [skill.lower() for skill in resume_skills]
        job_skills_lower = [skill.lower() for skill in job_skills]
        
        matching_skills = 0
        for job_skill in job_skills_lower:
            if job_skill in resume_skills_lower:
                matching_skills += 1
        
        # Calculate percentage
        match_score = (matching_skills / len(job_skills)) * 100
        return round(match_score)
    
    def find_matching_jobs(self, resume_skills: List[str], top_n: int = 3) -> List[Dict]:
        """
        Find top matching jobs based on resume skills.
        
        Args:
            resume_skills (List[str]): Skills extracted from resume
            top_n (int): Number of top jobs to return
            
        Returns:
            List[Dict]: List of matching jobs with scores
        """
        job_matches = []
        
        for job in self.jobs:
            match_score = self.calculate_match_score(resume_skills, job['skills'])
            
            # Find which skills match
            resume_skills_lower = [skill.lower() for skill in resume_skills]
            job_skills_lower = [skill.lower() for skill in job['skills']]
            
            matching_skills = []
            for job_skill in job_skills_lower:
                if job_skill in resume_skills_lower:
                    # Find the original case version
                    original_skill = next((skill for skill in resume_skills if skill.lower() == job_skill), job_skill)
                    matching_skills.append(original_skill)
            
            job_matches.append({
                'title': job['title'],
                'company': job['company'],
                'skills': job['skills'],
                'description': job['description'],
                'salary_range': job['salary_range'],
                'match_score': match_score,
                'matching_skills': matching_skills,
                'missing_skills': [skill for skill in job['skills'] if skill.lower() not in resume_skills_lower]
            })
        
        # Sort by match score (descending) and return top N
        job_matches.sort(key=lambda x: x['match_score'], reverse=True)
        return job_matches[:top_n]
    
    def get_all_jobs(self) -> List[Dict]:
        """
        Get all available jobs.
        
        Returns:
            List[Dict]: List of all jobs
        """
        return self.jobs
    
    def add_job(self, job: Dict) -> None:
        """
        Add a new job to the database.
        
        Args:
            job (Dict): Job information
        """
        required_fields = ['title', 'company', 'skills', 'description', 'salary_range']
        if all(field in job for field in required_fields):
            self.jobs.append(job)
        else:
            print("Job missing required fields")
