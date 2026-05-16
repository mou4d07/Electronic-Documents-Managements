const basePath = '/Ged';

// Theme management
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = themeToggle.querySelector('i');
    const appLogo = document.getElementById('appLogo'); // Get logo element

    document.documentElement.setAttribute('data-theme', savedTheme);
    document.documentElement.setAttribute('data-bs-theme', savedTheme); // Set Bootstrap theme

    if (savedTheme === 'dark') {
        themeIcon.className = 'fas fa-sun';
        if (appLogo) appLogo.src = `${basePath}/static_Files/logo/LOGO_clair.png`; // Set dark logo
    } else {
        themeIcon.className = 'fas fa-moon';
        if (appLogo) appLogo.src = `${basePath}/static_Files/logo/LOGO-min.png`; // Set light logo
    }
}

// Toggle theme
document.getElementById('themeToggle').addEventListener('click', function() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    const themeIcon = this.querySelector('i');
    const appLogo = document.getElementById('appLogo'); // Get logo element

    document.documentElement.setAttribute('data-theme', newTheme);
    document.documentElement.setAttribute('data-bs-theme', newTheme); // Set Bootstrap theme
    localStorage.setItem('theme', newTheme);

    if (newTheme === 'dark') {
        themeIcon.className = 'fas fa-sun';
        if (appLogo) appLogo.src = `${basePath}/static_Files/logo/LOGO_clair.png`; // Set dark logo
    } else {
        themeIcon.className = 'fas fa-moon';
        if (appLogo) appLogo.src = `${basePath}/static_Files/logo/LOGO-min.png`; // Set light logo
    }
});

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    initializeTheme();
});