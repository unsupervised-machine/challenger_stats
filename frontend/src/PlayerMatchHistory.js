import React, { useEffect, useState } from 'react';
import { getPlayerMatchHistory } from './apiService';
import Match from './Match';

const PlayerMatchHistory = ({ playerPuuid }) => {
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMatchHistory = async () => {
      try {
        const data = await getPlayerMatchHistory(playerPuuid);
        setMatches(data);
      } catch (error) {
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
