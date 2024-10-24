import axios from 'axios';

const API_BASE_URL = 'http://localhost:8001'; // Adjust this to your FastAPI server address

export const getPlayerMatchHistory = async (playerPuuid) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/player-match-history/${playerPuuid}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching player match history:', error);
    throw error;
  }
};
