const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.static(path.join(__dirname, 'public')));

// Endpoint to fetch champion names from JSON files
app.get('/champions', (req, res) => {
  const championDir = path.join(__dirname, 'data', 'individual_champion_data');

  fs.readdir(championDir, (err, files) => {
    if (err) {
      console.error(err);
      return res.status(500).send('Error reading champions directory');
    }

    const championNames = files
      .filter(file => file.endsWith('.json'))
      .map(file => file.replace('.json', ''));

    res.json(championNames);
  });
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
