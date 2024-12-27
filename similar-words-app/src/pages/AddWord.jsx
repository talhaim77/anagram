import React, { useState } from 'react';
import axios from 'axios';
import '../styles/AddWord.css';


const API_VERSION = process.env.REACT_APP_API_VERSION || 'v1';
const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

function AddWord() {
  const [word, setWord] = useState('');

  const addWord = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/${API_VERSION}/add-word`, { word });
      alert(response.data.message);
      setWord('');
    } catch (error) {
      alert('Error adding word: ' + (error.response?.data?.detail || error.message));
    }
  };

  return (
    <div>
      <h1>Add a New Word</h1>
      <input value={word} onChange={(e) => setWord(e.target.value)} placeholder="Enter a new word" />
      <button onClick={addWord}>Add Word</button>
    </div>
  );
}

export default AddWord;