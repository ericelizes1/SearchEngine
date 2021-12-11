import logo from './goggleglogo.svg';
import './App.css';
import React, { useEffect, useState } from "react";
import { flushSync } from 'react-dom';


function App() {

  // sets tab title to 'Goggle'
  useEffect(() => {
    document.title = "Goggle"
  }, []);

  // var result = []
  const [result, setResult] = useState([]);
  return (
    <div className="App">
      <header className="App-header">
        <div className="NameContainer">
        </div>
        <div style={{paddingLeft: '20%', paddingRight: '20%'}}className="SearchContainer">
          <img src={logo} className="App-logo" alt="logo" />
          <input className="SearchBar" id="searchBar" placeholder="Search word here"/>
          <button onClick={() => {
            const input = document.getElementById("searchBar").value;     //query input
            console.log(input);

            // sends input keyword to index.js to present to server; then logs output (in form of array)
            fetch("http://localhost:3002?keyword=" + input)
              .then(res => res.json())
              .then((out) => {
                //console.log('OUT BELOW')
                //console.log(out)
                setResult(out)
                console.log(result);
              })
              .catch(err => {
                throw err
              })
          }}>Search</button>
        </div>
      </header>
      <div>
        <GenerateOutput arr={result}/>
      </div>
    </div>
  );
}

// generates the list of links, titles, and descriptions relevant to output
function GenerateOutput(props) {
  const raw_output = props.arr
  const output = []
  
  if (raw_output == null || raw_output.length == 0) {
    //console.log()
    output.push(<p align='center'>No Results Found</p>)
  }
  else {
    for (let i = 0; i < Math.min(raw_output.length, 10); i++) {
      output.push(<SearchOutput title={raw_output[i][0]} link={raw_output[i][1]} desc={raw_output[i][2]}/>)
      console.log(raw_output[i][1]);
    }
  }

  return output;
}

// returns and prints the titles and descriptions of each relevant link
function SearchOutput(props) {
  return (
    <div className="SearchOutput" 
         align='left'
         style={{paddingLeft: '20%', 
                 paddingRight: '20%', 
                 paddingBottom: 20,}}>
      <a target="_blank"
       href={props.link}
       style={{
         fontSize: 20
       }}>{props.title}</a>
      <p>{props.desc}</p>
    </div>
  );
}

export default App;
