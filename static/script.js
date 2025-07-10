document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('search-form');
  const input = document.getElementById('search-input');
  const result = document.getElementById('result');
  const randomBtn = document.getElementById('random-btn');
  const darkToggle = document.getElementById('dark-toggle');

  async function fetchRandomArticle() {
    result.classList.add('hidden');
    result.textContent = 'Loading random article...';
    try {
      const res = await fetch('/api/random');
      const data = await res.json();
      if (data.error) {
        result.textContent = data.error;
      } else {
        const url = `https://en.wikipedia.org/wiki/${encodeURIComponent(data.title.replace(/ /g, '_'))}`;
        result.innerHTML = `<h2><a href="${url}" target="_blank" rel="noopener">${data.title}</a></h2><p>${data.summary}</p>`;
      }
      result.classList.remove('hidden');
    } catch (err) {
      result.textContent = 'Error fetching random article.';
      result.classList.remove('hidden');
    }
  }

  form.addEventListener('submit', async function(e) {
    e.preventDefault();
    const query = input.value.trim();
    if (!query) return;
    result.classList.add('hidden');
    result.textContent = 'Loading...';
    try {
      const res = await fetch(`/api/search?query=${encodeURIComponent(query)}`);
      const data = await res.json();
      if (data.error) {
        result.textContent = data.error;
      } else {
        const url = `https://en.wikipedia.org/wiki/${encodeURIComponent(data.title.replace(/ /g, '_'))}`;
        result.innerHTML = `<h2><a href="${url}" target="_blank" rel="noopener">${data.title}</a></h2><p>${data.summary}</p>`;
      }
      result.classList.remove('hidden');
    } catch (err) {
      result.textContent = 'Error fetching article.';
      result.classList.remove('hidden');
    }
  });

  randomBtn.addEventListener('click', fetchRandomArticle);

  // Dark mode logic
  function setDarkMode(on) {
    if (on) {
      document.body.classList.add('dark');
      localStorage.setItem('darkMode', '1');
      darkToggle.checked = true;
    } else {
      document.body.classList.remove('dark');
      localStorage.setItem('darkMode', '0');
      darkToggle.checked = false;
    }
  }
  // On load, set dark mode from localStorage
  setDarkMode(localStorage.getItem('darkMode') === '1');
  darkToggle.addEventListener('change', function() {
    setDarkMode(darkToggle.checked);
  });

  // Fetch a random article on initial load
  fetchRandomArticle();
}); 