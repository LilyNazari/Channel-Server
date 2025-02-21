
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const Home = () => {
  const [channels, setChannels] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:5555/channels', {
      headers: {
        Authorization: 'authkey 1234567890'
      }
    })
    .then(response => {
      setChannels(response.data.channels);
    })
    .catch(error => {
      console.error("There was an error fetching the channels!", error);
    });
  }, []);

  return (
    <div className="home">
      <h2>Available Channels</h2>
      <ul>
        {channels.map(channel => (
          <li key={channel.endpoint}>
            <Link to={`/chat/${channel.name}`}>{channel.name}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Home;

