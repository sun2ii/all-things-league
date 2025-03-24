let champions = [];

async function fetchChampions() {
  try {
    const res = await fetch('/champions');
    champions = await res.json();
    displayChampions(champions);
  } catch (error) {
    console.error('Error fetching champions:', error);
  }
}

function displayChampions(championList) {
  const grid = document.getElementById('championGrid');
  grid.innerHTML = '';

  championList.forEach(name => {
    const link = document.createElement('a');
    link.href = 'profile.html?champion=' + encodeURIComponent(name);
    link.className = 'champion';
    link.style.display = 'block'; // make entire box clickable
    // In case CSS isn't applying, add inline styles for debugging:
    link.style.padding = '8px';
    link.style.background = '#f3f3f3';
    link.style.textAlign = 'center';
    link.style.borderRadius = '5px';
    link.style.fontSize = '14px';
    link.style.color = 'black';
    link.style.textDecoration = 'none';
    link.style.marginBottom = '10px';

    link.textContent = name;
    grid.appendChild(link);
  });
}

document.getElementById('searchBar').addEventListener('input', (e) => {
  const filtered = champions.filter(champ =>
    champ.toLowerCase().includes(e.target.value.toLowerCase())
  );
  displayChampions(filtered);
});

fetchChampions();
