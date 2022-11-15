import React, { useEffect, useState } from 'react';
import axios from 'axios';
import $ from 'jquery';

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

  const onClick = event => (
    fetch('http://127.0.0.1:5000/get_image?type=1')
      .then(function(data){
      document.getElementById('progress').textContent = "Loading";
      return data.blob();
    })
    .then(blob => {
      var img = URL.createObjectURL(blob);
      // const dd = imagesrc
      // $('#progress').text("");
      // $('img').attr('src', dd);
      document.getElementById('progress').textContent = "Loaded"
      document.getElementById('test').setAttribute('src', img);
    })
  );

  return (
    <header class="App-header">
      {/* <div><Sup /></div> */}
      <button id="btn" onClick={onClick} >Get Image</button>
      <img src="" id="test" alt=""  width="500px" />
      <div id="progress"></div>
      <script></script>
    </header>
    
  );

}