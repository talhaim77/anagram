import React, { useState } from 'react';
import axios from 'axios';
import '../styles/AddWord.css';

const API_VERSION = process.env.REACT_APP_API_VERSION || 'v1';
const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

function AddWord() {
  const [word, setWord] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const addWord = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/${API_VERSION}/add-word`, { word });
      setSuccessMessage(response.data.message);
      setErrorMessage('');
      setWord('');
    } catch (error) {
      setErrorMessage(error.response?.data?.detail || error.message);
      setSuccessMessage('');
    }
  };

  return (
    <div className="add-word-container">
      <h1 className="add-word-title">Add a New Word</h1>
      <form className="add-word-form" onSubmit={(e) => { e.preventDefault(); addWord(); }}>
        <input
          type="text"
          className="add-word-input"
          value={word}
          onChange={(e) => setWord(e.target.value)}
          placeholder="Enter a new word"
        />
        <button type="submit" className="add-word-button">Add Word</button>
      </form>
      {successMessage && <p className="add-word-success-message">{successMessage}</p>}
      {errorMessage && <p className="add-word-error-message">{errorMessage}</p>}
    </div>
  );
}

export default AddWord;
