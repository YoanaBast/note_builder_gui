// modalColors.js

const modalColors = [
  "#e6e6ff", // light purple
  "#ffe6e6", // light red
  "#e6ffe6", // light green
  "#fff0e6", // light orange
  "#f0e6ff"  // light lavender
];

function setupAllModals() {
  // Find all buttons whose id starts with "openBtn-"
  document.querySelectorAll("[id^='openBtn-']").forEach(btn => {
    const btnId = btn.id;
    const modalId = btnId.replace("openBtn-", "myModal-"); // match modal naming
    const modal = document.getElementById(modalId);

    if (!modal) return; // skip if modal not found

    const span = modal.querySelector(".close");

    btn.onclick = () => {
      const randomColor = modalColors[Math.floor(Math.random() * modalColors.length)];
      modal.querySelector(".modal-content").style.backgroundColor = randomColor;
      modal.style.display = "block";
    };

    span.onclick = () => modal.style.display = "none";

    window.addEventListener("click", (event) => {
      if (event.target === modal) modal.style.display = "none";
    });
  });
}

// Run after DOM is ready
document.addEventListener("DOMContentLoaded", setupAllModals);
