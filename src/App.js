import React from 'react';
import './App.css';
import { BrowserRouter as Router, Routes, Route }
  from 'react-router-dom';
import Home from './pages/Home';
import Analyzer from './pages/Analyzer';

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path='/' element={<Home />} />
        <Route exact path='/analyzer' element={<Analyzer />} />
      </Routes>
    </Router>
  );
}

export default App;
