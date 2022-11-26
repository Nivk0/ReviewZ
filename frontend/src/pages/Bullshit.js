import React, { useEffect, useState } from 'react';

function GraphOptions() {
  const [open, setOpen] = React.useState(false);

  const handleOpen = () => {
    setOpen(!open);
    (document.getElementById('dropdown').getAttribute('class') == "iconify-dropdown") ? 
    (document.getElementById('dropdown').setAttribute('class', "iconify-dropdown-180")) :
    (document.getElementById('dropdown').setAttribute('class', "iconify-dropdown"));
  };
  
  return (
    <div class="App-analyzer">
      <div class="App-sidebar">
        <GraphOptionsDropdown
          open={open}
          trigger={ <button onClick={handleOpen}>
                      <span id="dropdown" class="iconify-dropdown" />
                    </button>}
          menu={[
            (<label class="graph-choices">
              <p>Histogram</p>
              <input type="radio" name="Graphs" id="HIST" value="analyzed_histogram.svg" /* onChange={handleChange} */ />
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
              <input type="radio" name="Graphs" id="HM" value="analyzed_heatmap.svg" /*onChange={handleChange} */ />
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
      </div>
    </div>
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

export default GraphOptions