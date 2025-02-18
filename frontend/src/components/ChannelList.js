import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const ChannelList = ({ onSelectChannel }) => {
  const [channels, setChannels] = useState([]);

  useEffect(() => {
    const fetchChannels = async () => {
      try {
        const response = await axios.get('http://localhost:5555/channels', {
          headers: {'Authorization': 'authkey 1234567890'}
        });
        // Extracting channels array from the response
        setChannels(response.data.channels);
      } catch (error) {
        console.error("Error fetching channels:", error);
      }
    };
    fetchChannels();
  }, []);

  return (
    <div className="p-4 bg-white rounded-xl shadow-md">
      <ul>
        {channels.map((channel) => (
          <li
            key={channel._id}
            className="mb-2 p-2 cursor-pointer hover:bg-gray-100 rounded-lg"
            onClick={() => onSelectChannel(channel._id)}
          >
            <Link to={`/chat/${channel.name}`}>{channel.name}</Link>
            {channel.name}
          </li>
        ))}
      </ul>
    </div>
  );
};



export default ChannelList;
