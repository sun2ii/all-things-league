const express = require('express');
const axios = require('axios');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
const port = 8000;

const apiKey = process.env.REACT_APP_RIOT_API_KEY;

app.get('/', (req, res) => {
    res.send('Hello from the backend!');
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
