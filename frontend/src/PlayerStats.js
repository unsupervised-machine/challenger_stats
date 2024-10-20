
// temp file using to figure out how to load backend data to front end using routes... delete later

import React, { useEffect, useState } from 'react';
import axios from 'axios';

const PlayerStats = () => {
    const [playerStats, setPlayerStats] = useState(null); // Change to null to handle object directly
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

    if (error) {
        return <p>Error: {error}</p>; // Display error message
    }

    // Dump the raw data
    return (
        <div>
            <h1>Player Stats</h1>
            <pre>{JSON.stringify(playerStats, null, 2)}</pre> {/* Display raw data */}
        </div>
    );
};

export default PlayerStats;

