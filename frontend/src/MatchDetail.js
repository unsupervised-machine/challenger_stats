import React from 'react';

const MatchDetail = ({ match }) => {
  if (!match) {
    return <div>Error: Match data is not available.</div>;
  }

  const { matchId } = match;

  // Use Object.keys to iterate over match properties from '0' to '9'
  return (
    <div style={{ border: '1px solid #ddd', padding: '10px', marginTop: '10px' }}>
      <h3>Expanded Match Details for Match ID: {matchId}</h3>
      {Array.from({ length: 10 }, (_, index) => {
        const matchDetail = match[index];
        if (matchDetail) {
          return (
              <div key={index}>
                <h4>Details for Player {index}:</h4>
                <>Player PUUID: {matchDetail.puuid}</>
                <p>Player Name: {matchDetail.riotIdGameName}</p>
                <p>Player Tagline: {matchDetail.riotIdTagline}</p>
                <p>Index: {index}</p>
                {/* Champion */}
                <p>Champion Name: {matchDetail.championName ?? 'N/A'}</p>

                {/* Items*/}
                <img src={`/icons/items/${matchDetail.item0}.png`} alt={`Item ${matchDetail.item0}`}
                     style={{width: '50px', height: '50px'}}/>
                <img src={`/icons/items/${matchDetail.item1}.png`} alt={`Item ${matchDetail.item1}`}
                     style={{width: '50px', height: '50px'}}/>
                <img src={`/icons/items/${matchDetail.item2}.png`} alt={`Item ${matchDetail.item2}`}
                     style={{width: '50px', height: '50px'}}/>
                <img src={`/icons/items/${matchDetail.item3}.png`} alt={`Item ${matchDetail.item3}`}
                     style={{width: '50px', height: '50px'}}/>
                <img src={`/icons/items/${matchDetail.item4}.png`} alt={`Item ${matchDetail.item4}`}
                     style={{width: '50px', height: '50px'}}/>
                <img src={`/icons/items/${matchDetail.item5}.png`} alt={`Item ${matchDetail.item5}`}
                     style={{width: '50px', height: '50px'}}/>
                <img src={`/icons/items/${matchDetail.item6}.png`} alt={`Item ${matchDetail.item6}`}
                     style={{width: '50px', height: '50px'}}/>


                {/*<p>Item 0: {matchDetail.item0 ?? 'N/A'}</p>*/}
                {/*<p>Item 1: {matchDetail.item1 ?? 'N/A'}</p>*/}
                {/*<p>Item 2: {matchDetail.item2 ?? 'N/A'}</p>*/}
                {/*<p>Item 3: {matchDetail.item3 ?? 'N/A'}</p>*/}
                {/*<p>Item 4: {matchDetail.item4 ?? 'N/A'}</p>*/}
                {/*<p>Item 5: {matchDetail.item5 ?? 'N/A'}</p>*/}
                {/*<p>Item 6: {matchDetail.item6 ?? 'N/A'}</p>*/}

                {/* Spacer */}
                <div style={{display: 'inline-block', width: '30px'}}></div>


                {/* Summoner Spells*/}
                <img src={`/icons/spells/${matchDetail.summoner1Id}.png`} alt={`Spell ${matchDetail.summoner1Id}`}
                     style={{width: '50px', height: '50px'}}/>
                <img src={`/icons/spells/${matchDetail.summoner2Id}.png`} alt={`Spell ${matchDetail.summoner2Id}`}
                     style={{width: '50px', height: '50px'}}/>

                {/*<p>Summoner Spell 1: {matchDetail.summoner1Id ?? 'N/A'}</p>*/}
                {/*<p>Summoner Spell 2: {matchDetail.summoner2Id ?? 'N/A'}</p>*/}

                {/* Performance */}
                <p>Kills : {matchDetail.kills ?? 'N/A'}</p>
                <p>Deaths : {matchDetail.deaths ?? 'N/A'}</p>
                <p>Assists : {matchDetail.assists ?? 'N/A'}</p>
                <p>CS : {matchDetail.totalMinionsKilled ?? 'N/A'}</p>
              </div>
          );
        }
        return null;
      })}
      <p>More information about the match will be displayed here.</p>
    </div>
  );
};

export default MatchDetail;
