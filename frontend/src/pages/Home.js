import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function SetUrl (urlpath, navigate) {
    fetch("/url", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({url: urlpath}), }) //http request ?url=urlpath
    .then(function (response) {
        return response.json();
    })
    .then(function (data) {
        NumberOfReviews(data, navigate)
    })
    .catch(function (error) {
        console.log(error)
    })
}

function NumberOfReviews(data, navigate) {
    if(data["message"] !== "Preparing to mine data from the sites.")
    {
        alert(data["message"])
        navigate('/')
    }
    else
    {
        document.getElementById("image-prep").innerText = data["message"]
        fetch("/number-of-reviews")
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            getProxies(data)
        })
        .catch(function (error) {
            console.log(error)
        })
    }
}

function getProxies(data) {
    if(data["message"] === "Failed to collect the total number of reviews. Please try again.")
    {
        document.getElementById("image-prep").innerText = data["message"]
    }
    else
    {
        const maxPage = (Math.ceil(data["message"]/10.0) > 500) ? 500 : Math.ceil(data["message"]/10.0)
        fetch("/get-proxies")
        .then(function (response) {
            return response.json()
        })
        .then(function (data) {
            ScrapeSite(maxPage, data["proxies"])
        })
        .catch(function (error) {
            console.log(error)
        })
    }
}

function ScrapeSite(maxPage, proxies) {
    let pageChunks = Math.ceil(maxPage/900)
    let sec = 0
    var timer = setInterval(function percentageUpdater() {
        document.getElementById("image-prep").innerText = "Collecting the reviews, we are about " + ((sec * 100 + 1) / (Math.ceil(pageChunks / 5) * 120)).toFixed(0) + "% done."
        if ((sec + 2) === (Math.ceil(pageChunks / 5) * 120))
        {
            document.getElementById("image-prep").innerText = "Collecting the reviews, we are about " + (((sec + 1) * 100) / (Math.ceil(pageChunks / 5) * 120)).toFixed(0) + "% done."
            clearInterval(timer)
        }
        sec++
    }, 250)

    for(let page = 0; page < pageChunks; page++)
    {
        fetch("/scraper", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({"proxies": proxies, "page-start": (page * 900 + 1), "page-interval": (((maxPage - page * 900) < 900) ? (maxPage - page * 900) : 900)}), })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            clearInterval(timer)
            document.getElementById("image-prep").innerText = "Complete!"
            setLocationFilter()
        })
    }
}

function setLocationFilter() {
    fetch('/location-filter')
    .then(function (response) {
        return response.json()
    })
    .then(function (data) {
        var locationFilter = "<option value=''></option>"
        let locations = data["locations"]
        locations.forEach(location => {
            locationFilter += "<option value='" + location + "'>" + getCaptializedWords(location) + "</option>"
        })
        document.getElementById("location-filter").innerHTML = locationFilter
    })
}

function getCaptializedWords(words) {
    let capitalizedWords = ""
    for (let word of words.split(" "))
    {
        capitalizedWords += word.charAt(0).toUpperCase() + word.substring(1) + " "
    }
    return capitalizedWords
}

/*
    HOME
    Description: User must insert a valid link. If they do, then it sends request to flask to start creating all the necessary files
*/

export default function Home() {
    const navigate = useNavigate();
    const [content, setContent] = useState("")

    document.getElementById("theme-color").setAttribute("content", "#1B263B") //error

    const handleClick = event => {

        const urlpath = String(content);

        // Request from flask to remove the old files
        axios("/remove").catch(error => {
            console.error("Error removing: ", error);
        })

        // placed here to discourage user from spamming the submit button as that would crash the program
        navigate('/analyzer')

        // Sends the request to flask to start creating the files and if an error occurs it is displayed then brings the user back to the home screen
        SetUrl(urlpath, navigate)

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