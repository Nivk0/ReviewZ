import React from 'react';
import './App.css';
import { BrowserRouter as Router, Routes, Route }
  from 'react-router-dom';
import Home from './pages/Home';
import Analyzer from './pages/Analyzer';
import Bullshit from './pages/Bullshit';


function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/analyzer' element={<Analyzer />} />
        <Route path='/bull' element={<Bullshit />} />
      </Routes>
    </Router>
  );
}

export default App;
