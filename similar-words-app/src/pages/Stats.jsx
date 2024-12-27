import React, { useState } from 'react';
import axios from 'axios';
import '../styles/Stats.css';

const API_VERSION = process.env.REACT_APP_API_VERSION || 'v1';
const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

function Stats() {
  const [stats, setStats] = useState(null);

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/${API_VERSION}/stats`);
      setStats(response.data);
    } catch (error) {
      alert('Error fetching stats: ' + (error.response?.data?.detail || error.message));
    }
  };

  return (
    <div className="stats-container">
      <h1 className="stats-title">Service Statistics</h1>
      <button className="stats-button" onClick={fetchStats}>
        Fetch Stats
      </button>
      {stats && (
        <div className="stats-card">
          <div className="stat">
            Total Words: <span>{stats.totalWords.toLocaleString()}</span>
          </div>
          <div className="stat">
            Total Requests: <span>{stats.totalRequests}</span>
          </div>
          <div className="stat">
            Average Processing Time (ms): <span>{stats.avgProcessingTimeMs}</span>
          </div>
        </div>
      )}
    </div>
  );
}

export default Stats;
