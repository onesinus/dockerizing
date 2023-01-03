'use strict';

const express = require('express');
const mysql = require('mysql')

// Constants
const PORT = 8080;
const HOST = '0.0.0.0';

// App
const app = express();
app.get('/', (req, res) => {
  res.send('Hello World');
});

app.get('/connect-db', (req, res) => {
  const connection = mysql.createConnection({
    host: 'db',
    user: 'root',
    password: 'barbar',
    database: 'express-db'
  })

  connection.connect()

  connection.query('SELECT * FROM users', (err, rows, fields) => {
    if (err) throw err

    console.log('The solution is: ', rows)
  })

  connection.end()
  res.send('Connect to db')
})

app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`);