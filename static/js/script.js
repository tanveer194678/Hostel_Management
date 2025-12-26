// Main JavaScript File
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips and popovers if using Bootstrap
    initializeBootstrapComponents();
    
    // Add smooth scroll behavior
    addSmoothScroll();
    
    // Initialize form validation
    initializeFormValidation();

    // Initialize theme (reads localStorage / system preference)
    initTheme();

    // Attach theme toggle handlers (support multiple toggles per page)
    document.querySelectorAll('.theme-toggle').forEach(btn => btn.addEventListener('click', toggleTheme));
});

function setThemeIndicator(name) {
    const indicator = document.getElementById('theme-indicator');
    if (!indicator) return;
    const icon = (name === 'dark') ? '🌙' : (name === 'sunrise') ? '🌞' : (name === 'forest') ? '🌲' : '';
    indicator.textContent = `Theme: ${icon} ${name.charAt(0).toUpperCase() + name.slice(1)}`;
}

// Update setTheme to call setThemeIndicator


// Theme helpers
const AVAILABLE_THEMES = ['dark', 'sunrise', 'forest'];

// Color presets used to generate the animated overlay between themes
const THEME_COLORS = {
    dark: ['#0f172a', '#64748b'],
    sunrise: ['#ff6b6b', '#ffd166'],
    forest: ['#16a34a', '#4ade80']
};

function setTheme(name) {
    // Animate theme swap with an overlay to create a smooth transition
    animateThemeChange(name);
}

function animateThemeChange(next) {
    const duration = 600; // ms total (we swap mid-way)
    const current = localStorage.getItem('site-theme') || 'forest';
    const from = THEME_COLORS[current] || THEME_COLORS.forest;
    const to = THEME_COLORS[next] || from;

    const overlay = document.createElement('div');
    overlay.className = 'theme-overlay';
    overlay.style.background = `linear-gradient(120deg, ${from[0]} 0%, ${to[1]} 100%)`;
    document.body.appendChild(overlay);

    // Trigger fade-in
    requestAnimationFrame(() => overlay.classList.add('show'));

    // After half the duration, apply the new theme classes so elements transition
    setTimeout(() => {
        document.documentElement.classList.remove('theme-sunrise', 'theme-forest');
        if (next === 'sunrise') document.documentElement.classList.add('theme-sunrise');
        if (next === 'forest') document.documentElement.classList.add('theme-forest');
        localStorage.setItem('site-theme', next);
        updateThemeIcon();

        // fade overlay out
        overlay.classList.remove('show');
        // remove overlay after fade out completes
        setTimeout(() => overlay.remove(), duration / 2 + 50);
    }, duration / 2);
}

function toggleTheme() {
    const current = localStorage.getItem('site-theme') || 'dark';
    const idx = AVAILABLE_THEMES.indexOf(current);
    const next = AVAILABLE_THEMES[(idx + 1) % AVAILABLE_THEMES.length];
    setTheme(next);
}

function initTheme() {
    const saved = localStorage.getItem('site-theme');
    if (saved) setTheme(saved);
    else {
        const prefersLight = window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches;
        // Prefer warm 'sunrise' for light mode, 'forest' for dark mode
        setTheme(prefersLight ? 'sunrise' : 'forest');
    }
}

function updateThemeIcon() {
    const btn = document.getElementById('theme-toggle');
    if (!btn) return;
    const theme = localStorage.getItem('site-theme') || 'dark';
    // Icon mapping: dark -> 🌙, sunrise -> 🌞, forest -> 🌲
    if (theme === 'dark') btn.textContent = '🌙';
    else if (theme === 'sunrise') btn.textContent = '🌞';
    else if (theme === 'forest') btn.textContent = '🌲';

    btn.setAttribute('aria-label', `Cycle theme (current: ${theme})`);
}

// Initialize Bootstrap components
function initializeBootstrapComponents() {
    // Tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// Smooth scroll behavior
function addSmoothScroll() {
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
}

// Form validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

// Confirmation dialog for delete actions
function confirmDelete(message = 'Are you sure you want to delete this item?') {
    return confirm(message);
}

// Add active class to current navigation link
function setActiveNavLink() {
    const currentLocation = location.pathname;
    const menuItems = document.querySelectorAll('.nav-link');
    
    menuItems.forEach(item => {
        if (item.getAttribute('href') === currentLocation) {
            item.classList.add('active');
        }
    });
}

// Debounce function for optimized event handling
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle function for performance optimization
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Call on page load
setActiveNavLink();
