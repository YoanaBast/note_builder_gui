// gridColors.js
const gridColors = [
  "#e6e6ff", // light purple
  "#ffe6e6", // light red
  "#e6ffe6", // light green
  "#fff0e6", // light orange
  "#f0e6ff", // light lavender
  "#fff79a"  // light yellow
];

function colorGridItems() {
  document.querySelectorAll(".grid-item button").forEach(btn => {
    const randomColor = gridColors[Math.floor(Math.random() * gridColors.length)];

    // solid color
    btn.style.background = randomColor;

    // match border to inside color
    btn.style.border = `1px solid ${randomColor}`;
  });
}

// Run after DOM is ready
document.addEventListener("DOMContentLoaded", colorGridItems);
