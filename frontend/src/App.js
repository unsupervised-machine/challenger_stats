// App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import TestRoute from './TestRoute';
import TestRoute3 from './TestRoute3';
import LadderComponentSkeleton from "./LadderComponentSkeleton";
import LadderComponent from "./LadderComponent";
import PlayerMatchHistory from "./PlayerMatchHistory";

// run front end with npm start --prefix frontend
//  make sure to gracefully exit with: ctrl+c
// to ensure port is not being used: npx kill-port 3000

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<LadderComponent />} />
      <Route path="/player/:puuid" element={<PlayerMatchHistory />} />
    </Routes>
  );
};

export default App;