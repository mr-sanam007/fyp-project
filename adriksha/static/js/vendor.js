/**
 * Vendor Panel JavaScript - Updated with proper logout handling
 */
document.addEventListener('DOMContentLoaded', function() {
  // DOM Elements
  const tableRows = document.querySelectorAll('.vp-data-table tbody tr');
  const filterSelect = document.getElementById('vp-orderFilter');
  const tableWrapper = document.querySelector('.vp-table-wrapper');
  const contentSection = document.querySelector('.vp-content-section');
  const navItems = document.querySelectorAll('.vp-nav-item:not(.vp-logout-item)'); // Exclude logout item
  
  // Add CSS transitions
  document.querySelectorAll('.vp-data-table tbody tr').forEach(row => {
    row.style.transition = 'opacity 0.3s ease, transform 0.3s ease, background-color 0.2s ease';
    row.style.willChange = 'opacity, transform';
    row.setAttribute('data-visible', 'true');
  });
  
  if (contentSection) {
    contentSection.style.transition = 'opacity 0.3s ease';
  }
  
  // Handle order filtering
  filterSelect.addEventListener('change', function() {
    this.classList.add('vp-filter-applied');
    setTimeout(() => this.classList.remove('vp-filter-applied'), 500);
    
    const selectedOption = this.value;
    let visibleCount = 0;
    
    tableWrapper.style.opacity = '0.98';
    
    tableRows.forEach((row, index) => {
      const statusText = row.querySelector('td:last-child span').textContent.toLowerCase();
      const shouldBeVisible = (selectedOption === 'all' || statusText === selectedOption.toLowerCase());
      
      setTimeout(() => {
        if (shouldBeVisible) {
          row.style.display = '';
          setTimeout(() => {
            row.style.opacity = '1';
            row.style.transform = 'translateY(0)';
          }, 10);
          row.setAttribute('data-visible', 'true');
          visibleCount++;
        } else {
          row.style.opacity = '0';
          row.style.transform = 'translateY(-3px)';
          row.setAttribute('data-visible', 'false');
          
          setTimeout(() => {
            if (row.getAttribute('data-visible') === 'false') {
              row.style.display = 'none';
            }
          }, 300);
        }
      }, index * 15);
    });
    
    setTimeout(() => {
      tableWrapper.style.opacity = '1';
      console.log(`Showing ${visibleCount} of ${tableRows.length} orders`);
    }, 300);
  });
  
  // Handle sidebar navigation (excluding logout)
  navItems.forEach(item => {
    item.addEventListener('click', function(e) {
      e.preventDefault();
      
      if (!this.classList.contains('vp-active')) {
        navItems.forEach(navItem => navItem.classList.remove('vp-active'));
        this.classList.add('vp-active');
        
        const icon = this.querySelector('i');
        icon.style.transform = 'scale(1.2)';
        setTimeout(() => icon.style.transform = '', 300);
        
        const menuText = this.querySelector('span').textContent;
        
        contentSection.style.opacity = '0';
        
        setTimeout(() => {
          const sectionHeading = document.querySelector('.vp-section-heading');
          sectionHeading.textContent = menuText === 'DASHBOARD' ? 'RECENT ORDERS' : menuText;
          contentSection.style.opacity = '1';
        }, 300);
      }
    });
  });
  
  // Handle table row interactions
  tableRows.forEach(row => {
    row.addEventListener('click', function() {
      const orderId = this.querySelector('td:first-child').textContent;
      
      this.style.backgroundColor = 'var(--vp-gray-100)';
      
      setTimeout(() => {
        this.style.backgroundColor = '';
        
        tableRows.forEach(r => {
          r.classList.remove('vp-selected-row');
          r.style.boxShadow = '';
          r.style.transform = '';
        });
        
        this.classList.add('vp-selected-row');
        console.log(`Order ${orderId} selected`);
      }, 150);
    });
    
    row.addEventListener('mouseenter', function() {
      this.style.cursor = 'pointer';
      if (!this.classList.contains('vp-selected-row')) {
        this.style.backgroundColor = 'var(--vp-gray-50)';
        this.style.transform = 'translateY(-1px)';
        this.style.boxShadow = 'var(--vp-shadow-sm)';
      }
    });
    
    row.addEventListener('mouseleave', function() {
      if (!this.classList.contains('vp-selected-row')) {
        this.style.backgroundColor = '';
        this.style.transform = '';
        this.style.boxShadow = '';
      }
    });
    
    row.addEventListener('dblclick', function(e) {
      e.preventDefault();
      const orderId = this.querySelector('td:first-child').textContent;
      
      const toast = document.createElement('div');
      toast.textContent = `Opening details for order #${orderId}`;
      toast.className = 'vp-notification';
      document.body.appendChild(toast);
      
      setTimeout(() => {
        toast.style.opacity = '1';
        toast.style.transform = 'translateY(0)';
        
        setTimeout(() => {
          toast.style.opacity = '0';
          toast.style.transform = 'translateY(-10px)';
          setTimeout(() => toast.remove(), 300);
        }, 3000);
      }, 10);
    });
  });
});