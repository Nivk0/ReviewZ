import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom';

/*
    TOP BAR
*/

function TopBar() {
    return(
        <div class="App-topbar">
            <HomeButton />
            <h1>ReviewZ</h1>
        </div>
    );
}

// Returns to the home screen
function HomeButton() {
    const navigate = useNavigate();
    return(
        <button onClick={ () => navigate('/')}>
            <span class="iconify-home" />
        </button>
    )
}

/*
    LOCATION FILTER
    Description: Create the select box for the different regions and when there is a change the filter is updated
*/

let locationFilter; // used to send flask the location filter selected
function Location() {
    const [location, setLocation] = useState('');
    let locations = [];
    locations.push(<option value={''}>{''}</option>)
    locations.push(<option value={'australia'}>{'Australia'}</option>)
    locations.push(<option value={'canada'}>{'Canada'}</option>)
    locations.push(<option value={'india'}>{'India'}</option>)
    locations.push(<option value={'the united kingdom'}>{'The United Kingdom'}</option>)
    locations.push(<option value={'the united states'}>{'The United States'}</option>)
    
    // If the html changes then value of that change(event) is set with setMonth
    const handleChange = event => {
        event.preventDefault()
        setLocation(event.target.value)
        locationFilter = String(event.target.value) // locationfilter initiliazed here
    };
    
    return(
        <label class="filter-choices">
            <p>Region</p>
            <select id="location-filter" value={location} onChange={handleChange}>
                { locations }
            </select>
        </label>
    );
}

/*
    MONTH FILTER
    Description: Creates the selection box each month and when there is a change the filter is updated
*/

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

    // If the html changes then value of that change(event) is set with setMonth
    const handleChange = event => {
        setMonth(event.target.value);
        monthFilter = String(event.target.value); // monthfilter initialized here
    };

    return(
        <label class="filter-choices">
            <p>Month</p>
            <select value={month} onChange={handleChange}>
                { months }
            </select>
        </label>
    );
}

/*
    FILTER OPTIONS
*/

// The backbone of the filter dropdown. If open is true then the filter choices are displayed
function FilterOptionsDropdown({open, trigger, menu}) {
    return (
      <div class="filter-options">
        <h1>Filters{trigger} </h1>
        {open ? (<> {menu} </>) : null}
      </div>
    );
}

/*  
    This is where filteroptionsdropdown is declared. Trigger is the button that causes teh filter to go up and down. 
    The menu is the filter choices--location and month. If another filter were to be added it would go under menu.
*/
function FilterOptions() {
    const [open, setOpen] = React.useState(true);

    const handleOpen = () => {
      setOpen(!open);
      // When the open button is clicked the filter icon flips via css
      (document.getElementById('filter-dropdown').getAttribute('class') === "iconify-dropdown") ? 
      (document.getElementById('filter-dropdown').setAttribute('class', "iconify-dropdown-180")) :
      (document.getElementById('filter-dropdown').setAttribute('class', "iconify-dropdown"));
    };

    return (
        <>
          <FilterOptionsDropdown
            open={open}
            trigger={ <button onClick={handleOpen}>
                        <span id="filter-dropdown" class="iconify-dropdown-180" />
                        </button>}
            menu={[
                (<Location />),
                (<Month />),
            ]}
          />
        </>
      );
}

/*
    GRAPH OPTIONS
*/

// Declared here to be used globally
let filename = "";

/* 
    Uses the GraphOptionsDropdown function. The menu for this dropdown are the graph options--histogram and heat map. 
    The radio buttons check boxes are made out of svg elements and uses CSS to put the svgs on top of each other.    
*/
function GraphOptions() {
    const [open, setOpen] = React.useState(true);
  
    // When a radio button is changed, its value is added to filename variable
    const handleChange = event => {
        filename = '/image/' + event.target.value;
    };

    const handleOpen = () => {
      setOpen(!open);
      // When the open button is clicked the filter icon flips via css
      (document.getElementById('graph-dropdown').getAttribute('class') === "iconify-dropdown") ? 
      (document.getElementById('graph-dropdown').setAttribute('class', "iconify-dropdown-180")) :
      (document.getElementById('graph-dropdown').setAttribute('class', "iconify-dropdown"));
    };
    
    return (
      <>
        <GraphOptionsDropdown
        open={open}
        trigger={ <button onClick={handleOpen}>
                    <span id="graph-dropdown" class="iconify-dropdown-180" />
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
  
// The backbone of the graph choices dropdown. If open is true then the graph choices are displayed
function GraphOptionsDropdown({open, trigger, menu}) {
    return (
        <div class="graph-options">
        <h1>Graph Options {trigger} </h1>
        {open ? (<> {menu} </>) : null}
        </div>
    );
}

/*
    ANALYZER
    Puts everything above together and fetches the new image from flask
*/

export default function Analyzer() {

    document.getElementById("theme-color").setAttribute("content", "#415A77")
    document.getElementById("viewport").setAttribute("content", "width=device-width, height=device-height, initial-scale=1, maximum-scale=1")

    const onClick = event => {
        locationFilter = document.getElementById("location-filter").value
        // sends location and month to flask to create a new filtered image
        fetch("/filterupdate", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({location: locationFilter, month: monthFilter}),
        }).then((response) => response.json()).then((data) => { 
            document.getElementById('image-prep').innerText = ""
            let message = data['message']
            // if analyzed csv file has not been created then it tells the user to be patient
            if (message !== "Success")
            {
                message = data['message']
                document.getElementById('image-prep').innerText = message
            }
            else
            {
                // fetches the images using filename created above. 
                // fetch put on this level to prevent flask from searching for an image before its created
                fetch(filename) 
                .then(function(data){
                    // blob is used for data types that are not text or json
                    return data.blob();
                })
                .then(blob => {
                    var img = URL.createObjectURL(blob);
                    document.getElementById('graph').setAttribute('src', img);
                })
            }
        });
    };

    return (
        <header class="App-analyzer">
            <TopBar />
            <div class="App-sidebar">
                <GraphOptions />
                <FilterOptions />
                <button class="btn-apply" onClick={onClick} >Apply</button>
            </div>
            <div class="App-main">
            <img src="" id="graph" alt="" width="500px"></img>
                <p id="image-prep" class="image-prep"></p>
            </div>
        </header> 
    );
}