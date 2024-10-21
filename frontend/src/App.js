// App.js
import React from 'react';
import TestRoute from './TestRoute';
import PlayerStats from './PlayerStats';
import LadderComponent from "./LadderComponent";

// run front end with npm start --prefix frontend
//  make sure to gracefully exit with: ctrl+c
// to ensure port is not being used: npx kill-port 3000

const App = () => {
  return (
    <div>
      <TestRoute />
      <LadderComponent />
      {/*<PlayerStats />*/}
    </div>

  );
};

export default App;