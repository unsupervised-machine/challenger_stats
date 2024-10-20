// PlayerStats.js
import React, { useEffect, useState } from 'react';

const PlayerStats = () => {
  const [playerStats, setPlayerStats] = useState([]);

  useEffect(() => {
    const fetchPlayerStats = async () => {
      try {
        const response = await fetch('http://localhost:8001/api/player-stats'); // Update this to your actual player stats route
        const data = await response.json();
        setPlayerStats(data);
      } catch (error) {
        console.error('Error fetching player stats:', error);
      }
    };

    fetchPlayerStats();
  }, []);

  return (
    <div>
      <h2>Player Stats</h2>
      <ul>
        {playerStats.map((player) => (
          <li key={player._id}>
            <strong>Kills:</strong> {player.average_kills}, 
            <strong>Deaths:</strong> {player.average_deaths}, 
            <strong>Assists:</strong> {player.average_assists}, 
            <strong>Match Count:</strong> {player.match_count}, 
            <strong>Win Rate:</strong> {(player.average_win_rate * 100).toFixed(2)}%
          </li>
        ))}
      </ul>
    </div>
  );
};

export default PlayerStats;