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
        <header class="App-home">
            <h1>ReviewZ</h1>
            <p>
                Get real time feedback on how your product is doing.
            </p>
            <form>
                <label>
                        Paste your Amazon url below:
                </label>
                <div>
                    <input 
                        type="text" 
                        id="url_submit" 
                        // ref={inputRef}
                        value = {content}
                        onChange = {e => setContent(e.target.value)} 
                        placeHolder = "Ex. https://www.amazon.com/Remote-Control-Dancing-Imitates-Animals/dp/B0B6GJ7847/ref=puwl_atf_sccl_1/131-6402069-2006342?pd_rd_w=6XAAv&content-id=amzn1.sym.b8d6fc5b-13fe-440c-8384-29c241919e84&pf_rd_p=b8d6fc5b-13fe-440c-8384-29c241919e84&pf_rd_r=R1HV2HZZKCWCSDP7YDAM&pd_rd_wg=DEZoo&pd_rd_r=c63334db-32ed-4f7e-9a4c-705d0c5c66e6&pd_rd_i=B0B6GJ7847&th=1"
                    />
                    <button onClick={handleClick}><span class="iconify-magnify" /></button>
                </div>
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