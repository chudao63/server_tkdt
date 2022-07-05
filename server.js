// Import:
const express = require('express');
const app = express();
const PORT = 80;

//Static File:
app.use(express.static('fontEnd'))
app.use('/css', express.static(__dirname + 'fontEnd/css'))
app.use('/js', express.static(__dirname + 'fontEnd/js'))
app.use('/img', express.static(__dirname + 'fontEnd/img'))
app.use('/txt', express.static(__dirname + 'fontEnd/txt'))

app.get('/home', (req, res) =>{
    res.sendFile(__dirname + '/fontEnd/home.html')
});
app.get('/monitor', (req, res) =>{
    res.sendFile(__dirname + '/fontEnd/monitor.html')
});



app.listen(PORT,() =>{
    console.log(`Server starting at http://localhost:${PORT}/`)
});
