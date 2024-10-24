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
    championName,
    item0,
    item1,
    item2,
    item3,
    item4,
    item5,
    item6,
    riotIdGameName,
    riotIdTagline
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
        <p>Player Name: {riotIdGameName}</p>
        <p>Player Tagline: {riotIdTagline}</p>
        <p>Date: {formattedMatchDate}</p>
        <p>Duration: {matchDuration ? `${matchDuration}` : 'Unknown duration'}</p>
        <p>Outcome: {outcome || 'Outcome not available'}</p>
      </div>

      {/* Column2: Player Performance*/}
      <div style={{flex: 1}}>
        <h3>Player Performance</h3>
        <p>Champion Name: {championName}</p>
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
        <img src={`/icons/items/${item0}.png`} alt={`Item ${item0}`}
             style={{width: '50px', height: '50px'}}/>

        <p>Item 1 ID: {item1}</p>
        <img src={`/icons/items/${item1}.png`} alt={`Item ${item1}`}
             style={{width: '50px', height: '50px'}}/>

        <p>Item 2 ID: {item2}</p>
        <img src={`/icons/items/${item2}.png`} alt={`Item ${item2}`}
             style={{width: '50px', height: '50px'}}/>

        <p>Item 3 ID: {item3}</p>
        <img src={`/icons/items/${item3}.png`} alt={`Item ${item3}`}
             style={{width: '50px', height: '50px'}}/>

        <p>Item 4 ID: {item4}</p>
        <img src={`/icons/items/${item4}.png`} alt={`Item ${item4}`}
             style={{width: '50px', height: '50px'}}/>

        <p>Item 5 ID: {item5}</p>
        <img src={`/icons/items/${item5}.png`} alt={`Item ${item5}`}
             style={{width: '50px', height: '50px'}}/>

        <p>Item 6 ID: {item6}</p>
        <img src={`/icons/items/${item6}.png`} alt={`Item ${item6}`}
             style={{width: '50px', height: '50px'}}/>
      </div>
    </div>
  );
};

export default Match;
