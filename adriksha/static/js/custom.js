document.addEventListener('DOMContentLoaded', function() {
    // Form Toggle Logic
    function initializeForm() {
        const step1 = document.getElementById('step1');
        const step2 = document.getElementById('step2');
        
        if (step1 && step2) {
            // Initial state
            step1.style.display = 'block';
            step2.style.display = 'none';
            
            // Next button functionality
            const nextButton = document.getElementById('nextStep');
            if (nextButton) {
                nextButton.addEventListener('click', function(e) {
                    e.preventDefault();
                    step1.style.display = 'none';
                    step2.style.display = 'block';
                    
                    // Update step indicators
                    updateStepIndicators(2);
                    window.scrollTo(0, 0);
                });
            }
            
            // Back button functionality
            const prevButton = document.getElementById('prevStep');
            if (prevButton) {
                prevButton.addEventListener('click', function(e) {
                    e.preventDefault();
                    step2.style.display = 'none';
                    step1.style.display = 'block';
                    
                    // Update step indicators
                    updateStepIndicators(1);
                    window.scrollTo(0, 0);
                });
            }
            
            // File upload display
            const fileInput = document.querySelector('input[type="file"]');
            const fileNameDisplay = document.getElementById('fileNameDisplay');
            
            if (fileInput && fileNameDisplay) {
                fileInput.addEventListener('change', function() {
                    fileNameDisplay.textContent = this.files[0]?.name || 'No file chosen';
                });
            }
        }
    }
    
    function updateStepIndicators(activeStep) {
        const step1Indicator = document.querySelector('.form-step[data-step="1"]');
        const step2Indicator = document.querySelector('.form-step[data-step="2"]');
        
        if (step1Indicator && step2Indicator) {
            step1Indicator.classList.toggle('active', activeStep === 1);
            step2Indicator.classList.toggle('active', activeStep === 2);
        }
    }
    
    // Dashboard Logic
    function initializeDashboard() {
        // Only run if we're on the dashboard page
        if (!document.getElementById('sidebar')) return;
        
        // DOM Elements
        const toggleSidebarBtn = document.getElementById('toggle-sidebar');
        const sidebar = document.getElementById('sidebar');
        const mainContent = document.querySelector('.main-content');
        const navItems = document.querySelectorAll('.nav-item a');
        const themeToggle = document.querySelector('.theme-toggle');
        
        // Sidebar toggle
        if (toggleSidebarBtn && sidebar && mainContent) {
            toggleSidebarBtn.addEventListener('click', function() {
                sidebar.classList.toggle('collapsed');
                mainContent.classList.toggle('expanded');
            });
        }
        
        // Navigation
        if (navItems.length) {
            navItems.forEach(item => {
                item.addEventListener('click', handleNavigation);
            });
        }
        
        function handleNavigation(e) {
            e.preventDefault();
            
            // Update active state
            navItems.forEach(item => {
                item.parentElement.classList.remove('active');
            });
            this.parentElement.classList.add('active');
            
            // Close sidebar on mobile
            if (window.innerWidth <= 768 && sidebar) {
                sidebar.classList.remove('show');
            }
            
            // Update page title
            const sectionName = this.querySelector('span')?.textContent;
            if (sectionName) {
                const header = document.querySelector('.page-header h1');
                if (header) header.textContent = `${sectionName} Overview`;
            }
        }
        
        // Theme toggle
        if (themeToggle) {
            themeToggle.addEventListener('click', toggleTheme);
        }
        
        function toggleTheme() {
            document.body.classList.toggle('dark-mode');
            const themeIcon = themeToggle.querySelector('i');
            if (themeIcon) {
                themeIcon.className = document.body.classList.contains('dark-mode') 
                    ? 'fas fa-moon' 
                    : 'fas fa-sun';
            }
            localStorage.setItem('theme', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
            applyDarkModeStyles();
        }
        
        function applyDarkModeStyles() {
            const root = document.documentElement;
            if (document.body.classList.contains('dark-mode')) {
                root.style.setProperty('--white', '#1a1a1a');
                root.style.setProperty('--light-gray', '#333333');
                root.style.setProperty('--dark-color', '#f8f9fa');
                root.style.setProperty('--border-color', '#444444');
            } else {
                root.style.setProperty('--white', '#ffffff');
                root.style.setProperty('--light-gray', '#e9ecef');
                root.style.setProperty('--dark-color', '#222222');
                root.style.setProperty('--border-color', '#dee2e6');
            }
        }
        
        // Check viewport width
        function checkViewportWidth() {
            if (!sidebar) return;
            
            if (window.innerWidth <= 768) {
                sidebar.classList.remove('collapsed', 'show');
                if (mainContent) mainContent.classList.remove('expanded');
                
                // Mobile menu toggle
                document.addEventListener('click', function(e) {
                    if (e.target.closest('#toggle-sidebar')) {
                        sidebar.classList.toggle('show');
                    } else if (!e.target.closest('.sidebar') && sidebar.classList.contains('show')) {
                        sidebar.classList.remove('show');
                    }
                });
            } else if (window.innerWidth <= 1024) {
                sidebar.classList.add('collapsed');
                if (mainContent) mainContent.classList.add('expanded');
            } else {
                sidebar.classList.remove('collapsed');
                if (mainContent) mainContent.classList.remove('expanded');
            }
        }
        
        // Initialize
        checkViewportWidth();
        window.addEventListener('resize', checkViewportWidth);
        
        // Check saved theme
        if (localStorage.getItem('theme') === 'dark') {
            document.body.classList.add('dark-mode');
            applyDarkModeStyles();
            const themeIcon = themeToggle?.querySelector('i');
            if (themeIcon) themeIcon.className = 'fas fa-moon';
        }
    }
    
    // Initialize both features
    initializeForm();
    initializeDashboard();
});