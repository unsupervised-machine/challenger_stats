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

  const placeholderImg = '/icons/items/9168.png'


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

      {/* Column3: Summoner information */}
      <div style={{flex: 1}}>
        <h4>Summoner Spells</h4>
        <img
            src={summoner1Id !== 0 ? `/icons/spells/${summoner1Id}.png` : placeholderImg}
            alt={summoner1Id !== 0 ? `Spell ${summoner1Id}` : 'Placeholder Item'}
            style={{width: '50px', height: '50px'}}
        />
        <img
            src={summoner2Id !== 0 ? `/icons/spells/${summoner2Id}.png` : placeholderImg}
            alt={summoner2Id !== 0 ? `Spell ${summoner2Id}` : 'Placeholder Item'}
            style={{width: '50px', height: '50px'}}
        />
        {/*<p>Summoner Spell 1 ID: {summoner1Id}</p>*/}
        {/*<p>Summoner Spell 2 ID: {summoner2Id}</p>*/}
      </div>

      {/* Column4: Items */}

      <div style={{flex: 1}}>
        <h4>Items</h4>

        {/* Item 0 */}
        <img
            src={item0 !== 0 ? `/icons/items/${item0}.png` : placeholderImg}
            alt={item0 !== 0 ? `Item ${item0}` : 'Placeholder Item'}
            style={{width: '50px', height: '50px'}}
        />

        {/* Item 1 */}
        <img
            src={item1 !== 0 ? `/icons/items/${item1}.png` : placeholderImg}
            alt={item1 !== 0 ? `Item ${item1}` : 'Placeholder Item'}
            style={{width: '50px', height: '50px'}}
        />

        {/* Item 2 */}
        <img
            src={item2 !== 0 ? `/icons/items/${item2}.png` : placeholderImg}
            alt={item2 !== 0 ? `Item ${item2}` : 'Placeholder Item'}
            style={{width: '50px', height: '50px'}}
        />

        {/* Item 3 */}
        <img
            src={item3 !== 0 ? `/icons/items/${item3}.png` : placeholderImg}
            alt={item3 !== 0 ? `Item ${item3}` : 'Placeholder Item'}
            style={{width: '50px', height: '50px'}}
        />

        {/* Item 4 */}
        <img
            src={item4 !== 0 ? `/icons/items/${item4}.png` : placeholderImg}
            alt={item4 !== 0 ? `Item ${item4}` : 'Placeholder Item'}
            style={{width: '50px', height: '50px'}}
        />

        {/* Item 5 */}
        <img
            src={item5 !== 0 ? `/icons/items/${item5}.png` : placeholderImg}
            alt={item5 !== 0 ? `Item ${item5}` : 'Placeholder Item'}
            style={{width: '50px', height: '50px'}}
        />

        {/* Item 6 */}
        <img
            src={item6 !== 0 ? `/icons/items/${item6}.png` : placeholderImg}
            alt={item6 !== 0 ? `Item ${item6}` : 'Placeholder Item'}
            style={{width: '50px', height: '50px'}}
        />
      </div>
    </div>
  );
};

export default Match;
