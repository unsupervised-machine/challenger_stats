import React from 'react';

const Match = ({ match }) => {
  return (
    <div className="match">
      <h3>Match ID: {match.matchId}</h3>
      <p>Date: {new Date(match.date).toLocaleDateString()}</p>
      <p>Duration: {match.duration} minutes</p>
      <p>Outcome: {match.outcome}</p>
      <p>Kills: {match.kills}</p>
      <p>Deaths: {match.deaths}</p>
      <p>Assists: {match.assists}</p>
      {/* Add any other relevant match details here */}
    </div>
  );
};

export default Match;
