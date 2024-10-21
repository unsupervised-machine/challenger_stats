import React, { useEffect, useState } from 'react';
import './LadderComponent.css'; // Import CSS for styling
import { LazyLoadImage } from 'react-lazy-load-image-component';

const LadderComponent = () => {
  const [ladderData, setLadderData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sortOrder, setSortOrder] = useState('desc');

  useEffect(() => {
    const fetchLadderData = async () => {
      try {
        const response = await fetch('http://localhost:8001/api/ladder'); // Update this to your actual ladder route
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setLadderData(data);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    fetchLadderData();
  }, []);

  const handleSort = () => {
    setSortOrder((prevOrder) => (prevOrder === 'asc' ? 'desc' : 'asc'));
  };

  const sortedLadderData = [...ladderData].sort((a, b) => {
    return sortOrder === 'asc'
      ? a.leaguePoints - b.leaguePoints
      : b.leaguePoints - a.leaguePoints;
  });

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  return (
    <div className="ladder-container">
      <h2>Player Ladder</h2>
      <button onClick={handleSort}>
        Sort by League Points: {sortOrder === 'asc' ? 'Ascending' : 'Descending'}
      </button>
      <ul className="ladder-list">
        {sortedLadderData.map((player) => (
          <li key={player._id} className="ladder-item">
            <LazyLoadImage
              src={`https://ddragon.leagueoflegends.com/cdn/12.18.1/img/profileicon/${player.player_ids_data.profileIconId}.png`}
              alt="Player Icon"
              className="player-icon"
              effect="blur"
            />
            <div className="player-info">
              <strong>Player Name:</strong> {player.player_ids_data.gameName}#{player.player_ids_data.tagLine}
              <br />
              <strong>Tier:</strong> {player.tier}
              <br />
              <strong>League Points:</strong> {player.leaguePoints}
              <br />
              <strong>Win Rate:</strong> {player.player_summarized_stats_data?.average_win_rate
                ? (player.player_summarized_stats_data.average_win_rate * 100).toFixed(2) + '%'
                : 'N/A'}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default LadderComponent;
