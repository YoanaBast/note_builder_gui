document.addEventListener('DOMContentLoaded', () => {
  const container = document.querySelector('.content');
  if (!container) return;

  const text = container.innerText;
  container.innerHTML = ''; // clear existing text

  // Wrap each letter in a span
  text.split('').forEach(char => {
    const span = document.createElement('span');
    span.textContent = char === ' ' ? '\u00A0' : char; // preserve spaces
    container.appendChild(span);
  });
});
