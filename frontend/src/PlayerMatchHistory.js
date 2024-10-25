// PlayerMatchHistory.js

import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom'; // Import useParams
import { getPlayerMatchHistory } from './apiService'; // API service to fetch matches
import Match from './Match'; // Component to render individual match
import MatchDetail from "./MatchDetail";

const PlayerMatchHistory = () => {
  const { puuid } = useParams(); // Retrieve puuid from the URL
  const [matches, setMatches] = useState([]);
  const [expandedMatches, setExpandedMatches] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!puuid) {
      setError('Invalid player identifier.');
      setLoading(false);
      return;
    }

    const fetchMatchHistory = async () => {
      try {
        const data = await getPlayerMatchHistory(puuid);
        setMatches(data);
      } catch (error) {
        console.error('Error fetching match history:', error); // Log the error for debugging
        setError('Failed to fetch match history');
      } finally {
        setLoading(false);
      }
    };

    fetchMatchHistory();
  }, [puuid]);

  const expandMatch = (matchId) => {
    setExpandedMatches((prevExpandedMatches) => ({
      ...prevExpandedMatches,
      [matchId]: !prevExpandedMatches[matchId], // Toggle the expanded state for the match
    }));
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
      <div>
        <h2>Match History</h2>
        {/*<h2>Match History for Player: {puuid}</h2>*/}
        {matches.length === 0 ? (
            <p>No match history found.</p>
        ) : (
            matches.map((match) => (
                <div key={match.matchId}>
                  <Match match={match}/>
                  <button onClick={() => expandMatch(match.matchId)}>
                    {expandedMatches[match.matchId] ? 'Collapse' : 'Expand'}
                  </button>
                  {expandedMatches[match.matchId] && <MatchDetail match={match}/>}
                </div>
            ))
        )}
      </div>
  );
};

export default PlayerMatchHistory;
