import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom';


function Body()
{
    const navigate = useNavigate();
    // const inputRef = useRef(null);
    const [content, setContent] = useState("")

    const handleClick = event => {
        // const url = (inputRef.current.value);

        const urlpath = String(content);

        const response = fetch("http://127.0.0.1:5000/url", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({url: urlpath}), //http request ?url=urlpath
        });
    
        alert(urlpath);

        navigate('/analyzer')
    };


    
    return (
        <header class="App-header">
            <h1>ReviewZ</h1>
            <p>
                Get real time feedback on how your product is doing.
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

export default function Home()
{
    return(
        <Body />
    );
};