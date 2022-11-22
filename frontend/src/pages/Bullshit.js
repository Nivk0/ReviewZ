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
  const [content, setContent] = useState("")
  const [data, setData] = useState("")
  const [loading, setLoading] = useState(true)

  const handleClick = event => {
    // const url = (inputRef.current.value);
    const urlpath = String(content);

    alert(urlpath);
};

  axios("http://127.0.0.1:5000/remove").then(response => {
    setData(response.data)
  }).catch(error => {
    console.error("Error removing: ", error);
  }).finally(() => {
    setLoading(false);
  })

  return (
    <header class="App-header">
            <h1>Bull</h1>
            <p id="para">
              {data}
            </p>
            <form>
                <label>
                        Paste your Amazon url below:
                </label>
                <input 
                    type="text" 
                    id="url_submit" 
                    // ref={inputRef}
                    value = {content}
                    onChange = {e => setContent(e.target.value)} 
                />
                <button onClick={handleClick}> 
                    Submit 
                </button>
            </form> 
        </header>
  );

}