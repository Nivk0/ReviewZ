import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Sup()
{
  const [getMessage, setGetMessage] = useState('');

  useEffect(()=>{
    axios.get('http://127.0.0.1:5000/picture').then(response => {
      console.log("SUCCESS", response)
      setGetMessage(response)
    }).catch(error => {
      console.log(error)
    })

  }, [])

alert(getMessage.data.message)

  return (
    <header class="App-header">
        <h1>sup</h1>
        <div>
          <img src={require(getMessage.data.message)} width="500px"></img>
        </div>
    </header>
  );
}


export default function Bull(){
  return (
    <header>
      <div><Sup /></div>
    </header>
    
  );

}