import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Reviews from './Reviews';
import './App.css';
function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Check if the user is logged in when the app loads
    axios.get('http://localhost:5000/google_login')
      .then(response => {
        setUser(response.data);  // Assuming the response contains user info
      })
      .catch(error => {
        console.error('Error fetching user data:', error);
      });
  }, []);

  const handleLogin = () => {
    window.location.href = 'http://localhost:5000/google_login'; // Redirect to Google login
  };

  const handleLogout = () => {
    // Implement logout functionality here (e.g., clearing session or token)
    setUser(null);
    window.location.href = 'http://localhost:5000/logout'; // Trigger logout in the Flask app
  };

  return (
    <div style={{ padding: '10px' }}>
      <h1 align='center'>GOOGLE INTEGRATION PORTAL </h1>
      
      {user ? (
        <div>
          <h3>Welcome, {user.displayName}!</h3>
          <button onClick={handleLogout}>Logout</button>
        </div>
      ) : (
        <h1 align = 'center'><button className="button" onClick={handleLogin}>Login with Google</button></h1>
      )}

      <Reviews />
    </div>
  );
}





export default App;
