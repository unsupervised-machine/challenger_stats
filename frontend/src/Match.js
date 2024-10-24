import React from 'react';

const Match = ({ match }) => {
  const {
    matchId,
    puuid,
    gameMode,
    matchDate,
    matchDuration,
    win,
    summoner1Id = 'N/A',
    summoner2Id = 'N/A',
    kills = 'N/A',
    deaths = 'N/A',
    assists = 'N/A',
    totalMinionsKilled,
    item0,
    item1,
    item2,
    item3,
    item4,
    item5,
    item6,
  } = match;

  // Format matchDate or set to 'Unknown date' if invalid
  const formattedMatchDate = matchDate ? new Date(matchDate).toLocaleDateString() : 'Unknown date';

  // Convert the 'win' boolean to a readable outcome
  const outcome = win ? 'Win' : 'Loss';

  return (
    <div className="match" style={{ display: 'flex', justifyContent: 'space-between', padding: '10px', borderBottom: '1px solid #ddd' }}>
      {/* Column1: Basic match information */}
      <div style={{flex: 1}}>
        <h3>Match Details</h3>
        <p>Game Mode: {gameMode}</p>
        <p>Match ID: {matchId || 'Unknown Match ID'}</p>
        <p>PUUID: {puuid}</p>
        <p>Date: {formattedMatchDate}</p>
        <p>Duration: {matchDuration ? `${matchDuration}` : 'Unknown duration'}</p>
        <p>Outcome: {outcome || 'Outcome not available'}</p>
      </div>

      {/* Column2: Player Performance*/}
      <div style={{ flex: 1 }}>
        <h3>Player Performance</h3>
        <p>Kills: {kills}</p>
        <p>Deaths: {deaths}</p>
        <p>Assists: {assists}</p>
        <p>CS: {totalMinionsKilled}</p>
      </div>

      {/* Center column: Summoner information */}
      <div style={{ flex: 1 }}>
        <h4>Summoner Spells</h4>
        <p>Summoner Spell 1 ID: {summoner1Id}</p>
        <p>Summoner Spell 2 ID: {summoner2Id}</p>
      </div>

      {/* Right column: Items */}
      <div style={{flex: 1}}>
        <h4>Items</h4>
        <p>Item 0 ID: {item0}</p>
        <p>Item 1 ID: {item1}</p>
        <p>Item 2 ID: {item2}</p>
        <p>Item 3 ID: {item3}</p>
        <p>Item 4 ID: {item4}</p>
        <p>Item 5 ID: {item5}</p>
        <p>Item 6 ID: {item6}</p>
      </div>
    </div>
  );
};

export default Match;
