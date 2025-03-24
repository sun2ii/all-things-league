const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.static('public'));

app.get('/champion', (req, res) => {
  const championName = req.query.name;
  if (!championName) {
    return res.status(400).send('Champion name is required');
  }
  const championFilePath = path.join(__dirname, 'data', 'champion.json');
  fs.readFile(championFilePath, 'utf-8', (err, fileData) => {
    if (err) {
      console.error(err);
      return res.status(500).send('Unable to read champion.json');
    }
    try {
      const champions = JSON.parse(fileData);
      const championData = champions.data[championName];
      if (!championData) {
        return res.status(404).send('Champion not found');
      }
      res.json(championData);
    } catch (parseError) {
      console.error(parseError);
      res.status(500).send('Invalid JSON in champion.json');
    }
  });
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
