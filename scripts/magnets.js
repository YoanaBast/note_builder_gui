document.addEventListener('DOMContentLoaded', () => {
  const container = document.querySelector('.content'); // your h1
  if (!container) return;

  const text = container.innerText;
  container.innerHTML = ''; // clear existing text

  // Split into words
  text.split(' ').forEach((wordText, wIndex) => {
    const wordSpan = document.createElement('span');
    wordSpan.className = 'word';
    wordSpan.style.whiteSpace = 'nowrap'; // prevent word break

    // Wrap each letter
    wordText.split('').forEach(char => {
      const letterSpan = document.createElement('span');
      letterSpan.textContent = char;
      wordSpan.appendChild(letterSpan);
    });

    // Add a space after word
    const space = document.createTextNode(' ');
    wordSpan.appendChild(space);

    container.appendChild(wordSpan);
  });
});
