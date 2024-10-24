// App.js
import React from 'react';
import TestRoute from './TestRoute';
import TestRoute3 from './TestRoute3';
import LadderComponentSkeleton from "./LadderComponentSkeleton";
import LadderComponent from "./LadderComponent";
import PlayerMatchHistory from "./PlayerMatchHistory";

// run front end with npm start --prefix frontend
//  make sure to gracefully exit with: ctrl+c
// to ensure port is not being used: npx kill-port 3000

const App = () => {
  const playerPuuid = 'cQ5qRo8B2jc9xnlYr0eE0DnhuGiyWpTppU_VHPGVSRBKrT_EVEUFrZTKCofZciCG5y1rDIVZUMuFJA';
  return (
    <div>
      <TestRoute />
      <TestRoute3 />
      {/*<LadderComponentSkeleton />*/}
      {/*<LadderComponent />*/}
      {/*<PlayerMatchHistory playerPuuid={playerPuuid} />*/}
    </div>

  );
};

export default App;