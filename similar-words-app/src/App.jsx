import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import './assets/style.css';
import HomePage from './pages/HomePage';
import SimilarWords from './pages/SimilarWords';
import Stats from './pages/Stats';
import AddWord from './pages/AddWord';


function App() {
  return (
    <Router>
      <div id="app">
        <nav>
          <Link to="/">Home</Link> |
          <Link to="/similar">Find Similar Words</Link> |
          <Link to="/stats">Stats</Link> |
          <Link to="/add-word">Add Word</Link>
        </nav>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/similar" element={<SimilarWords />} />
          <Route path="/stats" element={<Stats />} />
          <Route path="/add-word" element={<AddWord />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;