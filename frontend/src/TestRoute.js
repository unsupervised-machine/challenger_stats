import React, { useEffect, useState } from 'react';

const TestRoute = () => {
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchTestMessage = async () => {
      try {
        const response = await fetch('http://localhost:8001/api/test');
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
      <h1>Test Route Message</h1>
      <p>{message}</p>
    </div>
  );
};

export default TestRoute;