import React from 'react';

const Match = ({ match }) => {
  const {
    matchId,
    matchDate,
    matchDuration,
    win,
    kills = 'N/A',
    deaths = 'N/A',
    assists = 'N/A',
  } = match;

  // Format matchDate or set to 'Unknown date' if invalid
  const formattedMatchDate = matchDate ? new Date(matchDate).toLocaleDateString() : 'Unknown date';

  // Convert the 'win' boolean to a readable outcome
  const outcome = win ? 'Win' : 'Loss';

  return (
    <div className="match">
      <h3>Match ID: {matchId || 'Unknown Match ID'}</h3>
      <p>Date: {formattedMatchDate}</p>
      <p>Duration: {matchDuration ? `${matchDuration}` : 'Unknown duration'}</p>
      <p>Outcome: {outcome || 'Outcome not available'}</p>
      <p>Kills: {kills}</p>
      <p>Deaths: {deaths}</p>
      <p>Assists: {assists}</p>
      {/* Add any other relevant match details here */}
    </div>
  );
};

export default Match;
