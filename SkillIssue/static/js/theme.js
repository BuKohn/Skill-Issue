window.toggleTheme = function(e) {
    if (e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
    updateLogo(newTheme);
};

function updateThemeIcon(theme) {
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.textContent = theme === 'dark' ? '☀️' : '🌙';
        themeToggle.title = theme === 'dark' ? 'Переключить на светлую тему' : 'Переключить на темную тему';
    }
}

function updateLogo(theme) {
    const heroLogo = document.querySelector('.hero-logo');
    if (heroLogo) {
        if (theme === 'dark') {
            heroLogo.src = heroLogo.getAttribute('data-dark-src') || heroLogo.src.replace('logo.png', 'logo-dark.png');
        } else {
            heroLogo.src = heroLogo.getAttribute('data-light-src') || heroLogo.src.replace('logo-dark.png', 'logo.png');
        }
    }
}

function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    const html = document.documentElement;
    html.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
    updateLogo(savedTheme);
    
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.removeEventListener('click', window.toggleTheme);
        themeToggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            window.toggleTheme();
        });
    }
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTheme);
} else {
    initTheme();
}

window.addEventListener('load', function() {
    setTimeout(initTheme, 100);
});

