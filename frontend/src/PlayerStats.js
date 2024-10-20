
// temp file using to figure out how to load backend data to front end using routes... delete later

// src/PlayerStats.js
import React, { useEffect, useState } from 'react';
import axios from 'axios'; // Optional, use Fetch API if preferred

const PlayerStats = () => {
    const [playerStats, setPlayerStats] = useState([]);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true); // Loading state

    useEffect(() => {
        // Fetch player stats data from the backend API
        const fetchPlayerStats = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/player-stats'); // Adjust URL based on your backend
                setPlayerStats(response.data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false); // End loading state
            }
        };

        fetchPlayerStats();
    }, []);

    if (loading) {
        return <p>Loading...</p>; // Display loading message
    }

    return (
        <div>
            <h1>Player Stats</h1>
            {error && <p>Error: {error}</p>}
            <ul>
                {playerStats.map(stat => (
                    <li key={stat._id}>
                        {stat.summonerId}: {stat.leaguePoints} LP ({stat.tier} {stat.rank}) - {stat.wins}W {stat.losses}L
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default PlayerStats;
