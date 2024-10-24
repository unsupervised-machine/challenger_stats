import React from 'react';

const Match = ({ match }) => {
  const {
    matchId,
    date,
    duration,
    outcome,
    kills = 'N/A',
    deaths = 'N/A',
    assists = 'N/A',
  } = match;

  const formattedDate = date ? new Date(date).toLocaleDateString() : 'Unknown date';

  return (
    <div className="match">
      <h3>Match ID: {matchId || 'Unknown Match ID'}</h3>
      <p>Date: {formattedDate}</p>
      <p>Duration: {duration ? `${duration} minutes` : 'Unknown duration'}</p>
      <p>Outcome: {outcome || 'Outcome not available'}</p>
      <p>Kills: {kills}</p>
      <p>Deaths: {deaths}</p>
      <p>Assists: {assists}</p>
      {/* Add any other relevant match details here */}
    </div>
  );
};

export default Match;
