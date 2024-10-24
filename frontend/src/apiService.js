import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8001'; // Use environment variables for flexibility

export const getPlayerMatchHistory = async (playerPuuid) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/player-match-history/${playerPuuid}`, {
      timeout: 5000 // Optional timeout to prevent hanging requests
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      // Server responded with a status code other than 2xx
      console.error('Server Error:', error.response.status, error.response.data);
      const message = error.response.status === 404
        ? 'Player match history not found.'
        : `Server error: ${error.response.status}`;
      throw new Error(message);
    } else if (error.request) {
      // Request was made but no response received
      console.error('No response received:', error.request);
      throw new Error('No response received from server');
    } else {
      // Something else happened while setting up the request
      console.error('Error setting up request:', error.message);
      throw new Error('Error setting up request');
    }
  }
};
