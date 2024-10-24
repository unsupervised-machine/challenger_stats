// App.js
import React from 'react';
import TestRoute from './TestRoute';
import LadderComponentSkeleton from "./LadderComponentSkeleton";
import LadderComponent from "./LadderComponent";

// run front end with npm start --prefix frontend
//  make sure to gracefully exit with: ctrl+c
// to ensure port is not being used: npx kill-port 3000

const App = () => {
  return (
    <div>
      <TestRoute />
      {/*<LadderComponentSkeleton />*/}
      <LadderComponent />
    </div>

  );
};

export default App;