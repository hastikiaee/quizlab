// Global Navigation System
let userType = localStorage.getItem('userType') || 'student';

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    updateUserInterface();
    highlightCurrentPage();
});

// Update user interface based on user type
function updateUserInterface() {
    const userBadge = document.getElementById('user-type-badge');
    const userAvatar = document.getElementById('user-avatar-text');
    
    if (userBadge && userAvatar) {
        if (userType === 'student') {
            userBadge.textContent = 'دانشجو';
            userAvatar.textContent = 'د';
        } else {
            userBadge.textContent = 'استاد';
            userAvatar.textContent = 'ا';
        }
    }
    
    // Update switcher buttons
    const switcherButtons = document.querySelectorAll('.switcher-btn');
    switcherButtons.forEach(btn => {
        btn.classList.remove('active');
        if ((btn.textContent.includes('دانشجو') && userType === 'student') ||
            (btn.textContent.includes('استاد') && userType === 'teacher')) {
            btn.classList.add('active');
        }
    });
}

// Switch user type
function switchUserType(type) {
    userType = type;
    localStorage.setItem('userType', type);
    updateUserInterface();
    
    // If on dashboard page, update the content
    if (window.location.pathname.includes('dashboard.html')) {
        updateDashboardContent();
    }
}

// Navigation functions
function navigateToPage(page) {
    const pageMap = {
        'home': 'home.html',
        'dashboard': 'dashboard.html',
        'quiz': 'quiz.html',
        'ranking': 'ranking.html',
        'report-details':  djangoUrls.reportDetail+ "?id=" + reportId,
    };
    
    if (pageMap[page]) {
        window.location.href = pageMap[page];
    }
}

// Highlight current page in navigation
function highlightCurrentPage() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        
        const href = link.getAttribute('href');
        if (href && currentPath.includes(href)) {
            link.classList.add('active');
        }
    });
    
    // Special case for home page
    if (currentPath.includes('home.html') || currentPath === '/') {
        document.querySelector('a[href="home.html"]')?.classList.add('active');
    }
}

// Report navigation
function viewReportDetails(reportId) {
    localStorage.setItem('selectedReportId', reportId);
    window.location.href = djangoUrls.reportDetail.replace('0', reportId);
}

function goBackToDashboard() {
    localStorage.removeItem('selectedReportId');
    window.location.href = 'dashboard.html';
}

// Quiz navigation
function startQuiz(quizType) {
    localStorage.setItem('currentQuiz', quizType);
    window.location.href = 'quiz.html';
}

// Utility functions
function showLoading(element) {
    if (element) {
        element.style.opacity = '0.6';
        element.style.pointerEvents = 'none';
    }
}

function hideLoading(element) {
    if (element) {
        element.style.opacity = '1';
        element.style.pointerEvents = 'auto';
    }
}

// Add smooth transitions
function addPageTransition() {
    document.body.style.transition = 'opacity 0.3s ease';
}

// Export functions for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        navigateToPage,
        switchUserType,
        viewReportDetails,
        goBackToDashboard,
        startQuiz,
        updateUserInterface
    };
}

