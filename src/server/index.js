const express = require('express')
const app = express()
const port = 3002
var fs = require('fs')
var cors = require('cors')
const eol = require('eol')

var os = require('os')

app.use(cors()) 

var data, inv

app.get('/', (req, res) => {
res.setHeader('Content-Type', 'application/json');
kw = req.query.keyword

// read files

data = fs.readFileSync("data.csv",{encoding:'utf8', flag:'r'})
inv = fs.readFileSync("inv_freq.csv",{encoding:'utf8', flag:'r'})

/*
let data = '';

const readStreamD = fs.createReadStream('spiderdata.csv');

readStreamD.on('data', function(chunk) {
  data += eol.auto(chunk.toString('utf8'));
});

readStreamD.on('end', function() {
  console.log('finished reading');
});

let inv = '';

const readStreamI = fs.createReadStream('inv_freq2.csv');

readStreamI.on('ift', function(chunk) {
  inv += eol.auto(chunk.toString('utf8'));
});

readStreamI.on('end', function() {
  console.log('finished reading');
});
*/

// clean spider data

data = data.split('\r\n')
newdata = []
for(i = 0; i < data.length; i++){
    line = data[i].split('~')
    newdata.push([line[0],line[1],line[2]])
}
newdata.shift() // remove bad first element
for(i = 0; i < newdata.length; i++){
    if (newdata[i][0] != undefined && newdata[i][0] != undefined)
    data.push(newdata[i])
}

data = newdata

// clean invserse freq data

inv = inv.split('\r\n')
newinv = []
for(i = 0; i < inv.length; i++){
    line = inv[i].split('~')
 
if (line[1] != undefined){
    line[1] = line[1].replace(/\(/g,'[')
    line[1] = line[1].replace(/\)/g,']')
    line[1] = line[1].replace(/\'/g,'\"')
    line[1] = JSON.parse(line[1])
}
newinv.push(line)
}
 
inv = newinv
 
// build result data structure
debugger;
// lowercase the input keyword

kw = kw.trim()
kw = kw.toLowerCase()

// find the word in the inv_freq array 
// stores its list of links and frequencies
var msg = "Oh no! We can't find that word!"

for(i = 0; i < inv.length;i++){
    if (inv[i][0] == kw){
        msg = inv[i][1]
        break
    }
}

// returns if word is not found in data frame
if (msg == "Oh no! We can't find that word!"){
    res.send(msg)
    return
}

// finds the links and their associated titles and descriptions
// stores them to be outputted
output = []

for(i = 0; i < msg.length; i++)
    for(j = 0; j < data.length; j++)
        if (msg[i][0] == data[j][1])
            output.push([data[j][0],data[j][1],data[j][2],msg[i][1]])

    console.log("index.js out: ")
    console.log(output)

    res.send(JSON.stringify(output))
})

app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`)
})
