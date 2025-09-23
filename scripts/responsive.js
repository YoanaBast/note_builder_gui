function adjustForMobile() {
    const width = window.innerWidth;
    const height = window.innerHeight;
    const scaleFactor = window.devicePixelRatio || 1;

    // if screen width is less than 768px (typical mobile breakpoint)
    if (width < 768) {
        // zoom out slightly
        const zoom = 1 / scaleFactor; // adjust based on device pixel ratio
        document.body.style.transform = `scale(${zoom})`;
        document.body.style.transformOrigin = 'top left';
        document.body.style.width = `${100 / zoom}%`; // keep layout width
    } else {
        // reset for larger screens
        document.body.style.transform = '';
        document.body.style.transformOrigin = '';
        document.body.style.width = '';
    }
}

// run initially
adjustForMobile();

// run on resize
window.addEventListener('resize', adjustForMobile);
