import React from 'react';
import './App.css';
import { BrowserRouter as Router, Routes, Route }
  from 'react-router-dom';
import Home from './pages/Home';
import Analyzer from './pages/Analyzer';

function BrowserVH()
{
  window.addEventListener('resize', () => {
    let vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
  });
}

function App() {
  return (
    <Router class>
      <Routes id>
        {BrowserVH()}
        <Route path='/' element={<Home />} />
        <Route path='/analyzer' element={<Analyzer />} />
      </Routes>
    </Router>
  );
}

export default App;
