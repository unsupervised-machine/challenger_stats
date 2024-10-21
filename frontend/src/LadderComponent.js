// LadderComponent.js
import React, { useEffect, useState } from 'react';

const LadderComponent = () => {
  const [ladderData, setLadderData] = useState([]);

  useEffect(() => {
    const fetchLadderData = async () => {
      try {
        const response = await fetch('http://localhost:8001/api/ladder'); // Update this to your actual ladder route
        const data = await response.json();

        // Print the fetched data to the console
        console.log("Fetched ladder data:", data);

        setLadderData(data);
      } catch (error) {
        console.error('Error fetching ladder data:', error);
      }
    };

    fetchLadderData();
  }, []);

  return (
    <div>
      <h2>Player Ladder</h2>
      <ul>
        {ladderData.map((player) => (
          <li key={player._id}>
            <img
              src={`http://ddragon.leagueoflegends.com/cdn/12.18.1/img/profileicon/${player.player_ids_data.profileIconId}.png`}
              alt="Player Icon"
              width="50"
              height="50"
            />
            <strong>Player Name:</strong> {player.player_ids_data.gameName}#{player.player_ids_data.tagLine},
            <strong>Tier:</strong> {player.tier},
            <strong>League Points:</strong> {player.leaguePoints},
            <strong>Win Rate:</strong> {
              player.player_summarized_stats_data && player.player_summarized_stats_data.average_win_rate
                ? (player.player_summarized_stats_data.average_win_rate * 100).toFixed(2) + '%'
                : 'N/A' // Fallback if the data doesn't exist
            }
          </li>
        ))}
      </ul>
    </div>
  );
};

export default LadderComponent;
