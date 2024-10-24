import React, { useEffect, useState } from 'react';
import { getPlayerMatchHistory } from './apiService'; // API service to fetch matches
import Match from './Match'; // Component to render individual match

const PlayerMatchHistory = ({ playerPuuid }) => {
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!playerPuuid) {
      setError('Invalid player identifier.');
      setLoading(false);
      return;
    }

    const fetchMatchHistory = async () => {
      try {
        const data = await getPlayerMatchHistory(playerPuuid);
        setMatches(data);
      } catch (error) {
        console.error('Error fetching match history:', error); // Log the error for debugging
        setError('Failed to fetch match history');
      } finally {
        setLoading(false);
      }
    };

    fetchMatchHistory();
  }, [playerPuuid]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div>
      <h2>Match History for Player: {playerPuuid}</h2>
      {matches.length === 0 ? (
        <p>No match history found.</p>
      ) : (
        matches.map((match) => <Match key={match.matchId} match={match} />)
      )}
    </div>
  );
};

export default PlayerMatchHistory;
