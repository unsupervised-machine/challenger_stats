import React, { useEffect, useState } from 'react';

const TestRoute = () => {
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchTestMessage = async () => {
      const testNum = 3; // Specify the test number you want to fetch
      try {
        const response = await fetch(`http://localhost:8001/api/test/${testNum}`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setMessage(data.message); // Access the message from the returned data
      } catch (error) {
        console.error('Error fetching test message:', error);
      }
    };

    fetchTestMessage();
  }, []);

  return (
    <div>
      <h1>Test Route Message 3</h1>
      <p>Message: {message}</p>
    </div>
  );
};

export default TestRoute;
