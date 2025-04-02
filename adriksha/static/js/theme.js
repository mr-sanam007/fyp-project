document.addEventListener('DOMContentLoaded', function() {
  // ===== STATE MANAGEMENT =====
  const state = {
    isDarkMode: localStorage.getItem('darkMode') === 'true',
    isMobileMenuOpen: false,
    activeDropdown: null,
    selectedLanguage: localStorage.getItem('selectedLanguage') || 'EN / NPR',
    selectedLangCode: localStorage.getItem('selectedLangCode') || 'EN / NPR',
    selectedCurrencyCode: localStorage.getItem('selectedCurrencyCode') || 'NPR'
  };

  // ===== DOM ELEMENTS =====
  const elements = {
    header: document.getElementById('main-header'),
    themeToggle: document.getElementById('theme-toggle'),
    mobileMenuButton: document.getElementById('mobile-menu-button'),
    mobileMenu: document.getElementById('mobile-menu'),
    searchInput: document.getElementById('search-input'),
    mobileSearchInput: document.getElementById('mobile-search-input'),
    searchButton: document.getElementById('search-button'),
    mobileSearchButton: document.getElementById('mobile-search-button'),
    languageDropdownButton: document.getElementById('language-dropdown-button'),
    languageDropdown: document.getElementById('language-dropdown'),
    languageDropdownContainer: document.getElementById('language-dropdown-container'),
    selectedLanguageText: document.getElementById('selected-language'),
    accountDropdownButton: document.getElementById('account-dropdown-button'),
    accountDropdown: document.getElementById('account-dropdown'),
    accountDropdownContainer: document.getElementById('account-dropdown-container'),
    categoriesDropdownButton: document.getElementById('categories-dropdown-button'),
    categoriesDropdown: document.getElementById('categories-dropdown'),
    categoriesDropdownContainer: document.getElementById('categories-dropdown-container')
  };

  // ===== HELPER FUNCTIONS =====
  function closeAllDropdowns() {
    const dropdownContainers = [
      elements.languageDropdownContainer,
      elements.accountDropdownContainer,
      elements.categoriesDropdownContainer
    ];
    
    dropdownContainers.forEach(container => {
      if (container) container.classList.remove('dropdown-active');
    });
    
    state.activeDropdown = null;
  }

  function toggleDropdown(container, dropdownName) {
    if (state.activeDropdown === dropdownName) {
      closeAllDropdowns();
      return;
    }
    
    closeAllDropdowns();
    container.classList.add('dropdown-active');
    state.activeDropdown = dropdownName;
  }

  // ===== DARK MODE FUNCTIONS =====
  function updateDarkModeElements() {
    // Update logo
    const logo = document.querySelector('.company-logo');
    if (logo) {
      logo.style.filter = state.isDarkMode ? 'brightness(0) invert(1)' : 'none';
    }
    
    // Update payment icons
    document.querySelectorAll('.light-mode-payment').forEach(icon => {
      icon.style.display = state.isDarkMode ? 'none' : 'block';
    });
    document.querySelectorAll('.dark-mode-payment').forEach(icon => {
      icon.style.display = state.isDarkMode ? 'block' : 'none';
    });
  }

  function toggleTheme() {
    state.isDarkMode = !state.isDarkMode;
    
    // Save dark mode preference
    localStorage.setItem('darkMode', state.isDarkMode);
    
    // Update theme icon
    elements.themeToggle.innerHTML = state.isDarkMode 
      ? '<i class="fas fa-moon"></i>' 
      : '<i class="fas fa-sun"></i>';
    
    // Toggle dark mode class on body
    document.body.classList.toggle('dark-mode', state.isDarkMode);
    
    // Update logo and payment icons
    updateDarkModeElements();
  }

  // ===== OTHER EVENT HANDLERS =====
  function toggleMobileMenu() {
    state.isMobileMenuOpen = !state.isMobileMenuOpen;
    elements.mobileMenu.classList.toggle('show', state.isMobileMenuOpen);
  }

  function changeLanguage(language, langCode) {
    if (elements.selectedLanguageText) {
      elements.selectedLanguageText.textContent = language;
      state.selectedLanguage = language;
      state.selectedLangCode = langCode;
      localStorage.setItem('selectedLanguage', language);
      localStorage.setItem('selectedLangCode', langCode);
      updateCheckmarks();
    }
    closeAllDropdowns();
  }
  
  function changeCurrency(currencyCode) {
    state.selectedCurrencyCode = currencyCode;
    localStorage.setItem('selectedCurrencyCode', currencyCode);
    const displayText = `${state.selectedLangCode.split(' / ')[0]} / ${currencyCode}`;
    if (elements.selectedLanguageText) {
      elements.selectedLanguageText.textContent = displayText;
      state.selectedLanguage = displayText;
      localStorage.setItem('selectedLanguage', displayText);
    }
    updateCheckmarks();
    closeAllDropdowns();
  }
  
  function updateCheckmarks() {
    if (!elements.languageDropdown) return;
    
    const langOptions = elements.languageDropdown.querySelectorAll('a[data-lang]');
    const currOptions = elements.languageDropdown.querySelectorAll('a[data-currency]');
    
    // Clear all checkmarks
    [...langOptions, ...currOptions].forEach(option => {
      option.classList.remove('active');
      const checkIcon = option.querySelector('.fa-check');
      if (checkIcon) checkIcon.remove();
    });
    
    // Add checkmark to selected language
    const selectedLangEl = elements.languageDropdown.querySelector(`a[data-lang="${state.selectedLangCode}"]`);
    if (selectedLangEl) {
      selectedLangEl.classList.add('active');
      const span = selectedLangEl.querySelector('span');
      if (span && !selectedLangEl.querySelector('.fa-check')) {
        const checkIcon = document.createElement('i');
        checkIcon.className = 'fas fa-check';
        span.insertAdjacentElement('afterend', checkIcon);
      }
    }
    
    // Add checkmark to selected currency
    const selectedCurrEl = elements.languageDropdown.querySelector(`a[data-currency="${state.selectedCurrencyCode}"]`);
    if (selectedCurrEl) {
      selectedCurrEl.classList.add('active');
      const span = selectedCurrEl.querySelector('span');
      if (span && !selectedCurrEl.querySelector('.fa-check')) {
        const checkIcon = document.createElement('i');
        checkIcon.className = 'fas fa-check';
        span.insertAdjacentElement('afterend', checkIcon);
      }
    }
  }

  // ===== INITIALIZATION =====
  function initialize() {
    // Apply initial dark mode state
    if (state.isDarkMode) {
      document.body.classList.add('dark-mode');
      elements.themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
      updateDarkModeElements();
    }

    // Set initial language
    if (elements.selectedLanguageText) {
      elements.selectedLanguageText.textContent = state.selectedLanguage;
    }
    
    // Initialize checkmarks
    updateCheckmarks();

    // Set up dark mode observer
    const darkModeObserver = new MutationObserver(function(mutations) {
      mutations.forEach(function(mutation) {
        if (mutation.attributeName === 'class') {
          updateDarkModeElements();
        }
      });
    });

    darkModeObserver.observe(document.body, {
      attributes: true,
      attributeFilter: ['class']
    });
  }

  // ===== EVENT LISTENERS =====
  elements.themeToggle?.addEventListener('click', toggleTheme);
  elements.mobileMenuButton?.addEventListener('click', toggleMobileMenu);
  
  elements.languageDropdownButton?.addEventListener('click', (e) => {
    e.stopPropagation();
    toggleDropdown(elements.languageDropdownContainer, 'language');
  });
  
  elements.languageDropdown?.querySelectorAll('a[data-lang]').forEach(option => {
    option.addEventListener('click', (e) => {
      e.preventDefault();
      changeLanguage(option.getAttribute('data-lang'), option.getAttribute('data-lang'));
    });
  });
  
  elements.languageDropdown?.querySelectorAll('a[data-currency]').forEach(option => {
    option.addEventListener('click', (e) => {
      e.preventDefault();
      changeCurrency(option.getAttribute('data-currency'));
    });
  });
  
  elements.accountDropdownButton?.addEventListener('click', (e) => {
    e.stopPropagation();
    toggleDropdown(elements.accountDropdownContainer, 'account');
  });
  
  elements.categoriesDropdownButton?.addEventListener('click', (e) => {
    e.stopPropagation();
    toggleDropdown(elements.categoriesDropdownContainer, 'categories');
  });
  
  document.addEventListener('click', () => {
    if (state.activeDropdown) closeAllDropdowns();
  });
  
  document.querySelectorAll('.dropdown-menu').forEach(menu => {
    menu.addEventListener('click', (e) => e.stopPropagation());
  });

  document.querySelectorAll('a[data-lang], a[data-currency]').forEach(link => {
    link.addEventListener('click', (e) => e.preventDefault());
  });

  // Initialize everything
  initialize();
});