const navColors = [
  "#fff266", // bright yellow
  "#ff99d6", // bright pink
  "#66e0ff", // bright baby blue
  "#99ff99", // bright light green
  "#ffd699", // bright peach
  "#ccccff"  // brighter lavender
];

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("nav a").forEach(link => {
    const color = navColors[Math.floor(Math.random() * navColors.length)];

    // random shape
    const radius = Math.floor(Math.random() * 20) + 8;  // 8–28px

    // random tilt
    const tilt = (Math.random() * 6 - 3) + "deg";       // -3° to +3°

    link.style.background = color;
    link.style.borderRadius = radius + "px";
    link.style.transform = `rotate(${tilt})`;
  });
});
