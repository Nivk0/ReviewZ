import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function HomeButton() {
    const navigate = useNavigate();
    return(
        <button onClick={ () => navigate('/')}>
            <span class="iconify-home" />
        </button>
    )
}

let locationFilter;
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
        locationFilter = String(event.target.value)
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

let monthFilter;
function Month() {
    const [month, setMonth] = useState('');
    let months = [];
    months.push(<option value={''}>{''}</option>)
    months.push(<option value={'January'}>{'January'}</option>)
    months.push(<option value={'February'}>{'February'}</option>)
    months.push(<option value={'March'}>{'March'}</option>)
    months.push(<option value={'April'}>{'April'}</option>)
    months.push(<option value={'May'}>{'May'}</option>)
    months.push(<option value={'June'}>{'June'}</option>)
    months.push(<option value={'July'}>{'July'}</option>)
    months.push(<option value={'August'}>{'August'}</option>)
    months.push(<option value={'September'}>{'September'}</option>)
    months.push(<option value={'October'}>{'October'}</option>)
    months.push(<option value={'November'}>{'November'}</option>)
    months.push(<option value={'December'}>{'December'}</option>)

    
    const handleChange = event => {
        setMonth(event.target.value);
        monthFilter = String(event.target.value);
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

let filename = "";

function GraphOptions() {
    const [open, setOpen] = React.useState(true);
  
    const handleChange = event => {
        filename = 'http://127.0.0.1:5000/image/' + event.target.value;
    };

    const handleOpen = () => {
      setOpen(!open);
      (document.getElementById('dropdown').getAttribute('class') == "iconify-dropdown") ? 
      (document.getElementById('dropdown').setAttribute('class', "iconify-dropdown-180")) :
      (document.getElementById('dropdown').setAttribute('class', "iconify-dropdown"));
    };
    
    return (
      <>
        <GraphOptionsDropdown
        open={open}
        trigger={ <button onClick={handleOpen}>
                    <span id="dropdown" class="iconify-dropdown-180" />
                    </button>}
        menu={[
            (<label class="graph-choices">
            <p>Histogram</p>
            <input type="radio" name="Graphs" id="HIST" value="analyzed_histogram.svg" onChange={handleChange} />
            <svg class="unchecked" xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" preserveAspectRatio="xMidYMid meet" viewBox="0 0 24 24">
                <path fill="white" d="M19 3H5c-1.11 0-2 .89-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2m0 2v14H5V5h14Z"/>
            </svg>
            <svg class="checked" xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" preserveAspectRatio="xMidYMid meet" viewBox="0 0 32 32">
                <path fill="white" d="M26 4H6a2 2 0 0 0-2 2v20a2 2 0 0 0 2 2h20a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2ZM14 21.5l-5-4.957L10.59 15L14 18.346L21.409 11L23 12.577Z"/>
                <path fill="none" d="m14 21.5l-5-4.957L10.59 15L14 18.346L21.409 11L23 12.577Z"/>
            </svg>
            </label>),
            (<label class="graph-choices">
            <p>Heat Map</p>
            <input type="radio" name="Graphs" id="HM" value="analyzed_heatmap.svg" onChange={handleChange} />
            <svg class="unchecked" xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" preserveAspectRatio="xMidYMid meet" viewBox="0 0 24 24">
                <path fill="white" d="M19 3H5c-1.11 0-2 .89-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2m0 2v14H5V5h14Z"/>
            </svg>
            <svg class="checked" xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" preserveAspectRatio="xMidYMid meet" viewBox="0 0 32 32">
                <path fill="white" d="M26 4H6a2 2 0 0 0-2 2v20a2 2 0 0 0 2 2h20a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2ZM14 21.5l-5-4.957L10.59 15L14 18.346L21.409 11L23 12.577Z"/>
                <path fill="none" d="m14 21.5l-5-4.957L10.59 15L14 18.346L21.409 11L23 12.577Z"/>
            </svg>
            </label>),
        ]}
        />
      </>
    );
  }
  
  function GraphOptionsDropdown({open, trigger, menu}) {
    return (
      <div class="graph-options">
        <h1>Graph Options {trigger} </h1>
        {open ? (<> {menu} </>) : null}
      </div>
    );
  }

export default function Analyzer() {

    const onClick = event => {
        fetch("http://127.0.0.1:5000/filterupdate", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({location: locationFilter, month: monthFilter}), //http request ?url=urlpath
        }).then((response) => {
            fetch(filename) 
            .then(function(data){
                return data.blob();
            })
            .then(blob => {
                var img = URL.createObjectURL(blob);
                document.getElementById('graph').setAttribute('src', img);
            })
        });
    };

    return (
        <header class="App-analyzer">
            <TopBar />
            <div class="App-sidebar">
                <GraphOptions />
                <Filters />
                <button class="btn-apply" onClick={onClick} >Apply</button>
            </div>
            <div class="App-main">
                <img src="" id="graph" alt="" width="500px"></img>
            </div>
        </header> 
    );
}