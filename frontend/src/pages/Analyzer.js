import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom';

function HomeButton() {
    const navigate = useNavigate();
    return(
        <button onClick={ () => navigate('/')}>
            <span class="iconify-home" />
        </button>
    )
}

function Location() {
    const [location, setLocation] = useState('');
    let locations = [];
    locations.push(<option value={''}>{''}</option>)
    locations.push(<option value={'the united states'}>{'the united states'}</option>)
    locations.push(<option value={'canada'}>{'canada'}</option>)
    locations.push(<option value={'australia'}>{'australia'}</option>)
    locations.push(<option value={'india'}>{'india'}</option>)
    
    const handleChange = event => {
        event.preventDefault()
        setLocation(event.target.value)
    };
    
    return(
        <div>
            <form>
                <label>
                    Location
                    <select value={location} onChange={handleChange}>
                        { locations }
                    </select>
                </label>
            </form>
        </div>
    );
}

function Month() {
    const [month, setMonth] = useState('');
    let months = [];
    months.push(<option value={''}>{''}</option>)
    months.push(<option value={'1'}>{'January'}</option>)
    months.push(<option value={'2'}>{'February'}</option>)
    months.push(<option value={'3'}>{'March'}</option>)
    months.push(<option value={'4'}>{'April'}</option>)
    months.push(<option value={'5'}>{'May'}</option>)
    months.push(<option value={'6'}>{'June'}</option>)
    months.push(<option value={'7'}>{'July'}</option>)
    months.push(<option value={'8'}>{'August'}</option>)
    months.push(<option value={'9'}>{'September'}</option>)
    months.push(<option value={'10'}>{'October'}</option>)
    months.push(<option value={'11'}>{'November'}</option>)
    months.push(<option value={'12'}>{'December'}</option>)

    
    const handleChange = event => {
        setMonth(event.target.value);
        
    };
    return(
        <div>
            <form>
                <label>
                    Month of Review
                    <select value={month} onChange={handleChange}>
                        { months }
                    </select>
                </label>
            </form>
        </div>
    );
}




function Filters() {
    return(
        <div class="filters">
            <h1>Filters</h1>
            <Location />
            <Month />
        </div>
    );
}

function TopBar() {
    return(
        <div class="App-topbar">
            <HomeButton />
            <h1>ReviewZ</h1>
        </div>
    );
}

function GraphOption() {
    const [graphOption, setGraphOption] = useState('Histogram');
    let graphOptions = [];
    graphOptions.push(<option value={'Histogram'}>{'Histogram'}</option>)
    graphOptions.push(<option value={'Heat Map'}>{'Heat Map'}</option>)

    const handleChange = event => {
        setGraphOption(event.target.value);
    };
    return(
        <div class="graph-options">
            <h1>Graph Options</h1>
            <form>
                <label>
                    <p>Histogram</p>
                    <input type="radio" name="Graphs" value="analyzed_histogram.svg" id="HIST" />
                </label>
                <label>
                    <p>Heat Map</p>
                    <input type="radio" name="Graphs" value="analyzed_heatmap.svg" id="HM" />
                </label>
                
                {/* <label>
                    Graph Option
                    <select value={graphOption} onChange={handleChange}>
                        { graphOptions }
                    </select>
                </label> */}
            </form>
        </div>
    );
}

export default function Analyzer() {
    const SVG = (() => {
        if(document.getElementById('HIST').checked) {
            alert(document.getElementById('HIST').value)
            return document.getElementById('HIST').value
        }
        else {
            alert(document.getElementById('HM').value)
            return document.getElementById('HM').value
        }
    });

    const onClick = event => (
        fetch('http://127.0.0.1:5000/image/' + SVG)
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
          document.getElementById('graph').setAttribute('src', img);
        })
    );

    return (
        <header class="App-analyzer">
            <TopBar />
            <div class="App-sidebar">
                <GraphOption />
                <Filters />
                <button id="btn" onClick={onClick} >Get Image</button>
            </div>
            <img src="" id="graph" alt=""  width="500px" />
            <div id="progress"></div>
        </header> 
    );
}