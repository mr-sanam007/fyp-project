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
    // If we're toggling the currently active dropdown, just close it
    if (state.activeDropdown === dropdownName) {
      closeAllDropdowns();
      return;
    }
    
    // Close any open dropdown first
    closeAllDropdowns();
    
    // Open the requested dropdown
    container.classList.add('dropdown-active');
    state.activeDropdown = dropdownName;
  }

  // ===== EVENT HANDLERS =====
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
  }

  function toggleMobileMenu() {
    state.isMobileMenuOpen = !state.isMobileMenuOpen;
    
    if (state.isMobileMenuOpen) {
      elements.mobileMenu.classList.add('show');
    } else {
      elements.mobileMenu.classList.remove('show');
    }
  }

  // Removed the handleSearch function since forms are now submitted to Django backend

  function changeLanguage(language, langCode) {
    if (elements.selectedLanguageText) {
      elements.selectedLanguageText.textContent = language;
      state.selectedLanguage = language;
      state.selectedLangCode = langCode;
      localStorage.setItem('selectedLanguage', language);
      localStorage.setItem('selectedLangCode', langCode);
      
      // Update checkmarks for language options
      updateCheckmarks();
    }
    closeAllDropdowns();
  }
  
  function changeCurrency(currencyCode) {
    state.selectedCurrencyCode = currencyCode;
    localStorage.setItem('selectedCurrencyCode', currencyCode);
    
    // Form language/currency display format
    const displayText = `${state.selectedLangCode.split(' / ')[0]} / ${currencyCode}`;
    if (elements.selectedLanguageText) {
      elements.selectedLanguageText.textContent = displayText;
      state.selectedLanguage = displayText;
      localStorage.setItem('selectedLanguage', displayText);
    }
    
    // Update checkmarks for currency options
    updateCheckmarks();
    closeAllDropdowns();
  }
  
  function updateCheckmarks() {
    if (!elements.languageDropdown) return;
    
    // Remove all checkmarks first
    const langOptions = elements.languageDropdown.querySelectorAll('a[data-lang]');
    langOptions.forEach(option => {
      option.classList.remove('active');
      // Remove any existing checkmarks
      const checkIcon = option.querySelector('.fa-check');
      if (checkIcon) {
        checkIcon.remove();
      }
    });
    
    const currOptions = elements.languageDropdown.querySelectorAll('a[data-currency]');
    currOptions.forEach(option => {
      option.classList.remove('active');
      // Remove any existing checkmarks
      const checkIcon = option.querySelector('.fa-check');
      if (checkIcon) {
        checkIcon.remove();
      }
    });
    
    // Add checkmark to the selected language
    const selectedLangEl = elements.languageDropdown.querySelector(`a[data-lang="${state.selectedLangCode}"]`);
    if (selectedLangEl) {
      selectedLangEl.classList.add('active');
      const span = selectedLangEl.querySelector('span');
      if (span && !selectedLangEl.querySelector('.fa-check')) {
        // Add check icon after the span
        const checkIcon = document.createElement('i');
        checkIcon.className = 'fas fa-check';
        span.insertAdjacentElement('afterend', checkIcon);
      }
    }
    
    // Add checkmark to the selected currency
    const selectedCurrEl = elements.languageDropdown.querySelector(`a[data-currency="${state.selectedCurrencyCode}"]`);
    if (selectedCurrEl) {
      selectedCurrEl.classList.add('active');
      const span = selectedCurrEl.querySelector('span');
      if (span && !selectedCurrEl.querySelector('.fa-check')) {
        // Add check icon after the span
        const checkIcon = document.createElement('i');
        checkIcon.className = 'fas fa-check';
        span.insertAdjacentElement('afterend', checkIcon);
      }
    }
  }

  // Apply initial dark mode state
  if (state.isDarkMode) {
    document.body.classList.add('dark-mode');
    elements.themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
  }

  // Set initial language
  if (elements.selectedLanguageText) {
    elements.selectedLanguageText.textContent = state.selectedLanguage;
  }
  
  // Initialize checkmarks
  updateCheckmarks();

  // ===== EVENT LISTENERS =====
  // Theme Toggle
  elements.themeToggle.addEventListener('click', toggleTheme);
  
  // Mobile Menu
  elements.mobileMenuButton.addEventListener('click', toggleMobileMenu);
  
  // Language Dropdown
  if (elements.languageDropdownButton) {
    elements.languageDropdownButton.addEventListener('click', (e) => {
      e.stopPropagation();
      toggleDropdown(elements.languageDropdownContainer, 'language');
    });
  }
  
  // Language and Currency Selection
  if (elements.languageDropdown) {
    // Language selection
    const languageOptions = elements.languageDropdown.querySelectorAll('a[data-lang]');
    languageOptions.forEach(option => {
      option.addEventListener('click', (e) => {
        e.preventDefault();
        
        const selectedLanguage = option.getAttribute('data-lang');
        changeLanguage(selectedLanguage, selectedLanguage);
      });
    });
    
    // Currency selection
    const currencyOptions = elements.languageDropdown.querySelectorAll('a[data-currency]');
    currencyOptions.forEach(option => {
      option.addEventListener('click', (e) => {
        e.preventDefault();
        
        const currencyCode = option.getAttribute('data-currency');
        changeCurrency(currencyCode);
      });
    });
  }
  
  // Account Dropdown
  if (elements.accountDropdownButton) {
    elements.accountDropdownButton.addEventListener('click', (e) => {
      e.stopPropagation();
      toggleDropdown(elements.accountDropdownContainer, 'account');
    });
  }
  
  // Categories Dropdown
  if (elements.categoriesDropdownButton) {
    elements.categoriesDropdownButton.addEventListener('click', (e) => {
      e.stopPropagation();
      toggleDropdown(elements.categoriesDropdownContainer, 'categories');
    });
  }
  
  // Close dropdowns when clicking outside
  document.addEventListener('click', () => {
    if (state.activeDropdown) {
      closeAllDropdowns();
    }
  });
  
  // Prevent dropdown clicks from propagating
  document.querySelectorAll('.dropdown-menu').forEach(menu => {
    menu.addEventListener('click', (e) => {
      e.stopPropagation();
    });
  });

  // Remove event.preventDefault() for links with hrefs that should work
  // Only prevent default for language/currency selectors
  document.querySelectorAll('a[data-lang], a[data-currency]').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault(); // Only prevent default for language/currency toggles
    });
  });
});