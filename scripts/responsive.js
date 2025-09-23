function adjustForMobile() {
    const width = window.innerWidth;

    if (width < 768) {
        // Calculate appropriate scale for mobile
        const scale = Math.min(0.9, width / 850); // Adjust denominator as needed
        document.body.style.transform = `scale(${scale})`;
        document.body.style.transformOrigin = 'top left';
        document.body.style.width = `${100 / scale}%`;
        document.body.style.height = `${100 / scale}%`; // Add height adjustment

        // Ensure modals can display beyond the scaled container
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            modal.style.position = 'fixed';
            modal.style.zIndex = '1000';
            modal.style.top = '0';
            modal.style.left = '0';
            modal.style.width = '100vw';
            modal.style.height = '100vh';
            modal.style.transform = 'none'; // Override parent scaling
        });
    } else {
        // Reset for larger screens
        document.body.style.transform = '';
        document.body.style.transformOrigin = '';
        document.body.style.width = '';
        document.body.style.height = '';

        // Reset modal styles
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            modal.style.position = '';
            modal.style.zIndex = '';
            modal.style.transform = '';
        });
    }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', function() {
    adjustForMobile();
    window.addEventListener('resize', adjustForMobile);
});