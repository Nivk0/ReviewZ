import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

/*
    HOME
    Description: User must insert a valid link. If they do, then it sends request to flask to start creating all the necessary files
*/

export default function Home() {
    const navigate = useNavigate();
    const [content, setContent] = useState("")

    const handleClick = event => {

        const urlpath = String(content);

        // Request from flask to remove the old files
        axios("/remove").catch(error => {
            console.error("Error removing: ", error);
        })

        // placed here to discourage user from spamming the submit button as that would crash the program
        navigate('/analyzer')

        // Sends the request to flask to start creating the files and if an error occurs it is displayed then brings the user back to the home screen
        fetch("/url", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({url: urlpath}), //http request ?url=urlpath
        }).then(response =>  response.json()).then(data => {
            if(data["message"] !== "Collecting data from the US sites.")
            {
                alert(data["message"])
                navigate('/')
            }
            else
            {
                document.getElementById("image-prep").innerText = data["message"]
                fetch("/us-scraping").then(response => response.json()).then(data =>
                {
                    document.getElementById("image-prep").innerText = data["message"]
                    fetch("/au-scraping").then(response => response.json()).then(data =>
                    {
                        document.getElementById("image-prep").innerText = data["message"]
                        fetch("/ca-scraping").then(response => response.json()).then(data =>
                        {
                            document.getElementById("image-prep").innerText = data["message"]
                            fetch("/in-scraping").then(response => response.json()).then(data =>
                            {
                                document.getElementById("image-prep").innerText = data["message"]
                                fetch("/uk-scraping").then(response => response.json()).then(data =>
                                {
                                    document.getElementById("image-prep").innerText = data["message"]
                                    fetch("/tutorial-csv").then(response => response.json()).then(data =>
                                    {
                                        document.getElementById("image-prep").innerText = data["message"]
                                        fetch("/analyzed-csv").then(response => response.json()).then(data =>
                                        {
                                            document.getElementById("image-prep").innerText = data["message"]
                                        })
                                    })
                                })
                            })
                        })
                    })
                })
            }
        });
    };
    
    return (
        <header class="App-home">
            <h1>ReviewZ</h1>
            <p>
                Get real time feedback on how your product is doing.
            </p>
            <label>
                    Paste your Amazon url below:
            </label>
            <div>
                <input 
                    type="text" 
                    id="url_submit" 
                    value = {content}
                    onChange = {event => setContent(event.target.value)} 
                    placeHolder = "Ex. https://www.amazon.com/Remote-Control-Dancing-Imitates-Animals/dp/B0B6GJ7847/ref=puwl_atf_sccl_1/131-6402069-2006342?pd_rd_w=6XAAv&content-id=amzn1.sym.b8d6fc5b-13fe-440c-8384-29c241919e84&pf_rd_p=b8d6fc5b-13fe-440c-8384-29c241919e84&pf_rd_r=R1HV2HZZKCWCSDP7YDAM&pd_rd_wg=DEZoo&pd_rd_r=c63334db-32ed-4f7e-9a4c-705d0c5c66e6&pd_rd_i=B0B6GJ7847&th=1"
                />
                <button id="search-btn" onClick={handleClick}><span class="iconify-magnify" /></button>
            </div>
        </header>
    );
}