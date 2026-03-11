// DOM Elements
const uploadForm = document.getElementById('uploadForm');
const resumeFile = document.getElementById('resumeFile');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.querySelector('.file-name');
const uploadBtn = document.getElementById('uploadBtn');
const btnText = document.querySelector('.btn-text');
const btnLoader = document.querySelector('.btn-loader');
const errorMessage = document.getElementById('errorMessage');
const errorText = document.querySelector('.error-text');

// File validation
const MAX_FILE_SIZE = 16 * 1024 * 1024; // 16MB
const ALLOWED_TYPES = ['application/pdf'];

// Event Listeners
resumeFile.addEventListener('change', handleFileSelect);
uploadForm.addEventListener('submit', handleUpload);

// Handle file selection
function handleFileSelect(event) {
    const file = event.target.files[0];
    
    if (!file) {
        resetFileInput();
        return;
    }
    
    // Validate file type
    if (!ALLOWED_TYPES.includes(file.type)) {
        showError('Please upload a PDF file only.');
        resetFileInput();
        return;
    }
    
    // Validate file size
    if (file.size > MAX_FILE_SIZE) {
        showError('File size must be less than 16MB.');
        resetFileInput();
        return;
    }
    
    // Show file info
    fileName.textContent = file.name;
    fileInfo.style.display = 'flex';
    uploadBtn.disabled = false;
    hideError();
}

// Handle file upload
async function handleUpload(event) {
    event.preventDefault();
    
    const file = resumeFile.files[0];
    if (!file) {
        showError('Please select a file to upload.');
        return;
    }
    
    // Show loading state
    setLoadingState(true);
    hideError();
    
    // Create FormData
    const formData = new FormData();
    formData.append('resume', file);
    
    try {
        // Send upload request
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || 'Upload failed');
        }
        
        if (result.success && result.redirect) {
            // Redirect to results page
            window.location.href = result.redirect;
        } else {
            throw new Error('Invalid response from server');
        }
        
    } catch (error) {
        console.error('Upload error:', error);
        showError(error.message || 'An error occurred during upload. Please try again.');
        setLoadingState(false);
    }
}

// Remove selected file
function removeFile() {
    resetFileInput();
    hideError();
}

// Reset file input
function resetFileInput() {
    resumeFile.value = '';
    fileInfo.style.display = 'none';
    uploadBtn.disabled = true;
    fileName.textContent = '';
}

// Set loading state
function setLoadingState(loading) {
    if (loading) {
        uploadBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline-block';
    } else {
        uploadBtn.disabled = false;
        btnText.style.display = 'inline-block';
        btnLoader.style.display = 'none';
    }
}

// Show error message
function showError(message) {
    errorText.textContent = message;
    errorMessage.style.display = 'flex';
    
    // Auto-hide after 5 seconds
    setTimeout(hideError, 5000);
}

// Hide error message
function hideError() {
    errorMessage.style.display = 'none';
}

// Add drag and drop functionality
const uploadCard = document.querySelector('.upload-card');
const fileInputLabel = document.querySelector('.file-input-label');

// Prevent default drag behaviors
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    uploadCard.addEventListener(eventName, preventDefaults, false);
    document.body.addEventListener(eventName, preventDefaults, false);
});

// Highlight drop area when item is dragged over it
['dragenter', 'dragover'].forEach(eventName => {
    uploadCard.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
    uploadCard.addEventListener(eventName, unhighlight, false);
});

// Handle dropped files
uploadCard.addEventListener('drop', handleDrop, false);

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function highlight(e) {
    uploadCard.classList.add('drag-over');
}

function unhighlight(e) {
    uploadCard.classList.remove('drag-over');
}

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    
    if (files.length > 0) {
        resumeFile.files = files;
        handleFileSelect({ target: { files: files } });
    }
}

// Add drag-over styles
const style = document.createElement('style');
style.textContent = `
    .upload-card.drag-over {
        background: #f0f8ff;
        border: 2px dashed #667eea;
    }
    
    .upload-card.drag-over .file-input-label {
        background: #e8f5e8;
        border-color: #667eea;
    }
`;
document.head.appendChild(style);

// Add smooth scroll behavior
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add animation to feature cards on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe feature cards
document.querySelectorAll('.feature').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(card);
});

// Add keyboard navigation
document.addEventListener('keydown', function(e) {
    // Escape key closes error message
    if (e.key === 'Escape') {
        hideError();
    }
    
    // Enter key on file input label triggers file selection
    if (e.key === 'Enter' && document.activeElement === fileInputLabel) {
        e.preventDefault();
        resumeFile.click();
    }
});

// Add progress indicator for better UX
function createProgressIndicator() {
    const progress = document.createElement('div');
    progress.className = 'upload-progress';
    progress.innerHTML = `
        <div class="progress-bar">
            <div class="progress-fill"></div>
        </div>
        <div class="progress-text">Uploading...</div>
    `;
    
    // Add styles
    const progressStyles = document.createElement('style');
    progressStyles.textContent = `
        .upload-progress {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            text-align: center;
            z-index: 1000;
        }
        
        .progress-bar {
            width: 200px;
            height: 6px;
            background: #e9ecef;
            border-radius: 3px;
            overflow: hidden;
            margin-bottom: 15px;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            width: 0%;
            transition: width 0.3s ease;
            animation: progress-animation 2s ease-in-out infinite;
        }
        
        @keyframes progress-animation {
            0% { width: 0%; }
            50% { width: 70%; }
            100% { width: 100%; }
        }
        
        .progress-text {
            color: #666;
            font-weight: 500;
        }
    `;
    
    document.head.appendChild(progressStyles);
    return progress;
}

// Enhanced upload with progress
async function handleUploadWithProgress(event) {
    event.preventDefault();
    
    const file = resumeFile.files[0];
    if (!file) {
        showError('Please select a file to upload.');
        return;
    }
    
    // Show progress
    const progressIndicator = createProgressIndicator();
    document.body.appendChild(progressIndicator);
    hideError();
    
    // Create FormData
    const formData = new FormData();
    formData.append('resume', file);
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || 'Upload failed');
        }
        
        if (result.success && result.redirect) {
            window.location.href = result.redirect;
        } else {
            throw new Error('Invalid response from server');
        }
        
    } catch (error) {
        console.error('Upload error:', error);
        showError(error.message || 'An error occurred during upload. Please try again.');
    } finally {
        // Remove progress indicator
        if (progressIndicator.parentNode) {
            progressIndicator.parentNode.removeChild(progressIndicator);
        }
    }
}

// Replace the original upload handler with the enhanced one
uploadForm.removeEventListener('submit', handleUpload);
uploadForm.addEventListener('submit', handleUploadWithProgress);

// Console log for debugging
console.log('AI Resume Analyzer - Frontend loaded successfully');
