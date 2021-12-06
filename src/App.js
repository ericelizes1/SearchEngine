import logo from './goggleglogo.svg';
import './App.css';
import React, { useEffect, useState } from "react";
import { flushSync } from 'react-dom';


function App() {

  // sets tab title to 'Goggle'
  useEffect(() => {
    document.title = "Goggle"
  }, []);

  const[result, setResult] = useState([]);

  return (
    <div className="App">
      <header className="App-header">
        <div className="NameContainer">
        </div>
        <div className="SearchContainer">
          <img src={logo} className="App-logo" alt="logo" />
          <input className="SearchBar" id="searchBar" placeholder="Search word here"/>
          <button onClick={() => setResult(Query())}>Search</button>
        </div>
      </header>
      <GenerateOutput arr={result}/>
    </div>
  );
}

// queries the inverse frequency table and data of links from spider output to return relevant results
function Query() {
  const input = document.getElementById("searchBar").value;     //query input
  console.log(input);
  const output = []

  // sends input keyword to index.js to present to server; then logs output (in form of array)
  fetch("http://localhost:3002?keyword=" + input)
    .then(res => res.json())
    .then((out) => {
      if (out.length == 1) {
        output.push(out);
      }
      else {
        for (let i = 0; i < out.length; i++) {
          let title = out[i][0]
          let link = out[i][1]
          let desc = out[i][2]
          output.push([title, link, desc])
        }
        
      } 
    })
    .catch(err => {
      throw err
    });

  console.log(output[0]);
  return output;
}

// generates the list of links, titles, and descriptions relevant to output
function GenerateOutput(props) {
  const raw_output = props.arr
  const output = []
  
  if (raw_output == null || raw_output.length == 0) {
    output.push(<p>No Results Found</p>)
  }
  else {
    for (let i = 0; i < raw_output.length; i++) {
      output.push(<SearchOutput title={raw_output[i][0]} link={raw_output[i][1]} desc={raw_output[i][2]}/>)
      console.log(raw_output[i][1]);
    }
  }

  return output;
}

// returns and prints the titles and descriptions of each relevant link
function SearchOutput(props) {
  return (
    <div className="SearchOutput">
      <a target="_blank" href={props.link}>{props.title}</a>
      <p>{props.desc}</p>
    </div>
  );
}

export default App;