document.addEventListener('DOMContentLoaded', () => {
    // ====================== Vendor Panel ======================
    const tableRows = document.querySelectorAll('.vp-data-table tbody tr');
    const filterSelect = document.getElementById('vp-orderFilter');
    
    // Table UI Enhancements
    tableRows.forEach(row => {
        Object.assign(row.style, {
            transition: 'all 0.3s ease',
            willChange: 'opacity, transform'
        });
    });

    // Filter Orders
    filterSelect?.addEventListener('change', function() {
        const selectedOption = this.value.toLowerCase();
        let visibleCount = 0;

        tableRows.forEach((row, index) => {
            const status = row.querySelector('td:last-child span').textContent.toLowerCase();
            const isVisible = selectedOption === 'all' || status === selectedOption;

            setTimeout(() => {
                row.style.opacity = isVisible ? '1' : '0';
                row.style.transform = isVisible ? 'translateY(0)' : 'translateY(-5px)';
                row.style.display = isVisible ? '' : 'none';
                if (isVisible) visibleCount++;
            }, index * 15);
        });

        console.log(`Visible orders: ${visibleCount}/${tableRows.length}`);
    });

    // Row Interactions
    tableRows.forEach(row => {
        row.addEventListener('click', () => {
            tableRows.forEach(r => r.classList.remove('vp-selected-row'));
            row.classList.add('vp-selected-row');
        });

        row.addEventListener('dblclick', (e) => {
            e.preventDefault();
            const orderId = row.querySelector('td:first-child').textContent;
            alert(`Opening order #${orderId}`); // Replace with actual navigation
        });
    });

    // ====================== File Uploads ======================
    // Trigger file inputs
    document.getElementById('changeLogoBtn')?.addEventListener('click', () => 
        document.getElementById('profilePictureInput').click()
    );

    document.getElementById('uploadCoverBtn')?.addEventListener('click', () => 
        document.getElementById('coverPhotoInput').click()
    );

    document.getElementById('uploadLicenseBtn')?.addEventListener('click', () => 
        document.getElementById('vendorLicenseInput').click()
    );

    // Preview uploaded files
    const handleFilePreview = (inputId, previewId) => {
        document.getElementById(inputId)?.addEventListener('change', (e) => {
            const file = e.target.files[0];
            const preview = document.getElementById(previewId);
            
            if (file) {
                preview.innerHTML = `<img src="${URL.createObjectURL(file)}"><span>${file.name}</span>`;
            }
        });
    };

    handleFilePreview('profilePictureInput', 'logoPreview');
    handleFilePreview('coverPhotoInput', 'coverPreview');
    handleFilePreview('vendorLicenseInput', 'licensePreview');
});