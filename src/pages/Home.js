import React from 'react'
import { useNavigate } from 'react-router-dom';

export default function Home()
{
    const navigate = useNavigate();
    
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
                <input type="text" name="name"/>
                <input 
                    type="submit" 
                    value="Submit" 
                    onClick={() => navigate('/analyzer')}
                />
            </form>
        </header>
    );
};