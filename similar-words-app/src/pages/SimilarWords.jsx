import React, { useState } from 'react';
import axios from 'axios';
import '../styles/SimilarWords.css';

const API_VERSION = process.env.REACT_APP_API_VERSION || 'v1';
const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

function SimilarWords() {
  const [word, setWord] = useState('');
  const [results, setResults] = useState(null);
  const [error, setError] = useState('');

  const fetchSimilarWords = async () => {
    console.log('API Base URL:', API_BASE_URL);
    console.log('API Endpoint:', `${API_BASE_URL}/api/${API_VERSION}/similar`);
    try {
      const response = await axios.get(`${API_BASE_URL}/api/${API_VERSION}/similar`, {
        params: { word },
      });
      setResults(response.data.similar);
      setError(''); // Clear any previous errors
    } catch (error) {
      setResults(null); // Clear results if there's an error
      setError(error.response?.data?.detail || error.message);
    }
  };

  return (
    <div className="similar-words-container">
      <h1 className="similar-words-title">Find Similar Words</h1>
      <div className="similar-words-input-group">
        <input
          className="similar-words-input"
          value={word}
          onChange={(e) => setWord(e.target.value)}
          placeholder="Enter a word"
        />
        <button className="similar-words-button" onClick={fetchSimilarWords}>
          Search
        </button>
      </div>
      {error && <p className="similar-words-error-message">{error}</p>}
      {results && (
        <div className="similar-words-results">
          <h2>Similar Words</h2>
          <table className="similar-words-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Word</th>
              </tr>
            </thead>
            <tbody>
              {results.map((similarWord, index) => (
                <tr key={index}>
                  <td>{index + 1}</td>
                  <td>{similarWord}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default SimilarWords;
