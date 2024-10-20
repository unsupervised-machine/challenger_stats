// App.js
import React from 'react';
import TestRoute from './TestRoute';
import PlayerStats from './PlayerStats';

// run front end with npm start --prefix frontend
//  make sure to gracefully exit with: ctrl+c
// to ensure port is not being used: npx kill-port 3000

const App = () => {
  return (
    <div>
      <TestRoute />
      <PlayerStats />
    </div>

  );
};

export default App;